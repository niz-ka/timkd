#!/usr/bin/env python3

# Odpowiedzi do zadania znajdują się w pliku results.txt (szczególnie na samym końcu)
# Użycie: ./main.py input_file.txt

import sys
import math
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple


class LetterEntropyRunner:

    def calculcate_n_gram_count(self, input_text: str, n: int) -> DefaultDict[str, int]:
        n_grams = [input_text[i:i + n] for i in range(len(input_text) - n + 1)]

        n_gram_count = defaultdict(int)
        for token in n_grams:
            n_gram_count[token] += 1

        return n_gram_count

    def calculate_n_order_markov_source(
        self,
        input_text: str,
        order: int,
    ) -> Tuple[Dict[str, float], DefaultDict[str, Dict[str, float]]]:
        n_gram_count = self.calculcate_n_gram_count(input_text, order + 1)
        n_1_gram_count = self.calculcate_n_gram_count(input_text, order)

        count = sum(n_gram_count.values())
        probabilities = {n_gram: value / count for n_gram, value in n_gram_count.items()}

        conidtional_probabilities = defaultdict(dict)
        for token in n_gram_count:
            probability = n_gram_count[token] / n_1_gram_count[token[:-1]]
            letter, predecessor = token[-1], token[:-1]
            conidtional_probabilities[predecessor][letter] = probability

        return probabilities, conidtional_probabilities

    def calculate_conditional_entropy(
        self,
        probabilities: Dict[str, float],
        conditional_probabilities: DefaultDict[str, Dict[str, float]],
    ) -> float:
        conditional_probabilities.default_factory = None
        result = 0.0
        for token, p1 in probabilities.items():
            predecessor, letter = token[:-1], token[-1]
            p2 = conditional_probabilities[predecessor][letter]
            result += p1 * math.log(p2, 2)
        return -1 * result

    def calculate_entropy(self, text: str) -> float:
        letter_count = defaultdict(int)
        size = len(text)

        for letter in text:
            letter_count[letter] += 1

        result = 0.0
        for count in letter_count.values():
            p = count / size
            result += p * math.log(p, 2)

        return -result

    def run(self, input: str):
        entropy = self.calculate_entropy(input)
        print('Letter entropy:', entropy)

        for order in (1, 2, 3, 4):
            probabilities, conditional_probabilities = self.calculate_n_order_markov_source(input, order)
            conditional_entropy = self.calculate_conditional_entropy(probabilities, conditional_probabilities)
            print(f'Letter conditional entropy (order {order}): {conditional_entropy}')


class WordEntropyRunner:

    def calculcate_n_gram_count(self, input_text: str, n: int) -> DefaultDict[str, int]:
        input_text = input_text.split()
        n_grams = [tuple(input_text[i:i + n]) for i in range(len(input_text) - n + 1)]

        n_gram_count = defaultdict(int)
        for token in n_grams:
            n_gram_count[token] += 1

        return n_gram_count

    def calculate_n_order_markov_source(
        self,
        input_text: str,
        order: int,
    ) -> Tuple[Dict[str, float], DefaultDict[str, Dict[str, float]]]:
        n_gram_count = self.calculcate_n_gram_count(input_text, order + 1)
        n_1_gram_count = self.calculcate_n_gram_count(input_text, order)

        count = sum(n_gram_count.values())
        probabilities = {n_gram: value / count for n_gram, value in n_gram_count.items()}

        conditional_probabilities = defaultdict(dict)
        for words in n_gram_count:
            predecessors, word = words[:-1], words[-1]
            probability = n_gram_count[words] / n_1_gram_count[predecessors]
            conditional_probabilities[predecessors][word] = probability

        return probabilities, conditional_probabilities

    def calculate_conditional_entropy(
        self,
        probabilities: Dict[str, float],
        conditional_probabilities: DefaultDict[str, Dict[str, float]],
    ) -> float:
        conditional_probabilities.default_factory = None
        result = 0.0
        for token, p1 in probabilities.items():
            predecessor, letter = token[:-1], token[-1]
            p2 = conditional_probabilities[predecessor][letter]
            result += p1 * math.log(p2, 2)
        return -1 * result

    def calculate_entropy(self, text: str) -> float:
        word_count = defaultdict(int)
        size = len(text.split())

        for word in text.split():
            word_count[word] += 1

        result = 0.0
        for count in word_count.values():
            p = count / size
            result += p * math.log(p, 2)

        return -result

    def run(self, input: str):
        entropy = self.calculate_entropy(input)
        print('Word entropy:', entropy)

        for order in (1, 2, 3, 4):
            probabilities, conditional_probabilities = self.calculate_n_order_markov_source(input, order)
            conditional_entropy = self.calculate_conditional_entropy(probabilities, conditional_probabilities)
            print(f'Word conditional entropy (order {order}): {conditional_entropy}')


def main() -> None:
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <input_file>')
        print(f'Example: {sys.argv[0]} input.txt')
        sys.exit(1)

    with open(sys.argv[1], 'r') as input_file:
        file_content = input_file.read()

    print('File:', sys.argv[1])
    print('----------')
    letter_entropy_runner = LetterEntropyRunner()
    letter_entropy_runner.run(file_content)
    print('----------')
    word_entropy_runner = WordEntropyRunner()
    word_entropy_runner.run(file_content)


if __name__ == "__main__":
    main()
