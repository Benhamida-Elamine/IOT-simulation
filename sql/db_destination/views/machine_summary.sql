-- Synthèse par machine.
-- Les mesures sont agrégées dans une sous-requête séparée pour éviter
-- de multiplier les lignes lors de la jointure avec les autres tables.

CREATE OR REPLACE VIEW machine_summary AS
SELECT
    m.machine_id,
    m.machine_name,
    m.machine_type,
    m.location,
    COALESCE(md.measurement_count, 0) AS measurement_count,
    md.last_measured_at,
    md.avg_temperature,
    md.max_temperature,
    md.avg_vibration,
    md.max_vibration,
    md.avg_rpm
FROM machines AS m
LEFT JOIN (
    SELECT
        machine_id,
        COUNT(*) AS measurement_count,
        MAX(measured_at) AS last_measured_at,
        AVG(temperature) AS avg_temperature,
        MAX(temperature) AS max_temperature,
        AVG(vibration) AS avg_vibration,
        MAX(vibration) AS max_vibration,
        AVG(rpm) AS avg_rpm
    FROM metadata
    GROUP BY machine_id
) AS md
    ON md.machine_id = m.machine_id;
