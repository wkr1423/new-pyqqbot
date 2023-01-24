def deleteBlanks(command):
    while command[0] == "": del command[0]
    return command


def command_spliter(command, commandSettings):
    data = {
        "error": None,
        "executor": None,
        "args": {}
    }
    command = command.split(" ")
    command = deleteBlanks(command)
    if len(command) == 0:
        # menu
        data["executor"] = None
        return data
    executor = command[0]
    if executor in command:
        executor = command[executor]
