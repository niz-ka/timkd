#!/usr/bin/env python3

import sys
from random import choice, choices
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple, Optional


def calculcate_n_gram_count(input_text: str, n: int) -> DefaultDict[str, int]:
    n_grams = [input_text[i:i + n] for i in range(len(input_text) - n + 1)]

    n_gram_count = defaultdict(int)
    for token in n_grams:
        n_gram_count[token] += 1

    return n_gram_count


def calculate_n_order_markov_source(input_text: str, order: int) -> Dict[Tuple[str, str], float]:
    n_gram_count = calculcate_n_gram_count(input_text, order + 1)
    n_1_gram_count = calculcate_n_gram_count(input_text, order)

    probabilities = {}
    for token in n_gram_count:
        probability = n_gram_count[token] / n_1_gram_count[token[:-1]]
        letter, predecessor = token[-1], token[:-1]
        probabilities[(predecessor, letter)] = probability

    return probabilities


def save_text_to_file(text: str, file_path: str) -> None:
    with open(file_path, 'w') as file:
        file.write(text)


def generate_text(
    probabilities: Dict[Tuple[str, str], float],
    length: int,
    first_token: Optional[str] = None,
) -> str:
    if first_token is None:
        first_token = choice(tuple(probabilities.keys()))[0]

    text = first_token
    predecessor_length = len(tuple(probabilities.keys())[0][0])

    while len(text) < length:
        predecessor = text[-predecessor_length:]
        possibilities = {k[1]: v for k, v in probabilities.items() if k[0] == predecessor}
        random_letter = choices(tuple(possibilities.keys()), tuple(possibilities.values()))[0]
        text += random_letter

    return text


def calculate_average_word_length(text: str) -> float:
    splitted_text = text.split()
    words_length_sum = sum([len(word) for word in splitted_text])
    return words_length_sum / len(splitted_text)


def main() -> None:
    if len(sys.argv) != 6:
        print(f'Usage: {sys.argv[0]} <input_file> <text_length> <output_file1> <output_file2> <output_file3>')
        print(f'Example: {sys.argv[0]} input.txt 1000 output1.txt output2.txt output3.txt')
        sys.exit(1)

    with open(sys.argv[1], 'r') as input_file:
        file_content = input_file.read()

    run_options = (
        (1, None, sys.argv[3]),
        (3, None, sys.argv[4]),
        (5, 'probability', sys.argv[5]),
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
