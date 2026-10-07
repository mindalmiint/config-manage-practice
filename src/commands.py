"""Модуль команд эмулятора оболочки."""


def execute_command(command_name, arguments):
    """Выполняет команду по её имени.

    Args:
        command_name: Имя команды (строка).
        arguments: Список аргументов команды.

    Returns:
        Кортеж (результат, флаг_выхода).
        Флаг_выхода=True только для команды exit.
    """
    if command_name == "ls":
        return (cmd_ls(arguments), False)
    elif command_name == "cd":
        return (cmd_cd(arguments), False)
    elif command_name == "exit":
        return (cmd_exit(arguments), True)
    else:
        return (f"command not found: {command_name}", False)


def cmd_ls(arguments):
    """Заглушка команды ls. Возвращает имя и аргументы."""
    return f"ls {arguments}"


def cmd_cd(arguments):
    """Заглушка команды cd. Возвращает имя и аргументы."""
    return f"cd {arguments}"


def cmd_exit(arguments):
    """Заглушка команды exit. Возвращает имя и аргументы."""
    return f"exit {arguments}"
