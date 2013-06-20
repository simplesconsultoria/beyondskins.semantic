# -*- coding: utf-8 -*-

from beyondskins.semantic.portal.testing import INTEGRATION_TESTING
from beyondskins.semantic.portal.tiles.nitf import NITFBasicTile
from beyondskins.semantic.portal.tiles.poll import PollTile
from collective.cover.tiles.base import IPersistentCoverTile
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest2 as unittest
from beyondskins.semantic.portal.tiles.author import AuthorTile


class TileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']


class NITFBasicTileTestCase(TileTestCase):

    def setUp(self):
        super(NITFBasicTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@%s/%s' % ('nitf.basic', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(NITFBasicTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, NITFBasicTile))

        tile = NITFBasicTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['collective.nitf.content'])


class PollTileTestCase(TileTestCase):

    def setUp(self):
        super(PollTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@%s/%s' % ('poll', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(PollTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, PollTile))

        tile = PollTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['collective.polls.poll'])


class AuthorTileTestCase(TileTestCase):

    def setUp(self):
        super(AuthorTileTestCase, self).setUp()
        self.tile = self.portal.restrictedTraverse(
            '@@%s/%s' % ('semantic.author', 'test-tile'))

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(AuthorTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, AuthorTile))

        tile = AuthorTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertListEqual(
            self.tile.accepted_ct(), ['Collection'])
