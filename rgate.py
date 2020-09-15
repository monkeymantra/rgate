from flask import Flask, request
from flask import Response
from config import Config
from docker_manager import DockerManager
from models import *
from requests import request as make_request
import requests

class RGate:
    def __init__(self, port: int, config_path: str):
        self.port = port
        self.config = Config(config_path)
        self.docker = DockerManager()
        self.rgate = Flask("rgate")
        self.rgate.register_error_handler(404, self.error_handler())
        self._add_routes()

    def error_handler(self):
        @self.rgate.errorhandler(404)
        def default_response(e):
            return Response(self.config.default_response.body, self.config.default_response.status_code)
        return default_response

    def run_app(self):
        self.rgate.run(port=self.port, debug=True)

    def _add_routes(self):
        # Add routes dynamically to Flask
        print("Adding backends")
        for route in self.config.routes:
            print("Adding route {}".format(route))
            self.rgate.add_url_rule(route.path_prefix,
                                    route.path_prefix.replace("/", "_"),  # Make sure name is legal
                                    self._backend_func(route),
                                    methods=['POST', 'PUT', 'GET', 'DELETE'])
            self.rgate.add_url_rule(route.path_prefix + "/<path:path>",  # Handle wildcard after prefix
                                    route.path_prefix.replace("/", "_") + "extras",  # Make sure name is legal
                                    self._backend_func(route),
                                    methods=['POST', 'PUT', 'GET', 'DELETE'])

    def _backend_func(self, route: Route):
        container = self.docker.find_container(route.backend)
        port = container.ports.get("80/tcp")[0]["HostPort"]  # Keep this simple as a default
        url = "http://localhost:{}{}".format(port, route.path_prefix)

        def backend_func(path=None):
            try:
                resp = make_request(request.method, url, params=request.args, data=request.data)
                return Response(resp.content, resp.status_code)
            except requests.ConnectionError:
                return Response("Backend down", 503)
        return backend_func


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='RGate API Gateway')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port to expose')
    parser.add_argument('--config', type=str, default="./cfg.yaml",
                        help='Path to config yaml')


    args = parser.parse_args()
    rgate = RGate(args.port, args.config)
    rgate.run_app()




