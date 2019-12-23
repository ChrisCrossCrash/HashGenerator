import hashlib
import argparse

BLOCKSIZE = 2**16  # 65536 B
VERSION = '0.1'
PROGRAM_NAME = 'CLI Hash Checker'
LICENSE_URL = 'https://github.com/ChrisCrossCrash/HashGenerator/blob/master/LICENSE'
LICENSE = f'''{PROGRAM_NAME}  Copyright (C) 2019  Christopher Kumm
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; for details, please visit:\n{LICENSE_URL}
'''

if __name__ == '__main__':
    verbose = True
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-l', '--listalgs', help='list the algorithms available on this machine', action='store_true')
    mode.add_argument('-t', '--text', help='the text/string you want to hash')
    mode.add_argument('-f', '--file', help='the location of the file you want to hash')
    mode.add_argument('--version', help='prints version and license info', action='store_true')
    parser.add_argument('-a', '--algorithm', help='the hash algorithm you want to use', choices=hashlib.algorithms_available)
    parser.add_argument('--verify', help='the hash you want to verify')
    parser.add_argument('-i', '--iterations', help='perform multiple iterations of the hash', type=int)
    args = parser.parse_args()

    if args.version:
        print(LICENSE)
    elif args.listalgs:
        for alg in hashlib.algorithms_available:
            print(alg)
    else:
        empty_hasher = hashlib.new(args.algorithm)
        hasher = empty_hasher.copy()
        if args.text:
            hasher.update(bytes(args.text, 'utf-8'))
        elif args.file:
            if verbose:
                print('hashing...')
            with open(args.file, 'rb') as f:
                buf = f.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(BLOCKSIZE)

        if args.verify:
            if args.verify == hasher.hexdigest():
                if verbose:
                    print(f'{hasher.hexdigest()}\nSecure hashes MATCH!')
                else:
                    print(True)
            else:
                if verbose:
                    print(f'{hasher.hexdigest()}\nsecure hashes DON\'T MATCH!')
                else:
                    print(False)
        else:
            # TODO: iterations don't work
            if args.iterations:
                result = hasher.digest()
                print(result)
                iter_hash = empty_hasher.copy()
                print(f'this should be the empty hasher: {iter_hash.hexdigest()}')
                for i in range(args.iterations):
                    iter_hash = empty_hasher.copy()
                    iter_hash.update(result)
                    result = iter_hash.digest()
                    print(result)
                print(f'{iter_hash.name} secure hash in hexidecimal ({args.iterations} iterations):\n' + iter_hash.hexdigest())
            else:
                print(f'{hasher.name} secure hash in hexidecimal:\n' + hasher.hexdigest())
