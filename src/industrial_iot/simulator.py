import random
from datetime import datetime, timezone

# Plages physiques autorisées pour la simulation.
PLAGES = {
    "temperature": {"min": 0, "max": 150},
    "vibration": {"min": 0, "max": 100},
    "rpm": {"min": 0, "max": 5000},
}

# Seuils d'alerte : ils doivent rester atteignables, donc inférieurs aux maximums des plages.
SEUILS_ALERTE = {"temperature": 100, "vibration": 50, "rpm": 4000}

# Force de rappel vers la valeur nominale (0 = marche aléatoire pure, 1 = retour immédiat).
# Sans ce rappel, la marche aléatoire dérive sans limite sur de longues durées.
RAPPEL = 0.05


def borner(value, parameter):
    """Ramène une valeur dans la plage autorisée du paramètre."""
    return max(PLAGES[parameter]["min"], min(PLAGES[parameter]["max"], value))


def determiner_statut(temperature, vibration, rpm):
    """Détermine le statut selon les règles de simulation."""
    if (
        temperature > SEUILS_ALERTE["temperature"]
        or vibration > SEUILS_ALERTE["vibration"]
        or rpm > SEUILS_ALERTE["rpm"]
    ):
        return "ALERT"
    if rpm == 0:
        return "STOPPED"
    return "RUNNING"


def generate_measurement(machine):
    """Génère une nouvelle mesure à partir de l'état précédent de la machine.

    Modèle : X_n = X_(n-1) + RAPPEL * (X_nominal - X_(n-1)) + bruit
    La valeur nominale est l'état initial de la machine ; elle est mémorisée au premier appel.
    """
    nominal = machine.setdefault("nominal", {
        "temperature": machine["temperature"],
        "vibration": machine["vibration"],
        "rpm": machine["rpm"],
    })

    temperature = machine["temperature"] + RAPPEL * (nominal["temperature"] - machine["temperature"]) + random.gauss(0, 0.3)
    vibration = machine["vibration"] + RAPPEL * (nominal["vibration"] - machine["vibration"]) + random.gauss(0, 0.1)
    rpm = machine["rpm"] + round(RAPPEL * (nominal["rpm"] - machine["rpm"])) + random.randint(-10, 10)

    temperature = borner(temperature, "temperature")
    vibration = borner(vibration, "vibration")
    rpm = int(borner(rpm, "rpm"))

    measurement = {
        "machine_id": machine["machine_id"],
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 3),
        "rpm": rpm,
        "status": determiner_statut(temperature, vibration, rpm),
        "timestamp": datetime.now(timezone.utc),
    }

    # Mettre à jour l'état de la machine pour le prochain cycle
    machine["temperature"] = temperature
    machine["vibration"] = vibration
    machine["rpm"] = rpm
    machine["status"] = measurement["status"]

    return measurement
