import argparse
import time
from concurrent.futures import ThreadPoolExecutor

from database import close_pool, insert_measurement
from measurements import measurements_init
from simulator import generate_measurement


def run(cycles=None, interval=10):
    """Génère une mesure par machine à chaque cycle et l'insère dans PostgreSQL.

    cycles=None : boucle infinie (Ctrl+C pour arrêter).
    """
    cycle = 0
    try:
        while cycles is None or cycle < cycles:
            # ThreadPoolExecutor() utiliser pour executer la fonction generate_measurement en parallele pour chaque machine.
            # Chaque thread modifie uniquement l'état de sa propre machine, il n'y a donc pas d'état partagé.
            with ThreadPoolExecutor() as executor:
                resultats = list(executor.map(generate_measurement, measurements_init))

            for resultat in resultats:
                try:
                    insert_measurement(resultat)
                    print(f"Inserted measurement for {resultat['machine_id']} at {resultat['timestamp']}")
                except Exception as e:
                    print(f"Error occurred while inserting measurement for {resultat['machine_id']}: {e}")

            cycle += 1
            if cycles is None or cycle < cycles:
                time.sleep(interval)  # Attendre avant de générer le prochain lot de mesures
    except KeyboardInterrupt:
        print("\nArrêt du simulateur.")
    finally:
        close_pool()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulateur IoT industriel")
    parser.add_argument("--cycles", type=int, default=None, help="nombre de cycles (par défaut : infini)")
    parser.add_argument("--interval", type=float, default=10, help="secondes entre deux cycles (défaut : 10)")
    args = parser.parse_args()
    run(cycles=args.cycles, interval=args.interval)
