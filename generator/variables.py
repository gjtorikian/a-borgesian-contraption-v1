import re


def run_name():
    return 'small_10k'


def model_name():
    return "124M"


def file_name():
    return "borges.txt"


def length():
    return 5  # ideally, 22


def truncate(text, length):
    ending = text[length:]

    prev = re.search(r"\b\.!?", ending)

    if prev == None:
        return text

    idx = re.search(r"\b\.!?", ending).start() + 1

    return text[:length] + ending[:idx]
