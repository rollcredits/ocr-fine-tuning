# OCR Document Labeling Tool

## Description
This is a Python script with a GUI for labeling OCR documents to train machine learning models.

## Installation

### Requirements
- Python 3.8 or higher


#### Installing Pipenv (macOS)
If you don't have Pipenv installed, you can install it using Homebrew:
```bash
brew install pipenv
```
Or you can install it using pip:
```bash
pip install pipenv
```

#### Installing Pipenv (macOS)
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

## Usage
Run the script by providing the path to the folder containing the documents as a command-line argument:
```bash
python ./labeler/main.py path/to/your/documents/folder
