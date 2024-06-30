from src.router.basic_router import BasicRouter


class BasicRouterBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, translate_api, **kwargs):
        if not self._instance:
            self._instance = BasicRouter(translate_api)
        return self._instance
