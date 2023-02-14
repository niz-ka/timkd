#!/usr/bin/env python3

from typing import List, Dict, Tuple, Optional
from bitarray import bitarray
from math import log2, ceil


def create(data: str) -> Dict[str, int]:
    i = 0
    codes_dict: Dict[str, int] = {}

    for char in data:
        if char not in codes_dict:
            codes_dict[char] = i
            i += 1

    return codes_dict


def encode(data: str, codes_dict: Dict[str, int], max_dict_size: Optional[int]) -> Tuple[bitarray, int]:

    D = {k: v for k, v in codes_dict.items()}
    n = len(D)

    c = data[0]
    result: List[int] = []

    for s in data[1:]:
        if c + s in D:
            c += s
        else:
            result.append(D[c])
            if max_dict_size is None or len(D) < max_dict_size:
                D[c + s] = n
                n += 1
            c = s

    result.append(D[c])

    bit_array = bitarray()
    max_decimal = max(result)
    if max_decimal < 2:
        code_length = 1
    else:
        code_length = ceil(log2(max(result)))

    for code_int in result:
        code_binary: str = bin(code_int)[2:].rjust(code_length, '0')
        bit_array.extend(code_binary)

    return bit_array, code_length


def save(encoded_data: bitarray, codes_dict: Dict[str, int], code_length: int) -> None:
    assert len(encoded_data) == len(encoded_data.to01())

    code_content: List[str] = [f'{len(encoded_data)} {code_length}']
    for char, code_int in codes_dict.items():
        code_content.append(f'{ord(char)} {code_int}')

    with open('code.txt', 'w') as code_file:
        code_file.write('\n'.join(code_content))

    with open('data.bin', 'wb') as bin_file:
        encoded_data.tofile(bin_file)


def load() -> Tuple[bitarray, Dict[str, int], int]:
    encoded_data = bitarray()
    with open('data.bin', 'rb') as bin_file:
        encoded_data.fromfile(bin_file)

    with open('code.txt', 'r') as code_file:
        code_content = code_file.read()

    length, code_length = code_content.splitlines()[0].split(' ')

    codes_dict: Dict[str, int] = {}
    for line in code_content.splitlines()[1:]:
        char_int, code_int = line.split(' ')
        codes_dict[chr(int(char_int))] = int(code_int)

    return encoded_data[:int(length)], codes_dict, int(code_length)


def decode(encoded_data: bitarray, codes_dict: Dict[str, int], code_length: int) -> str:
    D = {v: k for k, v in codes_dict.items()}
    n = len(D)

    data_str = encoded_data.to01()
    data = [int(data_str[i:i + code_length], 2) for i in range(0, len(data_str), code_length)]

    pk = data[0]

    result = [D[pk]]

    for k in data[1:]:
        pc = D[pk]
        if k in D:
            D[n] = pc + D[k][0]
            n += 1
            result.append(D[k])
        else:
            D[n] = pc + pc[0]
            n += 1
            result.append(pc + pc[0])
        pk = k

    return ''.join(result)
