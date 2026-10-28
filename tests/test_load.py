import pytest
from Load import load_table


class FakeCursor:
    def __init__(self):
        self.query = None
        self.values = None

    def executemany(self, query, values):
        self.query, self.values = query, values

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.last_cursor = FakeCursor()

    def cursor(self):
        return self.last_cursor


def test_upsert_idempotent():
    connection = FakeConnection()
    count = load_table(connection, "machines", [{"machine_id": "MACHINE_01", "machine_name": "Presse"}])
    query = connection.last_cursor.query
    assert count == 1
    assert "ON DUPLICATE KEY UPDATE `machine_name` = new_row.`machine_name`" in query
    assert "`machine_id` = new_row" not in query
    assert connection.last_cursor.values == [("MACHINE_01", "Presse")]


def test_table_non_autorisee():
    with pytest.raises(ValueError):
        load_table(FakeConnection(), "users", [{"id": 1}])


def test_colonne_invalide():
    with pytest.raises(ValueError):
        load_table(FakeConnection(), "machines", [{"machine_id": "M", "name; DROP TABLE x": 1}])


def test_cle_primaire_obligatoire():
    with pytest.raises(ValueError):
        load_table(FakeConnection(), "metadata", [{"machine_id": "MACHINE_01"}])


def test_aucune_ligne():
    assert load_table(FakeConnection(), "machines", []) == 0
