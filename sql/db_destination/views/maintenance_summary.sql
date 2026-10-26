-- Maintenance metrics per machine, joined to pre-aggregated measurements.
-- This avoids a many-to-many fan-out between raw metadata and maintenance rows.
-- Adapt column names to the real MySQL schema before creating this view.

CREATE OR REPLACE VIEW maintenance_summary AS
SELECT
    m.machine_id,
    COALESCE(mt.maintenance_count, 0) AS maintenance_count,
    mt.last_maintenance_at,
    mt.total_downtime_minutes,
    md.last_measured_at,
    md.avg_temperature,
    md.avg_vibration
FROM machines AS m
LEFT JOIN (
    SELECT
        machine_id,
        COUNT(*) AS maintenance_count,
        MAX(maintenance_date) AS last_maintenance_at,
        SUM(COALESCE(duration_minutes, 0)) AS total_downtime_minutes
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
