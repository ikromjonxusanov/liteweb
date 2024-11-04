from collections import defaultdict


class Request:
    def __init__(self, environment):
        self.queries = defaultdict()

        for key, val in environment.items():
            setattr(self, key.replace(".", "_").lower(), val)
        
        if self.query_string:
            for query in self.query_string.split("&"):
                key, val = query.split("=")
                self.queries[key] = val
