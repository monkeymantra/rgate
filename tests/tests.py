import unittest
from config import Config
from models import * # code from module you're testing


class ModelTests(unittest.TestCase):

    CONFIG_FIXTURE = {
        "routes": [Route("/api/payments", backend=Backend())]
    }

    def setUp(self) -> None:
        self.config = Config("./cfg.yaml")

    def _testRoute(self, route: Route, shouldBe: Route):
        assert route.path_prefix == shouldBe.path_prefix
        self._testBackend(route.backend, shouldBe.backend)

    def _testBackend(self, backend: Backend, shouldBe: Backend):
        assert sorted(backend.match_labels) == sorted(shouldBe.match_labels)
        assert backend.name == shouldBe.name

    def testConfigParses(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        assert len(self.config.routes) == 2
        for route in self.config.routes:



    def testB(self):
        """test case B"""
        assert foo+foo == 34, "can't add Foo instances"

    def testC(self):
        """test case C"""
        assert foo.baz() == "blah", "baz() not returning blah correctly"


class OtherTestCase(unittest.TestCase):

    def setUp(self):
        blah_blah_blah()

    def tearDown(self):
        blah_blah_blah()

    def testBlah(self):
        assert self.blahblah == "blah", "blah isn't blahing blahing correctly"


if __name__ == "__main__":
    unittest.main() # run all tests