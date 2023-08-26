import argparse
import tkinter as tk
from gui import Gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR Labeling Tool")
    parser.add_argument("folder", help="Path to the document folder")
    args = parser.parse_args()

    document_folder = args.folder

    root = tk.Tk()
    app = Gui(root, document_folder)
    root.mainloop()
