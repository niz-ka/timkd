#!/usr/bin/env python3

import sys
from collections import defaultdict


def calculcate_n_gram_count(input_text, n):
    n_grams = [input_text[i:i + n] for i in range(len(input_text) - n + 1)]

    n_gram_count = defaultdict(int)
    for token in n_grams:
        n_gram_count[token] += 1

    return n_gram_count


def calculate_n_order_markov_source(input_text, order):
    n_gram_count = calculcate_n_gram_count(input_text, order + 1)
    n_1_gram_count = calculcate_n_gram_count(input_text, order)

    probabilities = {}
    for token in n_gram_count:
        key = f'"{token[-1]}"|"{token[:-1]}"'
        probability = n_gram_count[token] / n_1_gram_count[token[:-1]]
        probabilities[key] = probability

    return dict(sorted(probabilities.items(), key=lambda item: item[1], reverse=True))


def save_results(results):
    with open(sys.argv[2], 'w') as file:
        for result in results:
            file.write("#######\n")
            for key in result:
                file.write(f'{key} = {round(result[key] * 100, 4)}%\n')


def calculate_markov():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <input_file> <output_file>')
        sys.exit(1)

    with open(sys.argv[1], 'r') as input_file:
        file_content = input_file.read()

    first_order = calculate_n_order_markov_source(file_content, 1)
    third_order = calculate_n_order_markov_source(file_content, 3)
    fifth_order = calculate_n_order_markov_source('probability ' + file_content, 5)

    save_results((first_order, third_order, fifth_order))

    print(f'Result saved in {sys.argv[2]}. N-order result delimiter is #######')


if __name__ == "__main__":
    calculate_markov()
