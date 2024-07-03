from src.environment.i_environment import ENV_VARS
from src.factory.condition_provider import ConditionProvider
from src.factory.i_object_factory import IObjectFactory
from src.factory.translate_api_provider import TranslateAPIProvider
from src.router.builder.advanced_router_builder import AdvancedRouterBuilder
from src.router.builder.basic_router_builder import BasicRouterBuilder


class RouterProvider(IObjectFactory):
    def __init__(self, ):
        super().__init__()
        self.register_builder("advanced", AdvancedRouterBuilder())
        self.register_builder("basic", BasicRouterBuilder())
        self.api_provider = TranslateAPIProvider()
        self.condition_provider = ConditionProvider()

    def get(self, key, **kwargs):
        builder = self.get_builder(key)
        if isinstance(AdvancedRouterBuilder, builder):
            open_source_api = self.api_provider.get(ENV_VARS.OPEN_SOURCE_API, **kwargs)
            closed_source_api = self.api_provider.get(ENV_VARS.CLOSED_SOURCE_API, **kwargs)
            conditions = [
                self.condition_provider.get(env_var, **kwargs) for env_var in
                ENV_VARS.CONDITIONS.value.split(",")
            ]
            return builder(open_source_api, closed_source_api, conditions, **kwargs)
        elif isinstance(BasicRouterBuilder, builder):
            translate_api = self.api_provider.get(ENV_VARS.OPEN_SOURCE_API, **kwargs)
            return builder(translate_api, **kwargs)
        else:
            raise ValueError(key)
