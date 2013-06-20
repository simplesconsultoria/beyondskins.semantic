# -*- coding: utf-8 -*-

from beyondskins.semantic.portal.config import PROJECTNAME
from beyondskins.semantic.portal.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest

DEPENDENCIES = [
    'plone.app.theming',
    'collective.cover',
    'collective.nitf',
    's17.person',
    'sc.behavior.journalist',
]

JS = [
    '++theme++beyondskins.semantic.portal/javascripts/beyondskins_cartacapital_portal.js',
]

CSS = [
    '++theme++beyondskins.semantic.portal/src/beyondskins_cartacapital_portal.css',
]

TILES = [
    'nitf.basic',
    'poll',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_dependencies_installed(self):
        expected = set(DEPENDENCIES)
        installed = set(name for name, product in self.qi.items()
                        if product.isInstalled())
        result = sorted(expected - installed)

        self.assertFalse(result,
            "These dependencies are not installed: " + ", ".join(result))

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IThemeSpecific', layers, 'browser layer not installed')

    def test_javascript_registry(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JS:
            self.assertIn(js, portal_javascripts.getResourceIds())

    def test_css_registry(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.assertIn(css, portal_css.getResourceIds())

    def test_tiles(self):
        self.registry = getUtility(IRegistry)
        registered_tiles = self.registry['plone.app.tiles']
        for tile in TILES:
            self.assertIn(tile, registered_tiles)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME),
                         '%s not uninstalled' % PROJECTNAME)

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IThemeSpecific', layers, 'browser layer not removed')

    def test_javascript_registry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JS:
            self.assertNotIn(js, portal_javascripts.getResourceIds())

    def test_css_registry_removed(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.assertNotIn(css, portal_css.getResourceIds())
