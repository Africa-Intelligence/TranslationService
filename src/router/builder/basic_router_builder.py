from src.factory.i_builder import IBuilder
from src.router.basic_router import BasicRouter


class BasicRouterBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, translate_api):
        if not self._instance:
            self._instance = BasicRouter(translate_api)
        return self._instance
