import unittest

from repoze.bfg.configuration import Configurator
from repoze.bfg import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()
        self.config.begin()

    def tearDown(self):
        self.config.end()

    def test_my_view(self):
        from bmibargains.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'bmibargains')

