from hashlib import md5
from math import factorial
import random


def get_hash(key):
    return int(md5(key).hexdigest(), base = 16)


class CaesarCipher:
    def encrypt(data, key):
        key = get_hash(key)
        return bytes((c + key) % 256 for c in data)

    def decrypt(data, key):
        key = get_hash(key)
        return bytes((c - key) % 256 for c in data)


class VigenereCipher:
    def encrypt(data, key):
        return bytes((c + key[i % len(key)]) % 256 for i, c in enumerate(data))

    def decrypt(data, key):
        return bytes((c - key[i % len(key)]) % 256 for i, c in enumerate(data))


class VernamCipher:
    def check_key(data, key):
        if len(key) < len(data):
            raise ValueError('Key is not long enough')

    def encrypt(data, key):
        VernamCipher.check_key(data, key)
        return bytes(data[i] ^ key[i] for i in range(len(data)))

    def decrypt(data, key):
        VernamCipher.check_key(data, key)
        return VernamCipher.encrypt(data, key)


class PermutationCipher:
    # expanded key is permutation number
    def expand_key(key):
        random.seed(get_hash(key))
        return random.randrange(factorial(256))

    # returns permutated list(range(n))
    def kth_permutation(n, k):
        factorials = [1]
        for i in range(n - 1):
            factorials.append(factorials[len(factorials) - 1] * len(factorials))
        positions = []
        for fct in reversed(factorials):
            pos, k = divmod(k, fct)
            positions.append(pos)
        result, value = [-1] * n, 0
        for pos in positions:
            index = 0
            while bool(pos) or result[index] != -1:
                if result[index] == -1:
                    pos -= 1
                index += 1
            result[index] = value
            value += 1
        return result

    def encrypt(data, key):
        key = PermutationCipher.expand_key(key)
        dictionary = PermutationCipher.kth_permutation(256, key)
        return bytes(dictionary[c] for c in data)

    def decrypt(data, key):
        key = PermutationCipher.expand_key(key)
        reversed_dictionary = PermutationCipher.kth_permutation(256, key)
        dictionary = list(map(reversed_dictionary.index, range(256)))
        return bytes(dictionary[c] for c in data)


cipher_class = {'caesar': CaesarCipher, 'vigenere': VigenereCipher, 'vernam': VernamCipher,
                   'custom': PermutationCipher}
