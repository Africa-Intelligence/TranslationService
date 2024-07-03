from src.environment.i_environment import EnvVar, IEnvironment
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

    def get(self, key, environment: IEnvironment):
        builder = self.get_builder(key)
        open_source_key = environment.get_value(EnvVar.OpenSourceAPI.value)
        if isinstance(builder, AdvancedRouterBuilder):
            conditions = [
                self.condition_provider.get(condition, environment) for condition in
                environment.get_value(EnvVar.Conditions.value).split(",")
            ]
            open_source_api = self.api_provider.get(open_source_key, environment)
            closed_source_key = environment.get_value(EnvVar.ClosedSourceAPI.value)
            closed_source_api = self.api_provider.get(closed_source_key, environment)
            return builder(conditions, open_source_api, closed_source_api)
        elif isinstance(builder, BasicRouterBuilder):
            translate_api = self.api_provider.get(open_source_key, environment)
            return builder(translate_api)
        else:
            raise ValueError(key)
