# OCR Document & Image Labeling Tool

## Description
This repo contains a set of python scripts to make it easier to enable labeling OCR documents and images to train a fine-tuned OpenAI model. It includes a GUI-based tool for labeling and helper scripts to submit labels and prompts for fine-tuning to the OpenAI API.

## Installation

### Requirements
- Python 3.8 or higher


### Installing Dependencies (macOS)
If you don't have Pipenv installed, you can install it using Homebrew:
```bash
brew install pipenv
```
Or you can install it using pip:
```bash
pip install pipenv
```

Poppler is required for PDF to image conversion. You can install it using Homebrew:
```bash
brew install poppler
```

### Steps
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies using pipenv:
```bash
pipenv install
```
4. Activate the virtual environment:
```bash
pipenv shell
```
5. Copy the `.env.sample` to a `.env` file:
```bash
cp .env.sample .env
```
6. Populate the .env file with your OpenAI API key. For organization ID(s), if you are training a model across multiple organizations, you can provide multiple IDs separated by commas. Additionally, tweak any parameters you may care about (# of training epochs, model to train, etc).
7. Copy the `fields.json.sample` to a `fields.json` file:
```bash
cp fields.json.sample fields.json
```
8. Tweak the fields.json to reflect the fields that you want your OpenAI model to return.
    1. The `key` will be what the OpenAI model is trained to return.
    2. The `label` is what will be displayed to the human user above the input field when using the labeling GUI.
    3. The `type` will be used to constrain the input field. Current options are `string` or `number`.

## Usage

### Labeling Documents & Images
To run the labeling app, provide the following command line arguments:
1. The path to the folder containing the documents & images to be labeled, and
2. The output folder for the labeled data.
```bash
python ./labeler/main.py path/to/your/documents/folder path/to/your/output/folder
```

Files to be labeled must end with one of the following extensions:
```
.pdf, .png, .jpg, .jpeg
```

When labeling, keyboard navigation can be used.
1. Page Up & Page Down navigate to the previous and next page of the current document for multipage PDF documents.
2. Arrow Up and Arrow Down navigate to the previous and next file to label.

Output data will be saved to the specified output folder. Labels for each file will be saved with the same file name as the original file, but with the .json extension. For example, an input file with the filename `my-document.pdf` will have labels saved under the name `my-document.json`.

Data is autosaved as you type, and if you close and reopen the GUI tool later then existing labels you have created will be loaded up for each file as long as you specify the same output folder. If you add new fields to your `fields.json`, then you can go back through your files and add labels for just that field!

### Submitting Labels for Fine-Tuning
Submit labels and prompts to OpenAI to create a fine-tuned model by providing the following as command line arguments:
1. The path to the output folder that you used when running the labeling app, and
2. The path to your prompts folder.
```bash
python ./openai-submit/main.py path/to/your/output/folder path/to/your/prompts/folder
```

Prompts must be .txt files with filenames matching the document/labeled filename. For example, if your original input file had the filename `my-document.pdf`, your labels for that file will have the filename `my-document.json`, and your prompt should have the filename `my-document.txt`.

When running the script, you will have a chance to review the generated training data and test data before it is submitted to the OpenAI API. The generated data will be available in `training_data.jsonl` and `test_data.jsonl`.

You can check on the status of the fine-tuning job by running the check-status script. This can take upwards of an hour depending on the amount of training data.
```bash
python ./openai-submit/check-status.py
```