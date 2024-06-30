from src.factory.i_object_factory import IObjectFactory
from src.router.builder.advanced_router_builder import AdvancedRouterBuilder
from src.router.builder.basic_router_builder import BasicRouterBuilder


class RouterProvider(IObjectFactory):
    def __init__(self, ):
        super().__init__()
        self.register_builder("advanced", AdvancedRouterBuilder())
        self.register_builder("basic", BasicRouterBuilder())
