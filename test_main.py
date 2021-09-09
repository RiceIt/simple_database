import pytest

from main import DataBase


@pytest.fixture
def created_database():
    database = DataBase()
    database.execute("SET", ("x", "10"))
    return database


@pytest.fixture
def created_filled_database():
    database = DataBase()
    return database


@pytest.mark.parametrize(
    ("var", "value"), (
        ("x", "5"),
        ("7345H8EWRa", "10"),
    )
)
def test_database_set(created_database, var, value):
    created_database._set(var, value)
    assert created_database._values[var] == value


@pytest.mark.parametrize(
    ("var", "value"), (
        ("x", "5"),
        ("7345H8EWRa", "10"),
    )
)
def test_database_get(created_database, var, value):
    created_database._set(var, value)
    assert created_database._values[var] == value

