from response import Response
from parse import parse
import types
import inspect 


SUPPORTED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

class LiteWeb:
    def __init__(self, middlewares = []) -> None:
        self.routes = dict()
        self.middlewares = middlewares
        self.middlewares_for_routes = dict()

    def __call__(self, environ, start_response):
        response = Response()
        
        for middleware in self.middlewares:
            if isinstance(middleware, types.FunctionType):
                middleware(environ)
            else:
                raise ValueError("Middleware have to be a function")
            
        for path, handler_dict in self.routes.items():
            res = parse(path, environ["PATH_INFO"])
            for request_method, handler in handler_dict.items():
                if environ["REQUEST_METHOD"] == request_method and res:
                    route_middlewares = self.middlewares_for_routes[path][request_method]
                    
                    for middleware in route_middlewares:
                        if isinstance(middleware, types.FunctionType):
                            middleware(environ)
                        else:
                            raise ValueError("Middleware have to be a function")
                    
                    handler(environ, response, **res.named)
                    response.as_wsgi(start_response)
                    return [response.text.encode()]
                
        return response.as_wsgi(start_response)
    
    def route_common(self, path, handler, method_name, middlewares):
        path_name=path or "/{heander.__name__}"
        
        if path_name not in self.routes:
            self.routes[path_name] = {}
        
        self.routes[path_name][method_name] = handler
        
        if path_name not in self.middlewares_for_routes:
            self.middlewares_for_routes[path_name] = {}

        self.middlewares_for_routes[path_name][method_name] = middlewares
        
        return handler
    
    def get(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "GET", middlewares)

        return wrapper
    
    def post(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "POST", middlewares)

        return wrapper
    
    def put(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "PUT", middlewares)

        return wrapper
    
    def patch(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "PATCH", middlewares)

        return wrapper

    def delete(self, path=None, middlewares=[]):
        def wrapper(handler):
            return self.route_common(path, handler, "DELETE", middlewares)

        return wrapper

    def route(self, path=None, middlewares=[]):
        def wrapper(handler):
            if not isinstance(handler, type):
                raise ValueError("Handler have to be a class")
            class_members = inspect.getmembers(handler, lambda x: inspect.isfunction(x) and not (
                x.__name__.startswith("__") or x.__name__.endswith("__")
            ) and x.__name__.upper() in SUPPORTED_METHODS)
            for method_name, handler in class_members:
                self.route_common(path or f"/{handler.__name__}", handler, method_name.upper(), middlewares)
        return wrapper

