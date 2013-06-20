# -*- coding: utf-8 -*-

from beyondskins.semantic.portal.portlets import author
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


class TestAuthorPortlet(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlets.Author')
        self.assertEqual(portlet.addview, 'portlets.Author')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='portlets.Author')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEqual([
            'plone.app.portlets.interfaces.IColumn',
            'plone.app.portlets.interfaces.IDashboard',
            ], registered_interfaces)

    def testInterfaces(self):
        portlet = author.Assignment(count=5)
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portlet = getUtility(IPortletType, name='portlets.Author')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEqual(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], author.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = author.Assignment(count=5)
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, author.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = author.Assignment(count=5)

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, author.Renderer))


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
        assignment = assignment or author.Assignment(template='portlet_recent', macro='portlet')

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_published_news_articles(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        r = self.renderer(assignment=author.Assignment(count=5))
        self.assertEqual(0, len(r.published_news_articles()))

        self.portal.invokeFactory('collective.nitf.content', 'n1')
        self.portal.invokeFactory('collective.nitf.content', 'n2')
        self.portal.portal_workflow.doActionFor(self.portal.n1, 'publish')
        r = self.renderer(assignment=author.Assignment(count=5))
        self.assertEqual(1, len(r.published_news_articles()))

        self.portal.portal_workflow.doActionFor(self.portal.n2, 'publish')
        r = self.renderer(assignment=author.Assignment(count=5))
        self.assertEqual(2, len(r.published_news_articles()))

    def test_all_news_link(self):
        if 'news' in self.portal:
            self.portal._delObject('news')
        r = self.renderer(assignment=author.Assignment(count=5))
        self.assertEqual(r.all_news_link(), None)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'news')
        self.assertTrue(r.all_news_link().endswith('/news'))
