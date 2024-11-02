class LiteWeb:
    def __init__(self) -> None:
        pass

    def __call__(self, environ, start_response):
        start_response("200 OK", headers=[])
        return [b"Hello, World"]

liteweb = LiteWeb()

