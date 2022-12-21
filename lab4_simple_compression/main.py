#!/usr/bin/env python3

from coder import create, encode, decode, load, save

if __name__ == "__main__":
    with open('norm_wiki_sample.txt', 'r') as file:
        text = file.read()

    codes_dict = create()
    encoded_text = encode(text, codes_dict)
    save(encoded_text, codes_dict)
    # ----------------
    loaded_encoded_text, loaded_codes_dict = load()
    decoded_text = decode(loaded_encoded_text, loaded_codes_dict)

    if text == decoded_text:
        print("Compression OK")
    else:
        print("Compression WRONG")
