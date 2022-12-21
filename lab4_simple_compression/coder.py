#!/usr/bin/env python3

import string
from typing import List, Dict, Tuple
from bitarray import bitarray

EOF = '$'


def create() -> Dict[str, str]:
    chars: List[str] = list(string.ascii_lowercase) + [str(i) for i in range(10)] + [' '] + [EOF]
    codes: List[str] = [bin(i)[2:].rjust(6, '0') for i in range(len(chars))]
    return dict(zip(chars, codes))


def encode(text: str, codes_dict: Dict[str, str]) -> bitarray:
    bit_array = bitarray()
    for letter in text:
        bit_array.extend(codes_dict[letter])
    bit_array.extend(codes_dict[EOF])
    return bit_array


def save(text_bits: bitarray, codes_dict: Dict[str, str]) -> None:
    code_content: List[str] = []
    for letter, code in codes_dict.items():
        code_content.append(f'{letter}\t{code}')

    with open('code.txt', 'w') as code_file:
        code_file.write('\n'.join(code_content))

    with open('text.bin', 'wb') as bin_file:
        text_bits.tofile(bin_file)


def load() -> Tuple[bitarray, Dict[str, str]]:
    text_bits = bitarray()
    with open('text.bin', 'rb') as bin_file:
        text_bits.fromfile(bin_file)

    with open('code.txt', 'r') as code_file:
        code_content = code_file.read()

    codes_dict: Dict[str, str] = {}
    for line in code_content.splitlines():
        letter, code = line.split('\t')
        codes_dict[letter] = code

    return text_bits, codes_dict


def decode(text_bits: bitarray, codes_dict: Dict[str, str]) -> str:
    codes_dict_reversed: Dict[str, str] = dict((v, k) for k, v in codes_dict.items())
    text: List[str] = []
    code_length = len(list(codes_dict.values())[0])
    for i in range(0, len(text_bits), code_length):
        code: str = text_bits[i:i + code_length].to01()
        letter: str = codes_dict_reversed[code]
        if letter == EOF:
            break
        text.append(codes_dict_reversed[code])
    return ''.join(text)
