from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import encrypting, os, sys


# str like '***/encryption/'
project_dir = os.path.dirname(os.path.abspath(__file__))[:-3]


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('Encryption')
        self.resizable(width=False, height=False)
        if sys.platform == 'win32':
            self.iconbitmap(project_dir + 'src/graphUI.ico')

        def empty(*args):
            pass

        tabs = {'Encrypting': encrypting.encrypting, 'e': empty}

        self.notebook = Notebook(self, width=320, height=240, padding=10)
        for key, value in tabs.items():
            frame = Frame(self.notebook)
            self.notebook.add(frame, text=key, sticky=NSEW)
            value(frame)
        self.notebook.grid(row=0, column=0)
        self.notebook.enable_traversal()


if __name__ == "__main__":
    app = App()
    app.mainloop()
