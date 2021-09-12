class CommandNotFoundError(Exception):
    def __init__(self, command_name):
        self.message = 'command "{}" not found'.format(command_name)
        super().__init__(self.message)


class TooMuchArgumentError(Exception):
    def __init__(self, command_name, command_args_count, args_len):
        self.message = "command [{}] takes {} argument(s), but {} were given".format(command_name, command_args_count, args_len)
        super().__init__(self.message)


class MissingArgumentError(Exception):
    def __init__(self, command_name, missing_args):
        self.message = "[{}] missing {} argument(s): {}".format(command_name, len(missing_args), ', '.join(missing_args))
        super().__init__(self.message)


class NotTransactionError(Exception):
    def __init__(self):
        super().__init__("there is no transaction in progress")
