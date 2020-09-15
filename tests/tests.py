import unittest
from config import Config
from rgate import RGate


CONFIG_FIXTURE = {'routes': [{'path_prefix': '/api/payments', 'backend': 'payment'},
                             {'path_prefix': '/api/orders', 'backend': 'orders'}],
                  'default_response': {'body': 'This is not reachable', 'status_code': 403},
                  'backends': [{'name': 'payment', 'match_labels': ['app_name=payment', 'env=production']},
                               {'name': 'orders', 'match_labels': ['app_name=orders', 'env=production']}]}


class ModelTests(unittest.TestCase):

    def setUp(self) -> None:
        self.config = Config(CONFIG_FIXTURE)

    def testConfigParses(self):
        """Check if we can create a Config from a dict"""
        assert len(self.config.routes) == 2
        assert "/api/payments" in self.config.routes
        assert self.config.routes["/api/payments"].backend.name == "payment"
        assert "/api/orders" in self.config.routes
        assert self.config.routes["/api/orders"].backend.name == "orders"
        assert self.config.default_response.status_code == 403
        assert self.config.default_response.body == "This is not reachable"
        assert "payment" in self.config.backends
        assert "orders" in self.config.backends

    def testYamlParses(self):
        """This is where we'd double-check our yaml parsing"""
        pass


class GatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config(CONFIG_FIXTURE)
        self.port = 8080
        self.rgate = RGate(8080, self.config)
        self.test_client = self.rgate.rgate.test_client()

    def testCanGetRoutes(self):
        """"Make sure all routes are in the app"""
        for route_prefix in self.config.routes:
            print("Trying to get ")
            resp = self.test_client.get(route_prefix)
            assert resp.status_code == 200

    def testDefaultResponse(self):
        """Make sure default response matches"""
        resp = self.test_client.get("/some/bogus/url")
        assert resp.status_code == 403
        assert resp.data == b'This is not reachable'

    def testCanPostRoutes(self):
        """Make sure all routes can be POSTed to"""
        pass


class DockerTests(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a docker client"""
        pass

    def testCanFindBackend(self):
        """See if we can resolve a backend from labels"""
        pass


if __name__ == "__main__":
    unittest.main() # run all tests