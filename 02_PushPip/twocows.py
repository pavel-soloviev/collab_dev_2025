import argparse
import cowsay


def draw_cows(left_cow: str, right_cow: str):
    left_lines = left_cow.split('\n')
    right_lines = right_cow.split('\n')

    max_left_width = max(len(line) for line in left_lines)
    max_height = max(len(left_lines), len(right_lines))

    # Дополняем коров до одинаковой высоты
    left_padded = [' ' * max_left_width] * (max_height - len(left_lines)) + left_lines
    right_padded = [' ' * len(right_lines[0])] * (max_height - len(right_lines)) + right_lines

    space_between = ' ' * 5
    return "\n".join(
        l + ' ' * (max_left_width - len(l)) + space_between + r
        for l, r in zip(left_padded, right_padded)
    )


def main():
    parser = argparse.ArgumentParser(
        description="Вывод двух чудо-коров, выровненных по горизонтали."
    )
    parser.add_argument("-f", "--first_cow", default="moose", help="Первая корова")
    parser.add_argument("-F", "--second_cow", default="dragon", help="Вторая корова")
    parser.add_argument("-E", "--eyes", default="oo", help="Глаза второй коровы")
    parser.add_argument("-N", "--tongue", default="  ", help="Язык второй коровы")
    parser.add_argument("first_message", help="Сообщение первой коровы")
    parser.add_argument("second_message", help="Сообщение второй коровы")

    args = parser.parse_args()

    first_cow_art = cowsay.cowsay(args.first_message, cow=args.first_cow)

    second_cow_art = cowsay.cowsay(args.second_message, cow=args.second_cow, eyes=args.eyes, tongue=args.tongue)

    print(draw_cows(first_cow_art, second_cow_art))


if __name__ == "__main__":
    main()
