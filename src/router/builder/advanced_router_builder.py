from src.factory.condition_provider import ConditionProvider
from src.router.advanced_router import AdvancedRouter


class AdvancedRouterBuilder(object):
    def __init__(self):
        self._instance = None

    def __call__(self, condition, open_source_api, closed_source_api, **kwargs):
        if not self._instance:
            code_condition = ConditionProvider.get("code", )
            self._instance = AdvancedRouter(condition, open_source_api, closed_source_api)
        return self._instance
