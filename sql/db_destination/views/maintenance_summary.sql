-- Indicateurs de maintenance par machine, joints aux mesures pré-agrégées.
-- Les deux agrégations sont séparées pour éviter un produit cartésien
-- entre les mesures brutes et les interventions.

CREATE OR REPLACE VIEW maintenance_summary AS
SELECT
    m.machine_id,
    m.machine_name,
    COALESCE(mt.maintenance_count, 0) AS maintenance_count,
    mt.last_maintenance_at,
    COALESCE(mt.total_cost_eur, 0) AS total_cost_eur,
    md.last_measured_at,
    md.avg_temperature,
    md.avg_vibration
FROM machines AS m
LEFT JOIN (
    SELECT
        machine_id,
        COUNT(*) AS maintenance_count,
        MAX(maintenance_date) AS last_maintenance_at,
        SUM(cost_eur) AS total_cost_eur
    FROM maintenance
    GROUP BY machine_id
) AS mt
    ON mt.machine_id = m.machine_id
LEFT JOIN (
    SELECT
        machine_id,
        MAX(measured_at) AS last_measured_at,
        AVG(temperature) AS avg_temperature,
        AVG(vibration) AS avg_vibration
    FROM metadata
    GROUP BY machine_id
) AS md
    ON md.machine_id = m.machine_id;
