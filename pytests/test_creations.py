import v1pysdk
import common_test_server
from test_common_setup import TestV1CommonSetup

class TestV1Create(TestV1CommonSetup):
    def test_create_story(self, v1):
        """Creates a very simple story"""
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
	        # common setup already does this and tests the creation, it just needs a V1 instance to work on
	        self.test_initial_create_story(v1)
