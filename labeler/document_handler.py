from pdf2image import convert_from_path
from PIL import Image, ImageTk
import os
import json

VALID_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg']

class DocumentHandler:
    def __init__(self, document_folder, output_folder):
        self.output_folder = output_folder
        self.current_page = 0
        self.current_index = 0
        self.document_paths = [
            os.path.join(document_folder, f) for f in os.listdir(document_folder)
        ]
        self.document_paths = list(filter(
            lambda f: os.path.splitext(f)[1].lower() in VALID_EXTENSIONS,
            self.document_paths
        ))
        self.document_paths.sort()
        self.load_document(self.current_index)

    def load_document(self, index):
        # Load a specific document by its index in the list
        self.current_index = index
        document_path = self.document_paths[index]
        self.doc_extension = os.path.splitext(document_path)[1].lower()
        self.current_labeled_data = self.load_labeled_data()

        if self.doc_extension == '.pdf':
            self.doc = convert_from_path(document_path)
        else:
            self.doc = [Image.open(document_path)]
        self.total_pages = len(self.doc)

    def next_document(self):
        if self.current_index < len(self.document_paths) - 1:
            self.load_document(self.current_index + 1)
            self.current_page = 0

    def prev_document(self):
        if self.current_index > 0:
            self.load_document(self.current_index - 1)
            self.current_page = 0

    def get_page_image(self):
        return self.doc[self.current_page]

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1

    def get_current_page_info(self):
        return self.current_page, self.total_pages

    def save_labeled_data(self, labeled_data):
        json_file_path = self.get_json_path()
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        with open(json_file_path, 'w') as f:
            json.dump(labeled_data, f)

    def load_labeled_data(self):
        json_file_path = self.get_json_path()
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                return json.load(f)
        return {}

    def get_json_path(self):
        filename = os.path.basename(os.path.splitext(self.document_paths[self.current_index])[0]) + '.json'
        return os.path.join(self.output_folder, filename)
