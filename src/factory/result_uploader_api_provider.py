from src.api.result_uploader.builder.hf_result_uploader_api_builder import HFResultUploaderAPIBuilder
from src.factory.i_object_factory import IObjectFactory


class ResultUploaderAPIProvider(IObjectFactory):
    def __init__(self):
        super().__init__()
        self.register_builder("hf_result_uploader_api", HFResultUploaderAPIBuilder())
