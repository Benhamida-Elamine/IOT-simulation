import copy
import random

from measurements import measurements_init
from simulator import PLAGES, determiner_statut, generate_measurement


def nouvelle_machine():
    return copy.deepcopy(measurements_init[0])


def test_rpm_emis_correspond_au_nouvel_etat():
    # Régression : l'ancien code renvoyait le rpm du cycle précédent.
    random.seed(1)
    machine = nouvelle_machine()
    for _ in range(20):
        measurement = generate_measurement(machine)
        assert measurement["rpm"] == machine["rpm"]
        assert measurement["temperature"] == round(machine["temperature"], 2)


def test_valeurs_dans_les_plages():
    random.seed(2)
    machine = nouvelle_machine()
    for _ in range(5000):
        measurement = generate_measurement(machine)
        for parameter in ("temperature", "vibration", "rpm"):
            assert PLAGES[parameter]["min"] <= measurement[parameter] <= PLAGES[parameter]["max"]


def test_pas_de_derive_sur_une_longue_simulation():
    # Régression : la marche aléatoire pure dérivait (température observée de 8 à 100 °C).
    random.seed(3)
    machine = nouvelle_machine()
    nominal = machine["temperature"]
    temperatures = [generate_measurement(machine)["temperature"] for _ in range(20000)]
    assert max(abs(t - nominal) for t in temperatures) < 5


def test_statuts_atteignables():
    assert determiner_statut(120, 3, 1500) == "ALERT"
    assert determiner_statut(70, 60, 1500) == "ALERT"
    assert determiner_statut(70, 3, 4500) == "ALERT"
    assert determiner_statut(70, 3, 0) == "STOPPED"
    assert determiner_statut(70, 3, 1500) == "RUNNING"


def test_identifiants_presents_dans_la_table_machines():
    references = {f"MACHINE_{i:02d}" for i in range(1, 21)}
    assert {m["machine_id"] for m in measurements_init} <= references
