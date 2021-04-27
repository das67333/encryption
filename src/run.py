'''
Call cipher methods with no data loss in case of exceptions
'''

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
