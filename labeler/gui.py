import tkinter as tk
from document_handler import DocumentHandler


class LabelingApp:
    def __init__(self, master, document_folder):
        self.master = master
        self.labeled_data = {}
        master.title("Document Labeling Tool")

        fields = [
            ("Vendor Name:", "string"),
            ("Vendor Address:", "string"),
            ("Invoice Number:", "string"),
            ("Order Number:", "string"),
            ("Purchase Order Number:", "string"),
            ("Date (yyyy-MM-dd):", "string"),
            ("Due Date (yyyy-MM-dd):", "string"),
            ("Total in Cents:", "number"),
            ("Credit Card Last Four:", "number")
        ]

        self.entries = {}
        for label_text, _ in fields:
            label = tk.Label(master, text=label_text)
            label.pack()
            entry = tk.Entry(master)
            entry.pack()
            self.entries[label_text] = entry

        self.page_info_label = tk.Label(master, text="")
        self.page_info_label.pack()

        self.next_page_button = tk.Button(
            master, text="Next Page", command=self.next_page
        )
        self.next_page_button.pack()

        self.prev_page_button = tk.Button(
            master, text="Previous Page", command=self.prev_page
        )
        self.prev_page_button.pack()

        self.next_button = tk.Button(
            master, text="Next", command=self.next_document
        )
        self.next_button.pack()

        self.prev_button = tk.Button(
            master, text="Previous", command=self.prev_document
        )
        self.prev_button.pack()

        self.save_button = tk.Button(
            master, text="Save", command=self.save_labeled_data
        )
        self.save_button.pack()

        self.update_button = tk.Button(
            master, text="Update", command=self.update_data
        )
        self.update_button.pack()

        self.document_handler = DocumentHandler(document_folder)
        self.image_label = tk.Label(
            master, image=self.document_handler.get_page_image())
        self.image_label.pack()

        # Update the navigation button functions
        self.next_button['command'] = self.next_document
        self.prev_button['command'] = self.prev_document

    def next_document(self):
        self.document_handler.next_document()
        self.load_labeled_data()
        self.update_image()

    def prev_document(self):
        self.document_handler.prev_document()
        self.load_labeled_data()
        self.update_image()

    def update_image(self):
        image = self.document_handler.get_page_image()
        self.image_label.configure(image=image)
        self.image_label.image = image
        self.update_page_info()

    def update_page_info(self):
        current_page, total_pages = self.document_handler.get_current_page_info()
        self.page_info_label.config(
            text=f"Page {current_page} of {total_pages}"
        )

    def next_page(self):
        self.document_handler.next_page()
        self.update_image()

    def prev_page(self):
        self.document_handler.prev_page()
        self.update_image()

    def save_labeled_data(self):
        self.document_handler.save_labeled_data(self.labeled_data)

    def load_labeled_data(self):
        self.labeled_data = self.document_handler.current_labeled_data


if __name__ == "__main__":
    document_folder = 'path/to/your/documents/folder'
    root = tk.Tk()
    app = LabelingApp(root, document_folder)
    root.mainloop()
