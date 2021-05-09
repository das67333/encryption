'''
function 'run' and class 'steganography_ui'
for concealing strings/files
'''
import io, requests, tkinter, tkinter.filedialog, tkinter.messagebox
from PIL import ImageTk, Image
import decorators
from functions import *

encoding = 'utf-8'


@decorators.messagebox
def show(image):
    if not image:
        return
    global img  # just necessary for viewing imaging
    img = ImageTk.PhotoImage(image)
    top = tkinter.Toplevel()
    top.title('Viewer')
    top.resizable(width=False, height=False)
    if platform() == 'win32':
        top.iconbitmap(project_dir() + 'icons/viewer.ico')
    tkinter.Label(top, image=img).pack(side=tkinter.LEFT)


class link_or_file_ui:
    def set_to_link(self):
        self.object = None
        self.file_button.pack_forget()
        self.file_label.pack_forget()
        self.file_label.configure(text='')
        self.link_button.pack(side=tkinter.LEFT, padx=18)
        self.link_entry.pack(side=tkinter.LEFT)

    def set_to_file(self):
        self.object = None
        self.link_entry.pack_forget()
        self.link_entry.delete(0, tkinter.END)
        self.link_button.pack_forget()
        self.file_button.pack(side=tkinter.LEFT, padx=18)
        self.file_label.pack(side=tkinter.LEFT)

    @decorators.messagebox
    def get_by_link(self):
        self.object = requests.get(self.link_entry.get()).content

    def get_file(self):
        file = tkinter.filedialog.askopenfilename()
        self.file_label.configure(text=file.split('/')[-1])
        if file:
            with open(file, 'rb') as File:
                self.object = File.read()

    def __init__(self, master_frame, label_text):
        frame_top = tkinter.Frame(master_frame)
        frame_bottom = tkinter.Frame(master_frame)
        self.object = None
        self.object_type = label_text
        tkinter.Label(frame_top, text=label_text).pack(side=tkinter.LEFT,
                                                       padx=10,
                                                       pady=5)
        self.type = tkinter.IntVar()
        self.link_entry = tkinter.Entry(frame_bottom, width=50)
        self.link_button = tkinter.Button(frame_bottom,
                                          text='Load',
                                          command=self.get_by_link)
        self.file_button = tkinter.Button(frame_bottom,
                                          text='Open',
                                          command=self.get_file)
        self.file_label = tkinter.Label(frame_bottom)
        tkinter.Radiobutton(frame_top,
                            text='Link',
                            command=self.set_to_link,
                            variable=self.type,
                            value=1).pack(side=tkinter.LEFT, padx=(0, 5))
        tkinter.Radiobutton(frame_top,
                            text='File',
                            command=self.set_to_file,
                            variable=self.type,
                            value=2).pack(side=tkinter.LEFT, padx=(0, 5))

        @decorators.messagebox
        def check():
            if self.get():
                show(Image.open(io.BytesIO(self.object)))

        tkinter.Button(frame_top, text='Show',
                       command=check).pack(side=tkinter.LEFT)
        frame_top.pack(anchor=tkinter.W)
        frame_bottom.pack(anchor=tkinter.W)

    @decorators.messagebox
    def get(self):
        if not self.object:
            raise AttributeError(self.object_type + ' is not selected')
        return self.object


class concealing_ui:
    @decorators.messagebox
    def edit_image(self):
        if not self.original.get():
            return
        text = bytes(self.entry.get(), encoding)
        # make list of bits
        text = list((x >> i) & 1 for x in text for i in range(8))

        with Image.open(io.BytesIO(self.original.get())) as image:
            assert image.size[0] * image.size[1] > len(
                text) * 8, 'Image is not big enough'
            pixels = image.load()
            for i, v in enumerate(text):
                index = i // image.size[1], i % image.size[1]
                pixel = pixels[index]
                blue = pixel[2]
                if v == 1:
                    blue += 1
                if blue == 256:
                    blue = 254
                pixels[index] = (pixel[0], pixel[1], blue)
            return image

    def save_image(self):
        if not self.original.get():
            return
        path = tkinter.filedialog.asksaveasfilename(filetypes=[('BMP files',
                                                                '*.bmp')])
        if path:
            self.edit_image().save(path)

    def __init__(self, master_frame, entry, original):
        self.entry = entry
        self.original = original
        frame = tkinter.LabelFrame(master_frame, text='Conceal')

        tkinter.Label(frame, text='Edited image').pack(side=tkinter.LEFT,
                                                       padx=10)
        tkinter.Button(frame, text='Save',
                       command=self.save_image).pack(side=tkinter.LEFT,
                                                     padx=10)
        tkinter.Button(frame,
                       text='Show',
                       command=lambda: show(self.edit_image())).pack(
                           side=tkinter.LEFT, padx=20)

        frame.pack(anchor=tkinter.W, fill=tkinter.X, padx=10, pady=5, ipady=10)


class revealing_ui:
    @decorators.messagebox
    def get_bmp(self):
        self.image = tkinter.filedialog.askopenfilename(
            filetypes=[('BMP files', '*.bmp')])
        self.label.configure(text=self.image.split('/')[-1])

    @decorators.messagebox
    def find_message(self):
        if not self.original.get():
            return
        if not self.image:
            raise AttributeError('Edited image is not selected')
        image1, image2 = Image.open(io.BytesIO(
            self.original.get())), Image.open(self.image)
        assert image1.size == image2.size, 'Images are of different sizes'
        self.entry.delete(0, tkinter.END)
        pixels1 = image1.load()
        pixels2 = image2.load()
        bits, text = [], []
        for i in range(image1.size[0] * image1.size[1]):
            index = i // image1.size[1], i % image1.size[1]
            bits.append(abs(pixels1[index][2] - pixels2[index][2]))
            if len(bits) == 8:
                c = sum(bits[i] * 2**i for i in range(8))
                if c == 0:
                    break
                text.append(c)
                bits = []
        self.entry.insert(0, str(bytes(text), encoding))

    def __init__(self, master_frame, entry, original):
        self.entry = entry
        self.original = original
        self.image = None
        frame = tkinter.LabelFrame(master_frame, text='Reveal')
        tkinter.Label(frame, text='Edited image').pack(side=tkinter.LEFT,
                                                       padx=10)
        self.label = tkinter.Label(frame)
        tkinter.Button(frame, text='Open',
                       command=self.get_bmp).pack(side=tkinter.LEFT, padx=10)
        tkinter.Button(frame, text='Reveal',
                       command=self.find_message).pack(side=tkinter.LEFT,
                                                       padx=10)
        self.label.pack(side=tkinter.LEFT, padx=10)

        frame.pack(anchor=tkinter.W, fill=tkinter.X, padx=10, pady=5, ipady=10)


class steganography_ui:
    def message_ui(self, master_frame):
        frame = tkinter.Frame(master_frame)
        tkinter.Label(frame, text='Message').pack(side=tkinter.LEFT,
                                                  padx=10,
                                                  pady=10)
        self.entry = tkinter.Entry(frame, width=50)
        self.entry.pack(side=tkinter.LEFT)
        frame.pack(anchor=tkinter.W)

    def __init__(self, master_frame):
        self.message_ui(master_frame)
        self.original = link_or_file_ui(master_frame, 'Original image')
        concealing_ui(master_frame, self.entry, self.original)
        revealing_ui(master_frame, self.entry, self.original)
