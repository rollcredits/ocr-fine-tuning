import fitz
from PIL import Image, ImageTk
import os
import json


class DocumentHandler:
    def __init__(self, document_folder):
        self.current_page = 0
        self.current_index = 0
        self.document_paths = [
            os.path.join(document_folder, f) for f in os.listdir(document_folder)
        ]
        self.load_document(self.current_index)

    def load_document(self, index):
        # Load a specific document by its index in the list
        self.current_index = index
        document_path = self.document_paths[index]
        self.doc_extension = os.path.splitext(document_path)[1].lower()
        self.current_labeled_data = self.load_labeled_data()

        if self.doc_extension == '.pdf':
            self.doc = fitz.open(document_path)
        else:
            self.doc = Image.open(document_path)
        self.total_pages = len(self.doc) if self.doc_extension == '.pdf' else 1

    def next_document(self):
        if self.current_index < len(self.document_paths) - 1:
            self.load_document(self.current_index + 1)
            self.current_page = 0

    def prev_document(self):
        if self.current_index > 0:
            self.load_document(self.current_index - 1)
            self.current_page = 0

    def get_page_image(self):
        if self.doc_extension == '.pdf':
            pix = self.doc.load_page(self.current_page).get_pixmap()
            image = Image.frombytes(
                "RGB", [pix.width, pix.height], pix.samples)
        else:
            image = self.doc
        return ImageTk.PhotoImage(image)

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
        with open(json_file_path, 'w') as f:
            json.dump(labeled_data, f)

    def load_labeled_data(self):
        json_file_path = self.get_json_path()
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                return json.load(f)
        return {}

    def get_json_path(self):
        # Replace the document's extension with .json
        return os.path.splitext(self.document_paths[self.current_index])[0] + '.json'
