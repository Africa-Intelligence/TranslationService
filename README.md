# TranslationService
This repository is used to generate translations for training data in SFT.

# Prerequisites
The following prerequisites are required in order to run translations:
### 1. **Poetry**:

The dependency manager for this project is [Poetry](https://python-poetry.org/docs/#installation). This will need to be installed in order to manage the dependencies of the project.
```shell
pip3 install poetry 
```

### 2. Python 3.12

Python version 3.12 is used to run the project. One can install multiple versions of python using [pyenv](https://pypi.org/project/pyenv/).
Install pyenv by following the installation [instructions](https://github.com/pyenv/pyenv#installation). 

List current python versions available 

```shell
pyenv install -l
```

Install python 3.12 with pyenv:

```shell
pyenv install 3.12
```

### 3. Ollama

In order to use the ollama router, you must download Ollama from their website (https://ollama.com/)

# Translation Clients
## Azure Translation API
Microsoft Azure [Translation API](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation-overview) is configured to be used as a translation service.
View the current [supported languages](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support) that the API supports.

### How to Use:

The [alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca) dataset is the main dataset that is used for translation.

Clone the repo:

```shell
git clone https://github.com/Llama-Africa/TranslationService.git
```

run the following to install project dependencies:

```shell
poetry install
```

Enter api key in env file for the Azure TranslateText api. Follow [prerequisites](https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-sdk?pivots=programming-language-csharp#prerequisites) to generate api key.
Paste the region and api key in the .env file under `AZURE_TRANSLATE_API_KEY` and `AZURE_TRANSLATE_REGION` respectively.

CD into the src folder and run:
```shell
python main.py
```