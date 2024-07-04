from src.api.result_uploader.hf_result_uploader_api import HFResultUploaderAPI
from src.environment.i_environment import IEnvironment, EnvVar
from src.factory.i_builder import IBuilder


class HFResultUploaderAPIBuilder(IBuilder):
    def __init__(self):
        super().__init__()

    def __call__(self, env: IEnvironment):
        if not self._instance:
            api_key = env.get_value(EnvVar.HFAPIKey.value)
            repo_id = env.get_value(EnvVar.HFRepoId.value)
            self._instance = HFResultUploaderAPI(api_key, repo_id)
        return self._instance
