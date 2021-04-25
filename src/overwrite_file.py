def overwrite_file(args):
    name = 'encrypt' if args.encrypt else 'decrypt'
    with open(args.file, 'rb') as File:
        data = File.read()
    with open(args.file, 'wb') as File:
        try:
            File.write(getattr(args.cipher, name)(data, args.key))
        except:
            File.seek(0)
            File.write(data)
            raise
