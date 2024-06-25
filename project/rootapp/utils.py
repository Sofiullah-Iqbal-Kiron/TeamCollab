from typing import List


def get_largest_choice(choices: List) -> str:
    largest = choices[0][0]
    for choice in choices:
        if len(choice[0]) > len(largest):
            largest = choice[0]

    return largest
