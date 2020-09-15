import yaml
from models import *


class ConfigException(Exception):
    pass


class Config:
    def __init__(self, config_dict: dict):
        """Main config object"""
        self.backends = dict((backend.name, backend) for backend in
                        (Config.parse_backend(backend_dict) for backend_dict in config_dict['backends']))
        self.routes = dict((route.path_prefix, route) for route in
                           (self.parse_route(route_dict, self.backends) for route_dict in config_dict['routes']))
        self.default_response = DefaultResponse(config_dict['default_response']['body'],
                                                config_dict['default_response']['status_code'])

    @staticmethod
    def parse_backend(backend: dict) -> Backend:
        return Backend(name=backend['name'], match_labels=[MatchLabel(label) for label in backend['match_labels']])

    def parse_route(self, route: dict, backends: dict) -> Route:
        backend_name = route['backend']
        path_prefix = route['path_prefix']
        if backend_name not in backends:
            raise ConfigException("{} mapped to invalid backend {}".format(path_prefix, backend_name))

        return Route(path_prefix=route['path_prefix'], backend=backends[backend_name])


class YamlConfig(Config):
    def __init__(self, path: str):
        super().__init__(self._config_dict(path))

    def _config_dict(self, path):
        with open(path, "r") as config_file:
            config_dict = yaml.safe_load(config_file)
            return config_dict
