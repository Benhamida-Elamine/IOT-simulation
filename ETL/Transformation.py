
from datetime import datetime, timezone
from math import isfinite


def clean_text(value):
    """Nettoie une valeur texte sans modifier les autres types."""
    if isinstance(value, str):
        value = value.strip()
        return value if value else None

    return value


def to_utc_naive(value):
    """Convertit une date avec fuseau horaire en UTC sans fuseau.

    Le type DATETIME de MySQL ne conserve pas le fuseau horaire :
    on stocke donc toutes les dates en UTC pour qu'elles restent comparables.
    """
    if isinstance(value, datetime) and value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    return value


def clean_value(value):
    """Nettoie le texte et normalise les dates."""
    return to_utc_naive(clean_text(value))


def remove_duplicates(rows, key_columns):
    """Supprime les doublons en conservant la première occurrence."""
    seen = set()
    cleaned_rows = []

    for row in rows:
        key = tuple(row.get(column) for column in key_columns)

        # Ne pas supprimer les lignes dont la clé est incomplète.
        if any(value is None for value in key):
            cleaned_rows.append(row)
            continue

        if key not in seen:
            seen.add(key)
            cleaned_rows.append(row)

    return cleaned_rows


def transform_machines(rows):
    """Nettoie les données des machines."""
    cleaned_rows = []

    for row in rows:
        row = {
            column: clean_value(value)
            for column, value in row.items()
        }

        if row.get("machine_id") is None:
            continue

        cleaned_rows.append(row)

    return remove_duplicates(cleaned_rows, ["machine_id"])


def transform_sensors(rows):
    """Nettoie les données des capteurs."""
    cleaned_rows = []

    for row in rows:
        row = {
            column: clean_value(value)
            for column, value in row.items()
        }

        if row.get("sensor_id") is None:
            continue

        cleaned_rows.append(row)

    return remove_duplicates(cleaned_rows, ["sensor_id"])


def transform_metadata(rows):
    """Valide et nettoie les mesures des machines."""
    cleaned_rows = []

    for row in rows:
        row = {
            column: clean_value(value)
            for column, value in row.items()
        }

        # Une mesure doit être associée à une machine et à une date.
        if row.get("machine_id") is None:
            continue

        measured_at = row.get("measured_at")
        if not isinstance(measured_at, datetime):
            continue

        # Les mesures numériques doivent être convertibles
        # et finies : pas de NaN ni d'infini.
        valid = True

        for column in ("temperature", "vibration", "rpm"):
            value = row.get(column)

            if value is None:
                valid = False
                break

            try:
                number = float(value)
            except (TypeError, ValueError):
                valid = False
                break

            if not isfinite(number):
                valid = False
                break

            if column == "rpm" and number < 0:
                valid = False
                break

            row[column] = int(number) if column == "rpm" else number

        if not valid:
            continue

        cleaned_rows.append(row)

    return remove_duplicates(
        cleaned_rows,
        ["machine_id", "measured_at"]
    )


def transform_maintenance(rows):
    """Nettoie les données de maintenance."""
    cleaned_rows = []

    for row in rows:
        row = {
            column: clean_value(value)
            for column, value in row.items()
        }

        if row.get("machine_id") is None:
            continue

        cleaned_rows.append(row)

    # À adapter selon la véritable clé primaire de maintenance.
    if rows and "maintenance_id" in rows[0]:
        return remove_duplicates(cleaned_rows, ["maintenance_id"])

    return cleaned_rows
