import argparse
import tkinter as tk
from gui import Gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR Labeling Tool")
    parser.add_argument("document_folder", help="Path to the document folder")
    parser.add_argument("output_folder", help="Path to the output folder")
    args = parser.parse_args()

    document_folder = args.document_folder
    output_folder = args.output_folder

    root = tk.Tk()
    app = Gui(root, document_folder, output_folder)
    root.mainloop()
