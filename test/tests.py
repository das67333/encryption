import random, time, tkinter, tkinter.ttk, sys, unittest

sys.path.append('..')
import src.ciphers, src.cryptography, src.graphUI, src.steganography
from src.functions import *


class Tests(unittest.TestCase):
    def check_ciphers(self, data, key):
        for cipher in src.ciphers.cipher_dict.values():
            new_data = cipher.decrypt(cipher.encrypt(data, key), key)
            self.assertEqual(data, new_data)

    def get_rand_bytes(self, n):
        return bytes(random.choices(range(256), k=n))

    def check_widget(self, widget, *args):
        for i in range(3):
            window = tkinter.Tk()
            widget(window, *args)
            window.after(100, window.quit)
            window.mainloop()

    def test_ciphers1(self):
        data, key = b'Hello world!', b'Key' * 10
        Tests.check_ciphers(self, data, key)

    def test_ciphers2(self):
        lengths = [10, 50, 1000]
        for i in lengths:
            self.check_ciphers(self.get_rand_bytes(i), self.get_rand_bytes(i))

    def test_cryptography_ui1(self):
        self.check_widget(src.cryptography.text_or_file_ui, 'Test')

    def test_cryptography_ui2(self):
        self.check_widget(src.cryptography.cryptography_ui)

    def test_steganography_ui1(self):
        self.check_widget(src.steganography.concealing_ui, tkinter.Entry(),
                          None)

    def test_steganography_ui2(self):
        self.check_widget(src.steganography.revealing_ui, tkinter.Entry(),
                          None)

    def test_steganography_ui3(self):
        self.check_widget(src.steganography.link_or_file_ui, 'Test')

    def test_steganography_ui4(self):
        self.check_widget(src.steganography.steganography_ui)

    def test_messagebox(self):
        src.steganography.show(None)

    def test_sys_functions(self):
        assert isinstance(platform(), str)
        assert isinstance(project_dir(), str)

    def test_launch(self):
        src.graphUI.App()


if __name__ == '__main__':
    unittest.main()
