import argparse
import urllib.request
import sys
import cowsay
import random


def bulls_cows(guess: str, secret: str) -> tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))

    from collections import Counter
    guess_counter = Counter(guess)
    secret_counter = Counter(secret)
    common_letters = sum((guess_counter & secret_counter).values())

    cows = common_letters - bulls

    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = random.choice(words)
    attempt_cnt = 0
    while True:
        guess_word = ask("Введите слово: ", words)
        attempt_cnt += 1
        b, c = bulls_cows(guess_word, secret_word)
        inform("Быки: {}, Коровы: {}", b, c)
        if guess_word != secret_word:
            continue
        print(cowsay.cowsay(
            "Эты было не просто жёстко, это было очень жёстко!", cow="dragon"))
        return attempt_cnt


def ask(prompt: str, valid: list[str] = None) -> str:
    with open("my_custom_cow.cow", "r") as f:
        my_custom_cow = cowsay.read_dot_cow(f)
    while True:
        print(cowsay.cowsay(prompt, cowfile=my_custom_cow))
        guess_word = input()
        if guess_word not in valid:
            print(cowsay.cowsay("Недопустимое слово", cowfile=my_custom_cow))
            continue
        break
    return guess_word


def inform(format_string: str, bulls: int, cows: int) -> None:
    available_cows = cowsay.list_cows()
    random_cow = random.choice(available_cows)
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=random_cow))


def load_words(source: str) -> list[str]:
    if source.startswith(('http://', 'https://')):
        with urllib.request.urlopen(source) as response:
            return response.read().decode('utf-8').splitlines()
    else:
        with open(source, encoding='utf-8') as file:
            return file.read().splitlines()


def main():
    parser = argparse.ArgumentParser(description="Игра 'Быки и коровы'")
    parser.add_argument("dictionary", help="Файл или URL со словарём")
    parser.add_argument("length", nargs="?", type=int, default=5,
                        help="Длина используемых слов (по умолчанию 5)")
    args = parser.parse_args()

    words = [word for word in load_words(
        args.dictionary) if len(word) == args.length]
    if not words:
        print(f"Нет слов длиной {args.length} в указанном словаре.")
        sys.exit(1)

    gameplay(ask, inform, words)


if __name__ == "__main__":
    main()

