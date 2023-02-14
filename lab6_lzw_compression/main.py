#!/usr/bin/env python3

import sys
import os
from typing import Optional
from math import pow
from coder import create, load, save, encode, decode


def read_file(path: str) -> str:
    with open(path, 'rb') as binary_file:
        binary_data = binary_file.read()
    return ''.join([chr(i) for i in binary_data])


def run_with(file_path: str, max_dict_size: Optional[int]) -> None:
    data = read_file(file_path)

    codes_dict = create(data)
    encoded_data, code_length = encode(data, codes_dict, max_dict_size)
    save(encoded_data, codes_dict, code_length)

    loaded_encoded_data, loaded_codes_dict, loaded_code_length = load()

    assert encoded_data == loaded_encoded_data
    assert codes_dict == loaded_codes_dict
    assert code_length == loaded_code_length

    decoded_data = decode(loaded_encoded_data, loaded_codes_dict, loaded_code_length)

    if data == decoded_data:
        original_size = os.stat(file_path).st_size / (1024 * 1024)
        encoded_size = os.stat("data.bin").st_size / (1024 * 1024)
        compression = (original_size - encoded_size) / original_size * 100
        print('------------------------------------')
        print(f'FILE: {file_path} | MAX_DICT_SIZE: {max_dict_size if max_dict_size is not None else "INFINITY"}')
        print(f'Original {file_path} size: {round(original_size, 3)} MB')
        print(f'Encoded {file_path} size: {round(encoded_size, 3)} MB')
        print(f'Compression: {round(compression, 3)}%')
        print('------------------------------------')
    else:
        raise RuntimeError(f'LZW compression failed for file "{file_path}" with max dictionary size: {max_dict_size}')


def main() -> None:
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [file1] file2 file3 ...')
        print(f'Example: {sys.argv[0]} lena.bmp norm_wiki_sample.txt wiki_sample.txt')
        sys.exit(1)

    for file_path in sys.argv[1:]:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f'File "{file_path}" not found! LZW compression impossible!')

        run_with(file_path, None)
        run_with(file_path, int(pow(2, 18)))
        run_with(file_path, int(pow(2, 12)))


if __name__ == '__main__':
    main()
