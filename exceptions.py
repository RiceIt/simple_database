class CommandNotFoundError(Exception):
    def __init__(self, command_name):
        self.message = f'command "{command_name}" not found'
        super().__init__(self.message)


class TooMuchArgumentError(Exception):
    def __init__(self, command_name, command_args_count, args_len):
        self.message = f"command [{command_name}] takes {command_args_count} argument(s), but {args_len} were given"
        super().__init__(self.message)


class MissingArgumentError(Exception):
    def __init__(self, command_name, missing_args):
        self.message = f"[{command_name}] missing {len(missing_args)} argument(s): {', '.join(missing_args)}"
        super().__init__(self.message)


class NotTransactionError(Exception):
    def __init__(self):
        super().__init__("there is no transaction in progress")
