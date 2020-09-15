from typing import List


class MatchLabel:
    def __init__(self, filter: str):
        self.filter = filter

    def __str__(self):
        return "MatchLabel(\"{}\")".format(self.filter)

    def to_tuple(self):
        key_value = self.filter.split("=")
        return (key_value[0], key_value[1])


class Backend:
    def __init__(self, name: str, match_labels: List[MatchLabel]):
        self.name = name
        self.match_labels = match_labels

    def __str__(self):
        return "Backend(name=\"{}\", match_labels={}".format(self.name, [l.filter for l in self.match_labels])


class Route:
    def __init__(self, path_prefix: str, backend: Backend):
        self.path_prefix = path_prefix
        self.backend = backend

    def __str__(self):
        return "Route(path_prefix=\"{}\", backend={}".format(self.path_prefix, self.backend)


class DefaultResponse:
    def __init__(self, body: str, status_code: int):
        self.body = body
        self.status_code = status_code