import sys
if sys.version_info >= (3,0):
    from urllib.error import HTTPError
else:
    from urllib2 import HTTPError

# try the old version, then fallback to the new one
try:
    from xml.etree import ElementTree
    from xml.etree.ElementTree import parse, fromstring, Element
except ImportError:
    from elementtree import ElementTree
    from elementtree.ElementTree import parse, fromstring, Element

from v1pysdk.client import *
from v1pysdk import V1Meta
from common_test_server import PublicTestServerConnection

import pytest

class TestV1Connection():
    def test_connect(self):
        username = PublicTestServerConnection.username
        password = PublicTestServerConnection.password
        address = PublicTestServerConnection.address
        instance = PublicTestServerConnection.instance

        server = V1Server(address=address, username=username, password=password,instance=instance)
        # The story names, but limit to only the first result so we don't get inundated with results
        code, body = server.fetch('/rest-1.v1/Data/Story?sel=Name&page=1,0')

        elem = fromstring(body)
        assert(elem.tag == 'Assets')

    def test_meta_connect_instance_url(self):
        v1 = None
        try:
            v1 = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                username = PublicTestServerConnection.username,
                password = PublicTestServerConnection.password,
                )
        except Exception as e:
            pytest.fail("Error trying to create connection: {0}".format(str(e)))

        try:
            items = v1.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error running query from connection: {0}".format(str(e)))

    def test_meta_connect_instance_and_address(self):
        v1 = None
        try:
            v1 = V1Meta(
                address = PublicTestServerConnection.address,
                instance = PublicTestServerConnection.instance,
                username = PublicTestServerConnection.username,
                password = PublicTestServerConnection.password,
                )
        except Exception as e:
            pytest.fail("Error trying to create connection: {0}".format(str(e)))
        try:
            items = v1.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error running query from connection: {0}".format(str(e)))

    def test_meta_connect_instance_url_overrides_separate(self):
        v1 = None
        address = ''
        instance = None

        try:
            v1 = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                address = address,
                instance = instance,
                username = PublicTestServerConnection.username,
                password = PublicTestServerConnection.password,
                )
        except Exception as e:
            pytest.fail("Error trying to create connection: {0}".format(str(e)))

        try:
            items = v1.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error trying to create connection: {0}".format(str(e)))

    def test_meta_connect_oauth(self):
        v1 = None
        try:
            v1 = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                #no username
                password = PublicTestServerConnection.token,
                use_password_as_token=True,
                )
        except Exception as e:
            pytest.fail("Error trying to create connection: {0}".format(str(e)))

        try:
            items = v1.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error running query from connection: {0}".format(str(e)))

    def test_meta_connect_oauth_ignores_username(self):
        v1 = None
        username = ''

        try:
            v1 = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                username = username,
                password = PublicTestServerConnection.token,
                use_password_as_token=True,
                )
        except Exception as e:
            pytest.fail("Error trying to create connection: {0}".format(str(e)))

        try:
            items = v1.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error running query from connection: {0}".format(str(e)))

    def test_connect_fails_when_invalid(self):
        v1bad = None
        username = ''
        password = ''

        try:
            v1bad = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                username = username,
                password = password,
                use_password_as_token=False,
                )
            # we have to try to use it to get it to connect and fail
            items = v1bad.Story.select('Name').page(size=1)
            items.first() #run the query
        except HTTPError as e:
            assert(str(e.code) == '401', "Connection failed for reasons other than authorization")
        else:
            pytest.fail("Connection succeeded with bad credentials.")

    def test_reconnect_succeeds_after_invalid(self):
        v1bad = None
        username = ''
        password = ''

        try:
            v1bad = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                username = username,
                password = password,
                use_password_as_token=False,
                )
            items = v1bad.Story.select('Name').page(size=1)
            items.first() #run the query
        except HTTPError as e:
            assert(str(e.code) == '401', "Connection failed for reasons other than authorization")
        else:
            pytest.fail("First connection succeeded with bad credentials, cannot continue test")

        v1good = None

        # Connect correctly first
        try:
            v1good = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                password = PublicTestServerConnection.token,
                use_password_as_token=True,
                )
            items = v1good.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error running query from good connection: {0}".format(str(e)))

    def test_reconnect_fails_when_invalid(self):
        v1good = None

        # Connect correctly first
        try:
            v1good = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                password = PublicTestServerConnection.token,
                use_password_as_token=True,
                )
            items = v1good.Story.select('Name').page(size=1)
            items.first() #run the query
        except Exception as e:
            pytest.fail("Error running query from good connection: {0}".format(str(e)))

        v1bad = None
        username = ''

        password = ''

        try:
            v1bad = V1Meta(
                instance_url = PublicTestServerConnection.instance_url,
                username = username,
                password = password,
                use_password_as_token=False,
                )
            items = v1bad.Story.select('Name').page(size=1)
            items.first() #run the query
        except HTTPError as e:
            assert(str(e.code) == "401", "Connection failed for reasons other than authorization")
        else:
            assert(str(e.code) == "401", "Second connection failed for reasons other than authorization")
