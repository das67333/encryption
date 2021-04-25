from ciphers import cipher_dict
from time import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
from overwrite_file import overwrite_file
import os.path

__title__ = 'Encryption'
window = Tk()
window.title(__title__)
window.geometry('320x180')

class Args:
    file = None
    key = None
    cipher = None
    encrypt = None

args = Args()

def draw_ui(window):
    frames = [Frame(window) for i in range(5)]

    # get file
    Label(frames[0], text='Open file: ').pack(side=LEFT)
    file_name = Label(frames[0])

    def open_file_dialog():
        args.file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
        file_name.configure(text=args.file.split('/')[-1])
        file_name.pack(side=LEFT)

    Button(frames[0], text='Open', command=open_file_dialog).pack(side=LEFT)
    
    # get key
    def set_to_text():
        file_button.pack_forget()
        file_label.pack_forget()
        text_entry.pack(side=LEFT)

    def set_to_file():
        text_entry.pack_forget()
        file_button.pack(side=LEFT)
        file_label.pack(side=LEFT)

    def set_file_key():
        file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
        file_label.configure(text=file.split('/')[-1])
        with open(file, 'rb') as File:
            args.key = File.read()

    def set_text_key():
        args.key = bytes(text_entry.get(), encoding='utf-8')

    Label(frames[1], text='Key: ').pack(side=LEFT)
    key_type = IntVar()
    text_entry = Entry(frames[1], width=20)
    file_button = Button(frames[1], text='Open', command=set_file_key)
    file_label = Label(frames[1])

    rad1 = Radiobutton(frames[1], text='Text', command=set_to_text,
                       variable=key_type, value=1)
    rad2 = Radiobutton(frames[1], text='File', command=set_to_file,
                       variable=key_type, value=2)
    rad1.pack(side=LEFT)
    rad2.pack(side=LEFT)

    # select cipher
    Label(frames[2], text='Cipher: ').pack(side=LEFT)
    combo = Combobox(frames[2])
    combo['values'] = tuple(cipher_dict.keys())
    combo.current(0)
    combo.pack(side=LEFT)

    # select action
    def check_args():
        if key_type.get() == 1:
            set_text_key()
        args.cipher = cipher_dict[combo.get()]
        if args.file == None:
            raise FileNotFoundError('File is not selected')
        if args.key == None:
            raise FileNotFoundError('Key is not selected')

    def launch():
        try:
            check_args()
            progress_label.configure(text='Please wait...')
            ts = time()
            overwrite_file(args)
            te = time()
            progress_label.configure(text='Time taken: ' + f'{(te - ts):.3f}' + ' sec')
        except Exception as exception:
            messagebox.showerror(__title__, exception)

    def encrypt():
        args.encrypt = True
        launch()

    def decrypt():
        args.encrypt = False
        launch()

    Button(frames[3], text='Encrypt', command=encrypt).pack(side=LEFT)
    Button(frames[3], text='Decrypt', command=decrypt).pack(side=LEFT)
    progress_label = Label(frames[4])
    progress_label.pack(side=LEFT)

    for frame in frames:
        frame.pack(fill=X)

draw_ui(window)

window.mainloop()

