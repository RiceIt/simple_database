import pytest

from exceptions import NotTransactionError, TooMuchArgumentError, MissingArgumentError
from main import Transaction


class TestDatabase:
    @pytest.mark.parametrize(
        ("var", "value"), (
            ("x", "5"),
            ("7345H8EWRa", "10"),
        )
    )
    def test_database_set(self, created_database, var, value):
        created_database._set(var, value)
        assert created_database._values[var] == value

    @pytest.mark.parametrize(
        ("var", "expected"), (
            ("x", "10"),
            ("z", "NULL"),
        )
    )
    def test_database_get(self, created_database, var, expected):
        assert created_database._get(var) == expected

    @pytest.mark.parametrize(
        ("var", ), (
            ("x", ),
            ("z", ),
        )
    )
    def test_database_unset(self, created_database, var):
        created_database._unset(var)
        with pytest.raises(KeyError):
            var = created_database._values[var]

    @pytest.mark.parametrize(
        ("var", "excepted"), (
            ("5", 0),
            ("10", 2),
            ("20", 1),
        )
    )
    def test_counts(self, created_database, var, excepted):
        assert created_database._counts(var) == excepted

    @pytest.mark.parametrize(
        ("var", "excepted"), (
            ("5", None),
            ("10", "x b"),
            ("20", "a"),
        )
    )
    def test_find(self, created_database, var, excepted):
        assert created_database._find(var) == excepted

    def test_end(self, created_database):
        with pytest.raises(EOFError):
            created_database._end()

    def test_begin(self, created_database):
        created_database._begin()
        assert type(created_database._transactions[-1]) == Transaction and len(created_database._transactions) == 1

    def test_rollback(self, created_database):
        with pytest.raises(NotTransactionError):
            created_database._rollback()

    def test_commit(self, created_database):
        values = created_database._values
        created_database._commit()
        assert created_database._values == values

    @pytest.mark.parametrize(
        ("command_name", "args", "exception"), (
            ("SET", (), MissingArgumentError),
            ("SET", ("x", ), MissingArgumentError),
            ("SET", ("x", "y", "z"), TooMuchArgumentError),
            ("SET", ("x", "y", "z", "a", "b", "c"), TooMuchArgumentError),
        )
    )
    def test_validate_signature(self, created_database, command_name, args, exception):
        with pytest.raises(exception):
            created_database._validate_signature(command_name, args, created_database._set)
