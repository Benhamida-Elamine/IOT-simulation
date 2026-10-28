-- 4. Mesures générées par le simulateur (une ligne par machine et par cycle)
-- A exécuter après machine.sql : machine_id référence la table machines.
CREATE TABLE IF NOT EXISTS metadata (
    id BIGSERIAL PRIMARY KEY,
    machine_id VARCHAR(20) NOT NULL,
    temperature DOUBLE PRECISION,
    vibration DOUBLE PRECISION,
    rpm INTEGER,
    status VARCHAR(20),
    measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    FOREIGN KEY (machine_id)
        REFERENCES machines(machine_id)
);

CREATE INDEX IF NOT EXISTS idx_metadata_machine_time
    ON metadata (machine_id, measured_at);
