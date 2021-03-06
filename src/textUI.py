import argparse, cryptography, time


def command_line_args():
    parser = argparse.ArgumentParser(description='Tutorial')
    parser.add_argument('-f',
                        '--file',
                        required=True,
                        type=str,
                        help='path to the data file')
    parser.add_argument('-k',
                        '--key',
                        required=True,
                        type=str,
                        help='encryption/decryption key')

    parser.add_argument('-c',
                        '--cipher',
                        required=True,
                        type=str,
                        choices=cryptography.ciphers.cipher_dict.keys(),
                        help='cipher type to use')

    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('-e',
                           '--encrypt',
                           action='store_true',
                           help='encrypt the file')
    operation.add_argument('-d',
                           '--decrypt',
                           action='store_true',
                           help='decrypt the file')

    args = parser.parse_args()
    args.file_data = args.file
    del args.file
    args.text_key = args.key
    del args.key
    args.key = bytes(args.key, encoding='utf-8')
    args.cipher = cipher_dict[args.cipher]
    args.encrypt = not bool(args.decrypt)
    del args.decrypt
    return args


try:
    ts = time.time()
    args = command_line_args()
    cryptography.run(args)
    te = time.time()
    print('{}cryption finished'.format('En' if args.encrypt else 'De'))
    print('Time taken:', te - ts, 'sec')
except Exception as exception:
    print('{}cryption failed'.format('En' if args.encrypt else 'De'))
    print(exception)
