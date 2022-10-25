#!/usr/bin/env python3

import sys
from random import choice, choices
from collections import defaultdict
from typing import DefaultDict, Dict, Optional


def calculcate_n_gram_count(input_text: str, n: int) -> DefaultDict[str, int]:
    input_text = input_text.split()
    n_grams = [tuple(input_text[i:i + n]) for i in range(len(input_text) - n + 1)]

    n_gram_count = defaultdict(int)
    for token in n_grams:
        n_gram_count[token] += 1

    return n_gram_count


def calculate_n_order_markov_source(input_text: str, order: int) -> DefaultDict[str, Dict[str, float]]:
    n_gram_count = calculcate_n_gram_count(input_text, order + 1)
    n_1_gram_count = calculcate_n_gram_count(input_text, order)

    probabilities = defaultdict(dict)
    for words in n_gram_count:
        predecessors, word = words[:-1], words[-1]
        probability = n_gram_count[words] / n_1_gram_count[predecessors]
        probabilities[predecessors][word] = probability

    return probabilities


def save_text_to_file(text: str, file_path: str) -> None:
    with open(file_path, 'w') as file:
        file.write(text)


def generate_text(
    probabilities: DefaultDict[str, Dict[str, float]],
    length: int,
    first_token: Optional[str] = None,
) -> str:
    if first_token is None:
        first_token = choice(tuple(probabilities.keys()))

    text = []
    text.extend(first_token)
    predecessor_length = len(tuple(probabilities.keys())[0])

    if len(first_token) < predecessor_length:
        raise RuntimeError(f'First token is too short! Minimum length: {predecessor_length}')

    while len(text) < length:
        predecessors = tuple(text[-predecessor_length:])
        possibilities = probabilities[predecessors]
        random_word = choices(tuple(possibilities.keys()), tuple(possibilities.values()))[0]
        text.append(random_word)

    return ' '.join(text)


def calculate_average_word_length(text: str) -> float:
    splitted_text = text.split()
    words_length_sum = sum([len(word) for word in splitted_text])
    return words_length_sum / len(splitted_text)


def main() -> None:
    if len(sys.argv) != 6:
        print(f'Usage: {sys.argv[0]} <input_file> <text_length> <output_file1> <output_file2> <output_file3>')
        print(f'Example: {sys.argv[0]} input.txt 100000 output1.txt output2.txt output3.txt')
        sys.exit(1)

    with open(sys.argv[1], 'r') as input_file:
        file_content = input_file.read()

    run_options = (
        (1, None, sys.argv[3]),
        (2, None, sys.argv[4]),
        (3, None, sys.argv[5]),
    )

    text_length = int(sys.argv[2])
    for n_order, first_token, output_path in run_options:
        probabilities = calculate_n_order_markov_source(file_content, n_order)
        text = generate_text(probabilities, text_length, first_token)
        average_word_length = calculate_average_word_length(text)
        save_text_to_file(text, output_path)
        print(
            f'avg_word_length={round(average_word_length, 2)}',
            f'; text_length={text_length} and n_order={n_order}',
            f'; result saved in {output_path}',
        )


if __name__ == "__main__":
    main()
