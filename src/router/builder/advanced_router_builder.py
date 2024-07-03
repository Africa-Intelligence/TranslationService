from src.factory.i_builder import IBuilder
from src.router.advanced_router import AdvancedRouter


class AdvancedRouterBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, conditions, open_source_api, closed_source_api):
        if not self._instance:
            self._instance = AdvancedRouter(conditions, open_source_api, closed_source_api)
        return self._instance
