'''
function 'run' and class 'cryptography_ui'
for encrypting strings/files
'''
import tkinter
import ciphers, decorators

encoding = 'utf-8'


@decorators.duration
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


class Args:
    text_data, file_data = None, None
    text_key, file_key = None, None
    cipher = None
    encrypt = None


class text_or_file_ui:
    def set_entry_to_hex(self, entry, is_hex):
        # only if switched to hex
        string = bytes(entry.get(), encoding).hex()
        entry.delete(0, tkinter.END)
        entry.insert(0, string)

    def set_entry_from_hex(self, entry, is_hex):
        # only if switched from hex
        string = entry.get()
        entry.delete(0, tkinter.END)
        try:
            new_string = str(bytes.fromhex(string), encoding)
            virtual_entry = tkinter.Entry()
            virtual_entry.insert(0, new_string)
            self.set_entry_to_hex(virtual_entry, is_hex)
            assert string == virtual_entry.get(), 'Unequal convertion'
            string = new_string
        except Exception as exception:
            is_hex.set(True)
            tkinter.messagebox.showerror('', exception)
        finally:
            entry.insert(0, string)

    def set_to_text(self):
        self.file_button.pack_forget()
        self.file_label.pack_forget()
        self.file_label.configure(text='')
        self.file = None
        self.text_checkbutton.pack(side=tkinter.LEFT, padx=(20, 5))
        self.text_entry.pack(side=tkinter.LEFT)

    def set_to_file(self):
        self.text_entry.pack_forget()
        self.text_checkbutton.pack_forget()
        self.text_entry.delete(0, tkinter.END)
        self.text = None
        self.file_button.pack(side=tkinter.LEFT, padx=30)
        self.file_label.pack(side=tkinter.LEFT)

    def get_text(self):
        string = self.text_entry.get()
        if self.text_is_hex.get():
            self.text = bytes.fromhex(string)
        else:
            self.text = bytes(string, encoding)

    def get_file(self):
        self.file = tkinter.filedialog.askopenfilename()
        self.file_label.configure(text=self.file.split('/')[-1])
        if not self.file:
            self.file = None

    def switch_entry(self):
        if self.text_is_hex.get():
            self.set_entry_to_hex(self.text_entry, self.text_is_hex)
        else:
            self.set_entry_from_hex(self.text_entry, self.text_is_hex)

    def __init__(self, master_frame, label_text):
        frame_top = tkinter.Frame(master_frame)
        frame_bottom = tkinter.Frame(master_frame)
        self.text, self.file = None, None
        tkinter.Label(frame_top, text=label_text, width=5,
                      anchor=tkinter.W).pack(side=tkinter.LEFT,
                                             padx=10,
                                             pady=10)
        self.type = tkinter.IntVar()
        self.text_entry = tkinter.Entry(frame_bottom, width=50)
        self.text_is_hex = tkinter.BooleanVar()
        self.text_checkbutton = tkinter.Checkbutton(frame_bottom,
                                                    text='hex',
                                                    command=self.switch_entry,
                                                    variable=self.text_is_hex)
        self.file_button = tkinter.Button(frame_bottom,
                                          text='Open',
                                          command=self.get_file)
        self.file_label = tkinter.Label(frame_bottom)
        tkinter.Radiobutton(frame_top,
                            text='Text',
                            command=self.set_to_text,
                            variable=self.type,
                            value=1).pack(side=tkinter.LEFT, padx=(0, 5))
        tkinter.Radiobutton(frame_top,
                            text='File',
                            command=self.set_to_file,
                            variable=self.type,
                            value=2).pack(side=tkinter.LEFT, padx=(0, 5))
        frame_top.pack(anchor=tkinter.W)
        frame_bottom.pack(anchor=tkinter.W)

    def get(self):
        if self.type.get() == 1:
            self.get_text()
        return self.text, self.file


class cryptography_ui:
    def cipher_ui(self, master_frame):
        frame = tkinter.Frame(master_frame)
        tkinter.Label(frame, text='Cipher', width=5,
                      anchor=tkinter.W).pack(side=tkinter.LEFT,
                                             padx=10,
                                             pady=10)
        self.combo = tkinter.ttk.Combobox(frame, width=12)
        self.combo['values'] = tuple(ciphers.cipher_dict.keys())
        self.combo.current(0)
        self.combo.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

    def check_args(self):
        self.args.text_data, self.args.file_data = self.data_ui.get()
        self.args.text_key, self.args.file_key = self.key_ui.get()
        self.args.cipher = ciphers.cipher_dict[self.combo.get()]
        if self.args.file_data == None and self.args.text_data == None:
            raise TypeError('Data are not selected')
        if self.args.file_key == None and self.args.text_key == None:
            raise TypeError('Key is not selected')

    def check_data_entry(self):
        if self.data_ui.type.get() == 1:
            self.data_ui.text_entry.delete(0, tkinter.END)
            if not self.data_ui.text_is_hex.get():
                self.data_ui.text_is_hex.set(True)
            self.data_ui.text_entry.insert(0, self.args.text_data.hex())

    @decorators.messagebox
    def launch(self):
        self.check_args()
        duration = run(self.args)
        self.progress_label.configure(text='Time taken: ' + f'{duration:.3f}' +
                                      ' sec')
        self.check_data_entry()

    def encrypt(self):
        self.args.encrypt = True
        self.launch()

    def decrypt(self):
        self.args.encrypt = False
        self.launch()

    def action_ui(self, master_frame):
        frame_top = tkinter.Frame(master_frame)
        frame_bottom = tkinter.Frame(master_frame)
        tkinter.Button(frame_top, text='Encrypt',
                       command=self.encrypt).pack(side=tkinter.LEFT,
                                                  padx=(50, 10),
                                                  pady=10)
        tkinter.Button(frame_top, text='Decrypt',
                       command=self.decrypt).pack(side=tkinter.LEFT)
        self.progress_label = tkinter.Label(frame_bottom)
        self.progress_label.pack(side=tkinter.LEFT)
        frame_top.pack(anchor=tkinter.W)
        frame_bottom.pack(anchor=tkinter.W)

    def __init__(self, master_frame):
        self.args = Args()

        self.data_ui = text_or_file_ui(master_frame, 'Data')
        self.key_ui = text_or_file_ui(master_frame, 'Key')
        self.cipher_ui(master_frame)
        self.action_ui(master_frame)
