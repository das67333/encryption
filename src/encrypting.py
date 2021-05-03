'''
defines project_dir
run(args) cipher methods with no data loss in case of exceptions
'''
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
import ciphers, time


class Args:
    file_data, text_data = None, None
    file_key, text_key = None, None
    cipher = None
    encrypt = None


def run(args):
    if args.file_data:
        with open(args.file_data, 'rb') as File:
            data = File.read()
    else:
        data = args.text_data
    if args.file_key:
        with open(args.file_key, 'rb') as File:
            key = File.read()
    else:
        key = args.text_key
    name = 'encrypt' if args.encrypt else 'decrypt'
    try:
        data = getattr(args.cipher, name)(data, key)
    except:
        raise
    finally:
        if args.file_data:
            with open(args.file_data, 'wb') as File:
                File.write(data)
        else:
            args.text_data = data


class encrypting:
    def set_entry_to_hex(self, entry, is_hex):
        # only if switched to hex
        string = bytes(entry.get(), self.encoding).hex()
        entry.delete(0, END)
        entry.insert(0, string)

    def set_entry_from_hex(self, entry, is_hex):
        # only if switched from hex
        string = entry.get()
        entry.delete(0, END)
        try:
            new_string = str(bytes.fromhex(string), self.encoding)
            virtual_entry = Entry()
            virtual_entry.insert(0, new_string)
            self.set_entry_to_hex(virtual_entry, is_hex)
            assert string == virtual_entry.get(), 'Unequal convertion'
            string = new_string
        except Exception as exception:
            is_hex.set(True)
            messagebox.showerror('', exception)
        finally:
            entry.insert(0, string)

    def set_data_to_text(self):
        self.file_data_button.grid_forget()
        self.file_data_label.grid_forget()
        self.file_data_label.configure(text='')
        self.args.file_data = None
        self.text_data_entry.grid(row=1, column=1, columnspan=3)
        self.text_data_checkbutton.grid(row=0, column=3)

    def set_data_to_file(self):
        self.text_data_entry.grid_forget()
        self.text_data_checkbutton.grid_forget()
        self.text_data_entry.delete(0, END)
        self.args.text_data = None
        self.file_data_button.grid(row=1, column=1)
        self.file_data_label.grid(row=1, column=2)

    def get_file_data(self):
        self.args.file_data = filedialog.askopenfilename()
        self.file_data_label.configure(text=self.args.file_data.split('/')[-1])

    def get_text_data(self):
        string = self.text_data_entry.get()
        if self.text_data_hex.get():
            self.args.text_data = bytes.fromhex(string)
        else:
            self.args.text_data = bytes(string, self.encoding)

    def switch_data_entry(self):
        if self.text_data_hex.get():
            self.set_entry_to_hex(self.text_data_entry, self.text_data_hex)
        else:
            self.set_entry_from_hex(self.text_data_entry, self.text_data_hex)

    def data_ui(self, frame):
        Label(frame, text='Data: ').grid(row=0,
                                         column=0,
                                         sticky=W,
                                         padx=20,
                                         pady=10)
        self.data_type = IntVar()
        self.text_data_entry = Entry(frame, width=30)
        self.text_data_hex = BooleanVar()
        self.text_data_checkbutton = Checkbutton(
            frame,
            text='hex',
            command=self.switch_data_entry,
            variable=self.text_data_hex)
        self.file_data_button = Button(frame,
                                       text='Open',
                                       command=self.get_file_data)
        self.file_data_label = Label(frame)
        Radiobutton(frame,
                    text='Text',
                    command=self.set_data_to_text,
                    variable=self.data_type,
                    value=1).grid(row=0, column=1)
        Radiobutton(frame,
                    text='File',
                    command=self.set_data_to_file,
                    variable=self.data_type,
                    value=2).grid(row=0, column=2)

    def set_key_to_text(self):
        self.file_key_button.grid_forget()
        self.file_key_label.grid_forget()
        self.file_key_label.configure(text='')
        self.args.file_key = None
        self.text_key_entry.grid(row=3, column=1, columnspan=3)
        self.text_key_checkbutton.grid(row=2, column=3)

    def set_key_to_file(self):
        self.text_key_entry.grid_forget()
        self.text_key_checkbutton.grid_forget()
        self.text_key_entry.delete(0, END)
        self.args.text_key = None
        self.file_key_button.grid(row=3, column=1)
        self.file_key_label.grid(row=3, column=2)

    def get_file_key(self):
        self.args.file_key = filedialog.askopenfilename()
        self.file_key_label.configure(text=self.args.file_key.split('/')[-1])

    def get_text_key(self):
        string = self.text_key_entry.get()
        if self.text_key_hex.get():
            self.args.text_key = bytes.fromhex(string)
        else:
            self.args.text_key = bytes(string, self.encoding)

    def switch_key_entry(self):
        if self.text_key_hex.get():
            self.set_entry_to_hex(self.text_key_entry, self.text_key_hex)
        else:
            self.set_entry_from_hex(self.text_key_entry, self.text_key_hex)

    def key_ui(self, frame):
        Label(frame, text='Key: ').grid(row=2,
                                        column=0,
                                        sticky=W,
                                        padx=20,
                                        pady=10)
        self.key_type = IntVar()
        self.text_key_entry = Entry(frame, width=30)
        self.text_key_hex = BooleanVar()
        self.text_key_checkbutton = Checkbutton(frame,
                                                text='hex',
                                                command=self.switch_key_entry,
                                                variable=self.text_key_hex)
        self.file_key_button = Button(frame,
                                      text='Open',
                                      command=self.get_file_key)
        self.file_key_label = Label(frame)
        Radiobutton(frame,
                    text='Text',
                    command=self.set_key_to_text,
                    variable=self.key_type,
                    value=1).grid(row=2, column=1)
        Radiobutton(frame,
                    text='File',
                    command=self.set_key_to_file,
                    variable=self.key_type,
                    value=2).grid(row=2, column=2)

    def cipher_ui(self, frame):
        Label(frame, text='Cipher: ').grid(row=4,
                                           column=0,
                                           sticky=W,
                                           padx=20,
                                           pady=10)
        self.combo = Combobox(frame)
        self.combo['values'] = tuple(ciphers.cipher_dict.keys())
        self.combo.current(0)
        self.combo.grid(row=4, column=1, columnspan=2)

    def check_args(self):
        if self.data_type.get() == 1:
            self.get_text_data()
        if self.key_type.get() == 1:
            self.get_text_key()
        self.args.cipher = ciphers.cipher_dict[self.combo.get()]
        if self.args.file_data == None and self.args.text_data == None:
            raise TypeError('Data are not selected')
        if self.args.file_key == None and self.args.text_key == None:
            raise TypeError('Key is not selected')

    def check_data_entry(self):
        if self.data_type.get() == 1:
            self.text_data_entry.delete(0, END)
            if not self.text_data_hex.get():
                self.text_data_hex.set(True)
            self.text_data_entry.insert(0, self.args.text_data.hex())

    def launch(self):
        try:
            self.check_args()
            ts = time.time()
            run(self.args)
            te = time.time()
            self.progress_label.configure(text='Time taken: ' +
                                          f'{(te - ts):.3f}' + ' sec')
            self.check_data_entry()
        except Exception as exception:
            messagebox.showerror('', exception)

    def encrypt(self):
        self.args.encrypt = True
        self.launch()

    def decrypt(self):
        self.args.encrypt = False
        self.launch()

    def action_ui(self, frame):
        Button(frame, text='Encrypt', command=self.encrypt).grid(row=5,
                                                            column=1,
                                                            pady=10)
        Button(frame, text='Decrypt', command=self.decrypt).grid(row=5,
                                                            column=2,
                                                            pady=10)
        self.progress_label = Label(frame)
        self.progress_label.grid(row=6, column=1, columnspan=2, sticky=W)

    def __init__(self, frame):
        self.encoding = 'utf-8'
        self.args = Args()

        self.data_ui(frame)
        self.key_ui(frame)
        self.cipher_ui(frame)
        self.action_ui(frame)
