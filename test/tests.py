import ciphers
import random
import unittest

class Tests(unittest.TestCase):
    def check_ciphers(self, data, key):
        for cipher in ciphers.cipher_class.values():
            new_data = cipher.decrypt(cipher.encrypt(data, key), key)
            self.assertEqual(data, new_data)

    def test1(self):
        data, key = b'Hello world!', b'Key' * 10
        Tests.check_ciphers(self, data, key)

    def get_rand_bytes(n):
        return bytes(random.choices(range(256), k=n))

    def test2(self):
        for i in range(100):
            Tests.check_ciphers(self, Tests.get_rand_bytes(i), Tests.get_rand_bytes(i))

if __name__ == '__main__':
    unittest.main()
