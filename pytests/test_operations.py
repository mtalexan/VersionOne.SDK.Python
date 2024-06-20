"""
from testtools import TestCase
from testtools.assertions import assert_that
from testtools.content import text_content
from testtools.matchers import Equals
"""

import v1pysdk
from common_test_server import PublicTestServerConnection
import common_test_server
import test_common_setup
import pytest


class TestV1Operations(test_common_setup.TestV1CommonSetup):
    def test_quick_close_and_reopen(self):
        """Creates a story, quick closes it, then reopens it, then quick closes again"""
        with common_test_server.PublicTestServerConnection.getV1Meta() as v1:
            newStory = None
            try:
                newStory = self.test_initial_create_story(v1)
            except Exception as e:
                pytest.fail("Unable to setup by creating initial test story: {0}".format(str(e)))

            assert(newStory.IsClosed == False, "New story created already closed, cannot test")

            try:
                newStory.QuickClose()
            except Exception as e:
                pytest.fail("Error while quick closing story: {0}".format(str(e)))

            try:
                v1.commit()
            except Exception as e:
                pytest.fail("Error while syncing commits after close {0}".format(str(e)))

            assert(newStory.IsClosed == True, "Story didn't close when QuickClose() was called")

            try:
                newStory.Reactivate()
            except Exception as e:
                pytest.fail("Error while reactivating story {0}".format(str(e)))

            try:
                v1.commit()
            except Exception as e:
                pytest.fail("Error while syncing commits after reactivation")
            assert(newStory.IsClosed == 'false', "Story didn't re-open when Reactivate() was called")

            # "cleanup" by closing the story
            newStory.QuickClose()
            v1.commit()
