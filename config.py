import yaml
from models import *


class ConfigException(Exception):
    pass


class Config:

    def __init__(self, path: str):
        self.routes = {}
        self._backends = {}
        self.default_response = DefaultResponse("No default defined", 500)
        with open(path, "r") as config_file:
            config_dict = yaml.safe_load(config_file)
            # This is prettier in scala, sorry
            self._backends = dict(map(lambda backend: (backend.name, backend), map(Config.parse_backend, config_dict['backends'])))
            self.routes = [self.parse_route(route) for route in config_dict['routes']]
            self.default_response = DefaultResponse(config_dict['default_response']['body'], config_dict['default_response']['status_code'])
        return

    @staticmethod
    def parse_backend(backend: dict) -> Backend:
        return Backend(name=backend['name'], match_labels=[MatchLabel(label) for label in backend['match_labels']])

    def parse_route(self, route: dict) -> Route:
        backend_name = route['backend']
        path_prefix = route['path_prefix']
        if backend_name not in self._backends:
            raise ConfigException("{} mapped to invalid backend {}".format(path_prefix, backend_name))

        return Route(path_prefix=route['path_prefix'], backend=self._backends[backend_name])




if __name__ == "__main__":

    ml = MatchLabel("key1=value1")
    print(ml)
    cfg = Config("./cfg.yaml")
    for route in cfg.routes:
        print(route)
