-- Schéma MySQL de destination (data warehouse) du projet Industrial IoT.
-- Les colonnes reprennent celles des tables sources PostgreSQL (sql/db_sources).
-- A exécuter sur la base définie par MYSQL_DATABASE (ex. industrial_iot_dw).

CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(20) NOT NULL,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    installation_date DATE NOT NULL,
    PRIMARY KEY (machine_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id VARCHAR(30) NOT NULL,
    machine_id VARCHAR(20) NOT NULL,
    sensor_type VARCHAR(30) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    installation_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    PRIMARY KEY (sensor_id),
    CONSTRAINT fk_sensors_machines
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
) ENGINE=InnoDB;

-- id reprend l'identifiant source : relancer l'ETL met à jour les lignes au lieu de les dupliquer.
-- measured_at est stocké en UTC (DATETIME ne conserve pas de fuseau horaire).
CREATE TABLE IF NOT EXISTS metadata (
    id BIGINT NOT NULL,
    machine_id VARCHAR(20) NOT NULL,
    temperature DOUBLE NULL,
    vibration DOUBLE NULL,
    rpm INT NULL,
    status VARCHAR(20) NULL,
    measured_at DATETIME(6) NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_metadata_machine_time (machine_id, measured_at),
    CONSTRAINT fk_metadata_machines
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS maintenance (
    maintenance_id BIGINT NOT NULL,
    machine_id VARCHAR(20) NOT NULL,
    maintenance_date DATETIME(6) NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    technician VARCHAR(100) NOT NULL,
    cost_eur DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (maintenance_id),
    INDEX idx_maintenance_machine_date (machine_id, maintenance_date),
    CONSTRAINT fk_maintenance_machines
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
) ENGINE=InnoDB;
