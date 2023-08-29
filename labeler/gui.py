import tkinter as tk
from document_handler import DocumentHandler
from PIL import ImageTk
from fields import fields


class Gui:
    def __init__(self, master, document_folder, output_folder):
        self.master = master
        self.labeled_data = {}
        master.title("Document Labeling Tool")
        master.bind('<Prior>', self.prev_page)    # Page Up
        master.bind('<Next>', self.next_page)     # Page Down
        master.bind('<Up>', self.prev_document)   # Up Arrow
        master.bind('<Down>', self.next_document) # Down Arrow

        self.vars = {}

        self.entries = {}
        row = 0
        for field in fields:
            label = tk.Label(master, text=field["label"])
            label.grid(row=row, column=0)

            if field["type"] == "number":
                var = tk.IntVar()
            else:
                var = tk.StringVar()
            var.trace_add("write", lambda name, index, mode, sv=var: self.autosave(sv))
            self.vars[field["key"]] = var

            entry = tk.Entry(master, textvariable=self.vars[field["key"]])
            entry.grid(row=row, column=1)
            self.entries[field["key"]] = entry

            row += 1

        self.document_handler = DocumentHandler(document_folder, output_folder)
        self.image_label = tk.Label(master)
        self.image_label.grid(row=0, column=2, rowspan=row, columnspan=2)

        self.page_info_label = tk.Label(master, text="")
        self.page_info_label.grid(row=row, column=2, columnspan=2)

        row += 1

        self.prev_page_button = tk.Button(
            master, text="Previous Page", command=self.prev_page
        )
        self.prev_page_button.grid(row=row, column=2)

        self.next_page_button = tk.Button(
            master, text="Next Page", command=self.next_page
        )
        self.next_page_button.grid(row=row, column=3)

        row += 1

        self.prev_button = tk.Button(
            master, text="Previous", command=self.prev_document
        )
        self.prev_button.grid(row=row, column=0)

        self.next_button = tk.Button(
            master, text="Next", command=self.next_document
        )
        self.next_button.grid(row=row, column=1)

        row += 1

        # Update the navigation button functions
        self.next_button['command'] = self.next_document
        self.prev_button['command'] = self.prev_document

        self.load_document()

    def load_document(self):
        self.load_labeled_data()
        self.update_image()
        self.focus_first_input()

    def next_document(self, event=None):
        self.document_handler.next_document()
        self.load_document()

    def prev_document(self, event=None):
        self.document_handler.prev_document()
        self.load_document()

    def update_image(self):
        img = self.document_handler.get_page_image()
    
        # Get current dimensions
        base_height = img.height
        base_width = img.width
        
        # Define max dimensions
        max_height = 900
        max_width = 1000

        # Calculate new dimensions
        if base_height > max_height or base_width > max_width:
            aspect_ratio = base_width / base_height
            if base_height > max_height:
                new_height = max_height
                new_width = int(new_height * aspect_ratio)
            else:
                new_width = max_width
                new_height = int(new_width / aspect_ratio)
            
            # Resize image
            img = img.resize((new_width, new_height))

        # Convert and display
        image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=image)
        self.image_label.image = image
        self.update_page_info()

    def update_page_info(self):
        current_page, total_pages = self.document_handler.get_current_page_info()
        self.page_info_label.config(
            text=f"Page {current_page + 1} of {total_pages}"
        )

    def focus_first_input(self):
        list(self.entries.values())[0].focus_set()

    def next_page(self, event=None):
        self.document_handler.next_page()
        self.update_image()

    def prev_page(self, event=None):
        self.document_handler.prev_page()
        self.update_image()

    def autosave(self, var):
        for field, sv in self.vars.items():
            if sv == var:
                val = var.get()
                self.labeled_data[field] = val if val != "" else None
                self.document_handler.save_labeled_data(self.labeled_data)
                break

    def load_labeled_data(self):
        self.labeled_data = self.document_handler.current_labeled_data
        for field, var in self.vars.items():
            print(field, var)
            val = self.labeled_data.get(field, "")
            var.set(val if val is not None else "")
