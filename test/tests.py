import random
import sys
import unittest
sys.path.append('..')
import src.ciphers

class Tests(unittest.TestCase):
    def check_ciphers(self, data, key):
        for cipher in src.ciphers.cipher_dict.values():
            new_data = cipher.decrypt(cipher.encrypt(data, key), key)
            self.assertEqual(data, new_data)

    def test_ciphers1(self):
        data, key = b'Hello world!', b'Key' * 10
        Tests.check_ciphers(self, data, key)

    def get_rand_bytes(n):
        return bytes(random.choices(range(256), k=n))

    def test_ciphers2(self):
        for i in range(50):
            Tests.check_ciphers(self, Tests.get_rand_bytes(i), Tests.get_rand_bytes(i))

if __name__ == '__main__':
    unittest.main()
