import inspect
from collections import Counter
from copy import copy

from exceptions import CommandNotFoundError, TooMuchArgumentError, MissingArgumentError, NotTransactionError


class Transaction:
    def __init__(self):
        self._created_vars = {}
        self._updated_vars = {}
        self._deleted_vars = set()

    def create_var(self, var: str, value: str):
        self._created_vars[var] = value

    def update_var(self, var: str, value: str):
        self._updated_vars[var] = value

    def delete_var(self, var: str):
        self._deleted_vars.add(var)

    def get_vars(self):
        vars = copy(self._created_vars)
        vars.update(self._updated_vars)
        return vars

    def get_deleted_vars(self) -> set:
        return self._deleted_vars


class DataBase:
    def __init__(self):
        self._commands = {
            "GET": self._get,
            "SET": self._set,
            "UNSET": self._unset,
            "COUNTS": self._counts,
            "FIND": self._find,
            "END": self._end,
            "BEGIN": self._begin,
            "ROLLBACK": self._rollback,
            "COMMIT": self._commit,
        }

        self._commited_values = {}
        self._transactions = []

    @property
    def _transactions_deleted_values(self) -> list:
        return [var for transaction in self._transactions for var in transaction.get_deleted_vars()]

    @property
    def _transactions_values(self) -> dict:
        return {var: value for transaction in self._transactions for var, value in transaction.get_vars().items()}

    @property
    def _values(self) -> dict:
        values = self._commited_values
        values.update(self._transactions_values)
        for key in self._transactions_deleted_values:
            values.pop(key, None)
        return values

    def execute(self, command_name: str, args: tuple):
        command = self._get_command(command_name)
        self._validate_signature(command_name, args, command)
        self._print(command(*args))

    def _get_command(self, command_name: str):
        try:
            return self._commands[command_name]
        except KeyError:
            raise CommandNotFoundError(command_name)

    def _get(self, var: str) -> str:
        try:
            return self._values[var]
        except KeyError:
            return "NULL"

    def _set(self, var: str, value: str):
        if self._transactions:
            if self._values.get(var):
                self._transactions[-1].update_var(var, value)
            else:
                self._transactions[-1].create_var(var, value)
        else:
            self._commited_values[var] = value

    def _unset(self, var: str):
        if self._values.get(var):
            if self._transactions:
                self._transactions[-1].delete_var(var)
            else:
                del self._commited_values[var]

    def _counts(self, var: str) -> str:
        return Counter(self._values.values())[var]

    def _find(self, var: str) -> str:
        found_vars = " ".join(filter(lambda key: self._values[key] == var, self._values.keys()))
        if found_vars:
            return found_vars

    def _end(self):
        raise EOFError

    def _begin(self):
        self._transactions.append(Transaction())

    def _rollback(self):
        try:
            self._transactions.pop()
        except IndexError:
            raise NotTransactionError()

    def _commit(self):
        self._commited_values.update(self._transactions_values)
        for key in self._transactions_deleted_values:
            self._commited_values.pop(key, None)
        self._transactions = []

    @staticmethod
    def _print(value: str):
        if value is not None:
            print(value)

    @staticmethod
    def _validate_signature(command_name: str, args: tuple, command):
        command_args_count = len(inspect.signature(command).parameters)
        if len(args) > command_args_count:
            raise TooMuchArgumentError(command_name, command_args_count, len(args))
        elif len(args) < command_args_count:
            missing_args = tuple(inspect.signature(command).parameters.keys())[len(args):]
            raise MissingArgumentError(command_name, missing_args)


if __name__ == '__main__':
    database = DataBase()
    while True:
        try:
            command_name, *args = input("db=> ").strip().split(" ")
            try:
                database.execute(command_name.upper(), args)
            except (CommandNotFoundError, TooMuchArgumentError, MissingArgumentError, NotTransactionError) as e:
                print(e)
        except EOFError:
            break
