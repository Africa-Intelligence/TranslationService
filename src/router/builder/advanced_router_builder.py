from src.factory.condition_provider import ConditionProvider
from src.router.advanced_router import AdvancedRouter


class AdvancedRouterBuilder(object):
    def __init__(self):
        self._instance: AdvancedRouter|None = None
        self.open_source_api = None
        self.closed_source_api = None
        self.condition = None

    def __call__(self, open_source_api, closed_source_api, condition, **kwargs):
        if not self._instance:
            self._instance = AdvancedRouter(self.open_source_api, closed_source_api, condition)
        return self._instance
