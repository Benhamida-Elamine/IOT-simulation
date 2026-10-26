-- MySQL destination schema for the Industrial IoT project.
-- IMPORTANT: This is a TEMPLATE. Verify source columns and types before running.
-- Run against the database selected by MYSQL_DATABASE (e.g. industrial_iot_dw).

CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NULL,
    machine_type VARCHAR(100) NULL,
    status VARCHAR(50) NULL,
    created_at DATETIME NULL,
    PRIMARY KEY (machine_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id VARCHAR(100) NOT NULL,
    machine_id VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(100) NULL,
    unit VARCHAR(50) NULL,
    installed_at DATETIME NULL,
    PRIMARY KEY (sensor_id),
    INDEX idx_sensors_machine_id (machine_id),
    CONSTRAINT fk_sensors_machine
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS metadata (
    measurement_id BIGINT NOT NULL AUTO_INCREMENT,
    machine_id VARCHAR(100) NOT NULL,
    temperature DOUBLE NULL,
    vibration DOUBLE NULL,
    rpm DOUBLE NULL,
    status VARCHAR(50) NULL,
    measured_at DATETIME NOT NULL,
    PRIMARY KEY (measurement_id),
    INDEX idx_metadata_machine_time (machine_id, measured_at),
    CONSTRAINT fk_metadata_machine
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS maintenance (
    maintenance_id BIGINT NOT NULL AUTO_INCREMENT,
    machine_id VARCHAR(100) NOT NULL,
    maintenance_date DATETIME NULL,
    maintenance_type VARCHAR(100) NULL,
    description TEXT NULL,
    duration_minutes INT NULL,
    status VARCHAR(50) NULL,
    PRIMARY KEY (maintenance_id),
    INDEX idx_maintenance_machine_date (machine_id, maintenance_date),
    CONSTRAINT fk_maintenance_machine
        FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
) ENGINE=InnoDB;
