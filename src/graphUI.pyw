from ciphers import cipher_dict
from time import time
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox, Checkbutton
from run import run
import os.path


class Args:
    file_data, text_data = None, None
    file_key, text_key = None, None
    cipher = None
    encrypt = None


def launch_window():
    window = Tk()
    window.resizable(width=False, height=False)
    window.title(__title__)
    window.geometry('400x350')
    return window


def draw_ui(window):
    def set_entry_to_hex(entry, is_hex):
        # only if switched to hex
        string = bytes(entry.get(), encoding).hex()
        entry.delete(0, END)
        entry.insert(0, string)
        
    def set_entry_from_hex(entry, is_hex):
        # only if switched from hex
        string = entry.get()
        entry.delete(0, END)
        try:
            new_string = str(bytes.fromhex(string), encoding)
            virtual_entry = Entry()
            virtual_entry.insert(0, new_string)
            set_entry_to_hex(virtual_entry, is_hex)
            assert string == virtual_entry.get(), 'Unequal convertion'
            string = new_string
        except Exception as exception:
            is_hex.set(True)
            messagebox.showerror(__title__, exception)
        finally:
            entry.insert(0, string)

    # get data
    def set_data_to_text():
        file_data_button.place_forget()
        file_data_label.place_forget()
        file_data_label.configure(text='')
        args.file_data = None
        text_data_entry.place(x=70, y=37)
        text_data_checkbutton.place(x=300, y=35)

    def set_data_to_file():
        text_data_entry.place_forget()
        text_data_checkbutton.place_forget()
        text_data_entry.delete(0, END)
        args.text_data = None
        file_data_button.place(x=70, y=35)
        file_data_label.place(x=120, y=37)

    def get_file_data():
        args.file_data = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
        file_data_label.configure(text=args.file_data.split('/')[-1])

    def get_text_data():
        string = text_data_entry.get()
        if text_data_hex.get():
            args.text_data = bytes.fromhex(string)
        else:
            args.text_data = bytes(string, encoding)

    def switch_data_entry():
        if text_data_hex.get():
            set_entry_to_hex(text_data_entry, text_data_hex)
        else:
            set_entry_from_hex(text_data_entry, text_data_hex)

    Label(window, text='Data: ').place(x=15, y=10)
    data_type = IntVar()
    text_data_entry = Entry(window, width=30)
    text_data_hex = BooleanVar()
    text_data_checkbutton = Checkbutton(window, text='hex', command=switch_data_entry, variable=text_data_hex)
    file_data_button = Button(window, text='Open', command=get_file_data)
    file_data_label = Label(window)
    data_rad1 = Radiobutton(window, text='Text', command=set_data_to_text,
                       variable=data_type, value=1)
    data_rad2 = Radiobutton(window, text='File', command=set_data_to_file,
                       variable=data_type, value=2)
    data_rad1.place(x=70, y=10)
    data_rad2.place(x=120, y=10)
    
    # get key
    def set_key_to_text():
        file_key_button.place_forget()
        file_key_label.place_forget()
        file_key_label.configure(text='')
        args.file_key = None
        text_key_entry.place(x=70, y=107)
        text_key_checkbutton.place(x=300, y=105)

    def set_key_to_file():
        text_key_entry.place_forget()
        text_key_checkbutton.place_forget()
        text_key_entry.delete(0, END)
        args.text_key = None
        file_key_button.place(x=70, y=105)
        file_key_label.place(x=120, y=107)

    def get_file_key():
        args.file_key = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
        file_key_label.configure(text=args.file_key.split('/')[-1])

    def get_text_key():
        string = text_key_entry.get()
        if text_key_hex.get():
            args.text_key = bytes.fromhex(string)
        else:
            args.text_key = bytes(string, encoding)
            
    def switch_key_entry():
        if text_key_hex.get():
            set_entry_to_hex(text_key_entry, text_key_hex)
        else:
            set_entry_from_hex(text_key_entry, text_key_hex)

    Label(window, text='Key: ').place(x=15, y=80)
    key_type = IntVar()
    text_key_entry = Entry(window, width=30)
    text_key_hex = BooleanVar()
    text_key_checkbutton = Checkbutton(window, text='hex', command=switch_key_entry, variable=text_key_hex)
    file_key_button = Button(window, text='Open', command=get_file_key)
    file_key_label = Label(window)
    key_rad1 = Radiobutton(window, text='Text', command=set_key_to_text,
                       variable=key_type, value=1)
    key_rad2 = Radiobutton(window, text='File', command=set_key_to_file,
                       variable=key_type, value=2)
    key_rad1.place(x=70, y=80)
    key_rad2.place(x=120, y=80)

    # select cipher
    Label(window, text='Cipher: ').place(x=15, y=150)
    combo = Combobox(window)
    combo['values'] = tuple(cipher_dict.keys())
    combo.current(0)
    combo.place(x=70, y=152)

    # select action
    def check_args():
        if data_type.get() == 1:
            get_text_data()
        if key_type.get() == 1:
            get_text_key()
        args.cipher = cipher_dict[combo.get()]
        if args.file_data == None and args.text_data == None:
            raise TypeError('Data are not selected')
        if args.file_key == None and args.text_key == None:
            raise TypeError('Key is not selected')

    def check_data_entry():
        if data_type.get() == 1:
            text_data_entry.delete(0, END)
            if not text_data_hex.get():
                text_data_hex.set(True)
            text_data_entry.insert(0, args.text_data.hex())

    def launch():
        try:
            check_args()
            ts = time()
            run(args)
            te = time()
            progress_label.configure(text='Time taken: ' + f'{(te - ts):.3f}' + ' sec')
            check_data_entry()
        except Exception as exception:
            messagebox.showerror(__title__, exception)

    def encrypt():
        args.encrypt = True
        launch()

    def decrypt():
        args.encrypt = False
        launch()

    Button(window, text='Encrypt', command=encrypt).place(x=35, y=250)
    Button(window, text='Decrypt', command=decrypt).place(x=100, y=250)
    progress_label = Label(window)
    progress_label.place(x=30, y=300)


__title__ = 'Encryption'
encoding = 'utf-8'
args = Args()

window = launch_window()
draw_ui(window)
window.mainloop()
