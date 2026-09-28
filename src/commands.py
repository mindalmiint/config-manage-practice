def execute_command(command_name, arguments):

    if command_name == "ls":
        return (cmd_ls(arguments), False)
    elif command_name == "cd":
        return (cmd_cd(arguments), False)
    elif command_name == "exit":
        return (cmd_exit(arguments), True)
    else:
        return (f"command not found: {command_name}", False)


def cmd_ls(arguments):
    return f"ls {arguments}"


def cmd_cd(arguments):
    return f"cd {arguments}"

def cmd_exit(arguments):
    return f"exit {arguments}"