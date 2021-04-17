import argparse
import ciphers
import decorators

@decorators.timing
def operation(args, name):
    # name is in ['encrypt', 'decrypt']
    with open(args.file, 'rb') as File:
        data = File.read()
    with open(args.file, 'wb') as File:
        try:
            File.write(getattr(args.cipher, name)(data, args.key))
            print('{}ion finished'.format(name))
        except:
            try:
                File.write(data)
                print('{}ion failed, your data is intact'.format(name))
            except:
                print('{}ion failed, your data is corrupted'.format(name))
            raise

def command_line_args():
    parser = argparse.ArgumentParser(description='Tutorial')
    parser.add_argument('-f', '--file', required=True, type=str, help='path to the file')
    parser.add_argument('-k', '--key', required=True, type=str, help='encryption/decryption key')

    parser.add_argument('-c', '--cipher', required=True, type=str,
                        choices=ciphers.cipher_class.keys(), help='cipher type to use')

    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('-e', '--encrypt', action='store_true', help='encrypt the file')
    operation.add_argument('-d', '--decrypt', action='store_true', help='decrypt the file')

    args = parser.parse_args()
    args.key = bytes(args.key, encoding='utf-8')
    args.cipher = ciphers.cipher_class[args.cipher]
    return args

try:
    args = command_line_args()
    if args.encrypt:
        operation(args, 'encrypt')
    if args.decrypt:
        operation(args, 'decrypt')
except Exception as exception:
    print(exception)
