import random
from datetime import datetime, timezone


def generate_measurement(machine):
    temperature = machine["temperature"] + random.gauss(0, 0.3)
    vibration = machine["vibration"] + random.gauss(0, 0.1)
    rpm = machine["rpm"] + random.randint(-10, 10)
    
    temperature = max(0, min(100, temperature))
    vibration = max(0, vibration)
    rpm = max(0, max(0, min(5000, rpm)))

    measurement = {
        "machine_id": machine["machine_id"],
        "temperature": temperature,
        "vibration": vibration,
        "rpm": machine["rpm"],
        "status": machine["status"],
        "timestamp": datetime.now(timezone.utc),
    }
      # Déterminer le statut selon les règles de simulation
    if (
           measurement["temperature"] > 100
           or measurement["vibration"] > 50
           or measurement["rpm"] > 4000
       ):
           measurement["status"] = "ALERT"
    elif measurement["rpm"] == 0:
           measurement["status"] = "STOPPED"
    else:
           measurement["status"] = "RUNNING"



    # Mettre à jour l'état de la machine pour le prochain cycle
    machine["temperature"] = temperature
    machine["vibration"] = vibration
    machine["rpm"] = rpm 
    machine["status"] = measurement["status"]

    return measurement




## État initial de la machine ( exemple pour la premiere machine ) 
#machine_0002 = {
#    "machine_id": "MACHINE_0002",
#    "timestamp": "2026-10-03T12:00:00Z",
#    "temperature_c": 71.9,
#    "vib_m_s": 3.3,
#    "rpm": 1500,
#    "status": "RUNNING"
#}
#
#
#class MesureIoT:
#
#    def __init__(self):
#        # Plages définies pour notre simulation
#        self.plages = {
#            "temperature_c": {"min": 0, "max": 150},
#            "vib_m_s": {"min": 0, "max": 100},
#            "rpm": {"min": 0, "max": 5000}
#        }
#
#    def generate_measurement(self, previous_data: dict) -> dict:
#        """Génère une nouvelle mesure à partir de l'état précédent. 
#           le modele utiliser pour la generation des donnees est X_n = X_(n-1) + random_noise, ou random_noise est un bruit aleatoire.
#        """
#
#        new_data = {
#            "machine_id": previous_data["machine_id"],
#            "timestamp": datetime.now(timezone.utc).isoformat().replace(
#                "+00:00", "Z"
#            )
#        }
#
#        # Générer les nouvelles valeurs
#        new_data["temperature_c"] = (
#            previous_data["temperature_c"] + random.uniform(-1, 1)
#        )
#
#        new_data["vib_m_s"] = (
#            previous_data["vib_m_s"] + random.uniform(-0.2, 0.2)
#        )
#
#        new_data["rpm"] = max(
#            0,
#            previous_data["rpm"] + random.randint(-10, 10)
#        )
#
#        # Appliquer les limites définies
#        for parameter in ["temperature_c", "vib_m_s", "rpm"]:
#            minimum = self.plages[parameter]["min"]
#            maximum = self.plages[parameter]["max"]
#
#            new_data[parameter] = max(
#                minimum, min(new_data[parameter], maximum)
#            )
#
#        # Déterminer le statut selon les règles de simulation
#        if (
#            new_data["temperature_c"] > 100
#            or new_data["vib_m_s"] > 50
#            or new_data["rpm"] > 4000
#        ):
#            new_data["status"] = "ALERT"
#
#        elif new_data["rpm"] == 0:
#            new_data["status"] = "STOPPED"
#
#        else:
#            new_data["status"] = "RUNNING" 
#
#            
#
#        return new_data