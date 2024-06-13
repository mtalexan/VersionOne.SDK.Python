#from testtools import TestCase

import v1pysdk
from .common_test_server import PublicTestServerConnection
from .common_test_setup import TestV1CommonSetup

class TestV1Create(TestV1CommonSetup):
    def test_create_story(self):
        """Creates a very simple story"""
        with PublicTestServerConnection.getV1Meta() as v1:
	        # common setup already does this and tests the creation, it just needs a V1 instance to work on
	        self._create_story(v1)
