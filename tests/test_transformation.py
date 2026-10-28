from datetime import datetime, timedelta, timezone

from Transformation import remove_duplicates, to_utc_naive, transform_machines, transform_metadata

PARIS_ETE = timezone(timedelta(hours=2))


def mesure(**valeurs):
    row = {
        "id": 1,
        "machine_id": "MACHINE_01",
        "temperature": 72.5,
        "vibration": 3.2,
        "rpm": 1500,
        "status": "RUNNING",
        "measured_at": datetime(2026, 10, 5, 12, 0, tzinfo=PARIS_ETE),
    }
    row.update(valeurs)
    return row


def test_conversion_utc():
    assert to_utc_naive(datetime(2026, 10, 5, 12, 0, tzinfo=PARIS_ETE)) == datetime(2026, 10, 5, 10, 0)
    assert to_utc_naive("texte") == "texte"


def test_mesure_valide_conservee_et_normalisee():
    [row] = transform_metadata([mesure()])
    assert row["measured_at"] == datetime(2026, 10, 5, 10, 0)
    assert row["rpm"] == 1500 and isinstance(row["rpm"], int)


def test_mesures_invalides_rejetees():
    rows = [
        mesure(machine_id=None),
        mesure(machine_id="   "),
        mesure(measured_at=None),
        mesure(temperature=float("nan")),
        mesure(vibration="abc"),
        mesure(rpm=-5),
        mesure(temperature=None),
    ]
    assert transform_metadata(rows) == []


def test_doublons_supprimes():
    rows = transform_metadata([mesure(id=1), mesure(id=2)])
    assert [row["id"] for row in rows] == [1]


def test_remove_duplicates_garde_les_cles_incompletes():
    rows = [{"k": None}, {"k": None}, {"k": 1}, {"k": 1}]
    assert remove_duplicates(rows, ["k"]) == [{"k": None}, {"k": None}, {"k": 1}]


def test_transform_machines_nettoie_le_texte():
    rows = transform_machines([{"machine_id": " MACHINE_01 ", "machine_name": "  "}])
    assert rows == [{"machine_id": "MACHINE_01", "machine_name": None}]
