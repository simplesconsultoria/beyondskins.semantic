# -*- coding: utf-8 -*-

from beyondskins.semantic.portal.portlets import news_articles_in_section
from beyondskins.semantic.portal.testing import INTEGRATION_TESTING
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from Products.GenericSetup.utils import _getDottedName
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest2 as unittest


class TestNewsArticlesInSectionPortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlets.NewsArticlesInSection')
        self.assertEqual(portlet.addview, 'portlets.NewsArticlesInSection')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='portlets.NewsArticlesInSection')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual([
            'plone.app.portlets.interfaces.IColumn',
            'plone.app.portlets.interfaces.IDashboard',
            ], registered_interfaces)

    def testInterfaces(self):
        portlet = news_articles_in_section.Assignment(count=5)
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portlet = getUtility(IPortletType, name='portlets.NewsArticlesInSection')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], news_articles_in_section.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = news_articles_in_section.Assignment(count=5)
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, news_articles_in_section.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = news_articles_in_section.Assignment(count=5)

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, news_articles_in_section.Renderer))


class TestRenderer(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        # Make sure News Articles use simple_publication_workflow
        self.portal.portal_workflow.setChainForPortalTypes(
            ['collective.nitf.content'], ['simple_publication_workflow'])

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment or news_articles_in_section.Assignment(template='portlet_recent', macro='portlet')

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_published_news_articles(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        r = self.renderer(assignment=news_articles_in_section.Assignment(count=5))
        self.assertEqual(0, len(r.published_news_articles()))

        self.portal.invokeFactory('collective.nitf.content', 'n1')
        self.portal.invokeFactory('collective.nitf.content', 'n2')
        self.portal.portal_workflow.doActionFor(self.portal.n1, 'publish')
        r = self.renderer(assignment=news_articles_in_section.Assignment(count=5))
        self.assertEqual(1, len(r.published_news_articles()))

        self.portal.portal_workflow.doActionFor(self.portal.n2, 'publish')
        r = self.renderer(assignment=news_articles_in_section.Assignment(count=5))
        self.assertEqual(2, len(r.published_news_articles()))

    def test_all_news_link(self):
        if 'news' in self.portal:
            self.portal._delObject('news')
        r = self.renderer(assignment=news_articles_in_section.Assignment(count=5))
        self.assertEqual(r.all_news_link(), None)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'news')
        self.assertTrue(r.all_news_link().endswith('/news'))
