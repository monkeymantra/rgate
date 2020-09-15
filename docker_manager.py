import docker
from docker.models.containers import Container
from models import Backend


class DockerManager:
    def __init__(self):
        self.docker_client = docker.from_env()

    def find_container(self, backend: Backend) -> Container:
        containers = self.docker_client.containers.list(filters={"label": [label.filter for label in backend.match_labels]})
        if containers:
            if len(containers) > 1:
                raise BackendResolutionError("Multiple containers matched filters")
            else:
                return containers[0]
        else:
            raise BackendResolutionError("No containers found for backend")


class BackendResolutionError(Exception):
    pass