import pytest

from main import DataBase


@pytest.fixture
def created_database():
    database = DataBase()
    database.execute("SET", ("x", "10"))
    database.execute("SET", ("a", "20"))
    database.execute("SET", ("b", "10"))
    return database
