import tkinter, tkinter.ttk
from PIL import ImageTk, Image
import cryptography, steganography
from functions import *


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title('Encryption')
        self.resizable(width=False, height=False)
        if platform() == 'win32':
            self.iconbitmap(project_dir() + 'icons/graphUI.ico')

        def empty(*args):
            pass

        tabs = {
            'Cryptography': cryptography.cryptography_ui,
            'Steganography': steganography.steganography_ui
        }

        self.notebook = tkinter.ttk.Notebook(self,
                                             width=400,
                                             height=240,
                                             padding=10)
        for key, value in tabs.items():
            frame = tkinter.Frame(self.notebook)
            self.notebook.add(frame, text=key, sticky=tkinter.NSEW)
            value(frame)
        self.notebook.grid(row=0, column=0)
        self.notebook.enable_traversal()


if __name__ == "__main__":
    app = App()
    app.mainloop()
