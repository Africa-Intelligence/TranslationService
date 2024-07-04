from huggingface_hub import HfApi, REPO_TYPE_DATASET

from src.api.result_uploader.i_result_uploader import IResultUploaderAPI


class HFResultUploaderAPI(IResultUploaderAPI):

    def __init__(self, api_key, repo_id):
        self.api = HfApi(token=api_key)
        self.repo_id = repo_id
        self.CSV_FORMAT = "*.csv"
        # Check if repo exists, otherwise create it
        self.api.create_repo(repo_id=repo_id, repo_type=REPO_TYPE_DATASET, private=True, exist_ok=True)

    def upload_result_file(self, folder_path):
        print(f"\nUploading results in folder {folder_path} to Hugging Face repo: {self.repo_id}")
        self.api.upload_folder(
            create_pr=True,
            folder_path=folder_path,
            repo_id=self.repo_id,
            repo_type=REPO_TYPE_DATASET,
            allow_patterns=self.CSV_FORMAT
        )
