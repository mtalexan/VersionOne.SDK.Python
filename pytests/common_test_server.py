
importedOk=True

# Allow for tests that can't don't import this to use this file still
try:
    import v1pysdk
except ImportError:
    importedOk=False


class PublicTestServerConnection():
    username = 'admin'
    password = 'admin'
    address = 'www14.v1host.com'
    instance = 'v1sdktesting'
    scheme = 'https'
    # must match scheme + "://" + address + "/" + instance
    instance_url = 'https://www14.v1host.com/v1sdktesting'
    token = '1.VdeWXQVNdY0yVpYexTtznCxcWTQ='

    def __init__():
        pass

    @staticmethod
    def getV1Meta():
        """Creates a V1Meta object from the default configuration and returns it
        """
        # If we couldn't import the v1pysdk, we can't create the object
        if not importedOk:
            return None
        else:
            return v1pysdk.V1Meta(
                address = PublicTestServerConnection.address,
                instance = PublicTestServerConnection.instance,
                scheme = 'https',
                username = PublicTestServerConnection.username,
                password = PublicTestServerConnection.password,
            )
