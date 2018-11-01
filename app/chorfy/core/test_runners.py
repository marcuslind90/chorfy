from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """
    TestRunner that does not setup a test database.

    Expects the user to mock all database calls.
    """
    def setup_databases(self, *args, **kwargs):
        pass

    def teardown_databases(self, *args, **kwargs):
        pass
