import shlex

def parse_command(line):
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