import pytest
import common_test_server

@pytest.fixture
def v1():
    return common_test_server.PublicTestServerConnection.getV1Meta()
