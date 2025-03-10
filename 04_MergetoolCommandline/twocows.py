import shlex
import cmd
import cowsay


def draw_cows(left_cow: str, right_cow: str):
    left_lines = left_cow.split('\n')
    right_lines = right_cow.split('\n')

    max_left_width = max(len(line) for line in left_lines)
    max_height = max(len(left_lines), len(right_lines))

    # Дополняем коров до одинаковой высоты
    left_padded = [' ' * max_left_width] * \
        (max_height - len(left_lines)) + left_lines
    right_padded = [' ' * len(right_lines[0])] * \
        (max_height - len(right_lines)) + right_lines

    space_between = ' ' * 5
    return "\n".join(
        l + ' ' * (max_left_width - len(l)) + space_between + r
        for l, r in zip(left_padded, right_padded)
    )


class Comandline(cmd.Cmd):
    prompt = "cmd>> "

    def do_list_cows(self, arg):
        """Выводит список доступных персонажей cowsay."""
        if arg:
            print("Команда list_cows не принимает аргументов.")
            return
        cows = cowsay.list_cows()

        print("Доступные персонажи cowsay:")
        print(cows)

    def do_exit(self, arg):
        """Выход из командной строки."""
        print("До встречи!")
        return True

    def do_EOF(self, arg):
        return True

    def do_make_bubble(self, arg):
        """
        Имитирует вызов make_bubble() из python-cowsay.
        Создаёт текстовый пузырь с заданными параметрами.
        Использование: make_bubble text [-w width]
        Пример: make_bubble "Hello world" -w 20
        """
        try:
            args = shlex.split(arg)
        except ValueError as e:
            print(f"Ошибка разбора аргументов: {e}")
            return

        if not args:
            print("Необходимо указать текст. Использование: make_bubble text [-w width]")
            return

        text = args[0]
        width = 40

        i = 1
        while i < len(args):
            if args[i] == "-w" and i + 1 < len(args):
                try:
                    width = int(args[i + 1])
                    i += 2
                except ValueError:
                    print("Ошибка: ширина (-w) должна быть числом.")
                    return
            else:
                print(f"Неизвестный аргумент: {args[i]}")
                return

        if text is None:
            print("Текст не может быть None.")
            return

        try:
            bubble = cowsay.make_bubble(text, width=width, wrap_text=True)
            print(bubble)
        except Exception as e:
            print(f"Ошибка при создании пузыря: {e}")

    def do_cowsay(self, arg):
        """
        Первая корова говорит сообщение, вторая отвечает.
        Использование: cowsay [сообщение] [-n имя] [-r ответ] [-c1 корова1] [-c2 корова2] [eyes1=XX] [tongue1=UU] [eyes2=XX] [tongue2=UU]
        Пример: cowsay "Hello" -r "Hi back" -c1 moose -c2 dragon eyes1=OO tongue1=-- eyes2=XX tongue2=..
        """
        try:
            args = shlex.split(arg)
        except ValueError as e:
            print(f"Ошибка разбора аргументов: {e}")
            return

        if not args:
            return

        message = ""
        name = ""
        reply_to = ""
        cow1 = "default"
        cow2 = "default"
        eyes1 = "oo"
        tongue1 = "  "
        eyes2 = "oo"
        tongue2 = "  "

        i = 0
        while i < len(args):
            if args[i].startswith("-n") or args[i].startswith("--name"):
                if i + 1 < len(args):
                    name = args[i + 1]
                    i += 2
            elif args[i].startswith("-r") or args[i].startswith("--reply"):
                if i + 1 < len(args):
                    reply_to = args[i + 1]
                    i += 2
            elif args[i].startswith("-c1") or args[i].startswith("--cow1"):
                if i + 1 < len(args):
                    cow1 = args[i + 1]
                    i += 2
            elif args[i].startswith("-c2") or args[i].startswith("--cow2"):
                if i + 1 < len(args):
                    cow2 = args[i + 1]
                    i += 2
            elif "=" in args[i]:
                key, value = args[i].split("=", 1)
                if key == "eyes1":
                    eyes1 = value
                elif key == "tongue1":
                    tongue1 = value
                elif key == "eyes2":
                    eyes2 = value
                elif key == "tongue2":
                    tongue2 = value
                i += 1
            else:
                if not message:
                    message = args[i]
                    i += 1
                else:
                    print(f"Неизвестный аргумент: {args[i]}")
                    return

        try:
            result1 = cowsay.cowsay(
                message=message,
                cow=cow1,
                eyes=eyes1,
                tongue=tongue1
            )
            result2 = cowsay.cowsay(
                message=reply_to,
                cow=cow2,
                eyes=eyes2,
                tongue=tongue2,
            )
            print(draw_cows(result1, result2))
        except Exception as e:
            print(f"Ошибка при создании cowsay: {e}")

    def do_cowthink(self, arg):
        """
        Создаёт вывод с коровой и текстовым пузырём.
        Использование: cowthink [сообщение] [-c корова] [eyes=XX] [tongue=UU]
        Пример: cowthink "Thinking..." -c dragon eyes=XX tongue=--
        """
        try:
            args = shlex.split(arg)
        except ValueError as e:
            print(f"Ошибка разбора аргументов: {e}")
            return

        if not args:
            return

        message = ""
        cow = "default"
        eyes = "oo"
        tongue = "  "

        i = 0
        while i < len(args):
            if args[i].startswith("-c") or args[i].startswith("--cow"):
                if i + 1 < len(args):
                    cow = args[i + 1]
                    i += 2
            elif "=" in args[i]:
                key, value = args[i].split("=", 1)
                if key == "eyes":
                    eyes = value
                elif key == "tongue":
                    tongue = value
                i += 1
            else:
                if not message:
                    message = args[i]
                    i += 1
                else:
                    print(f"Неизвестный аргумент: {args[i]}")
                    return

        try:
            result = cowsay.cowthink(
                message=message,
                cow=cow,
                eyes=eyes,
                tongue=tongue
            )
            print(result)
        except Exception as e:
            print(f"Ошибка при создании cowthink: {e}")
    
    def complete_cowsay(self, text, line, begidx, endidx):
        """
        Предоставляет автодополнение для команды cowsay, предлагая названия коров.
        Работает для параметров -c1 и -c2.
        """
        available_cows = cowsay.list_cows()

        try:
            args = shlex.split(line)
        except ValueError:
            args = []

        if not text:
            return available_cows

        completions = []
        prev_arg = args[-2] if len(args) > 1 else ""

        if prev_arg in ["-c1", "--cow1", "-c2", "--cow2"]:
            completions = [cow for cow in available_cows if cow.startswith(text.lower())]

        return completions


if __name__ == '__main__':
    Comandline().cmdloop()

