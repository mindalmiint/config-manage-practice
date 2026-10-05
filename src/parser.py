"""Модуль разбора командной строки на имя команды и аргументы."""

import shlex


def parse_command(line):
    """Разбирает строку команды на имя и список аргументов.

    Использует shlex для корректной обработки кавычек,
    как в настоящей UNIX-оболочке.

    Args:
        line: Строка, введённая пользователем.

    Returns:
        Кортеж (имя_команды, список_аргументов).
        Для пустой строки — (None, []).

    Raises:
        ValueError: Если кавычки в строке не закрыты.
    """
    stripped_line = line.strip()

    if not stripped_line:
        return (None, [])

    try:
        tokens = shlex.split(stripped_line)
    except ValueError as error:
        raise ValueError(
            f"Ошибка ввода команды: {error}"
        ) from error

    command_name = tokens[0]
    arguments = tokens[1:]

    return (command_name, arguments)
