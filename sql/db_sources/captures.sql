-- 2. Capteurs installés sur les machines
CREATE TABLE sensors (
    sensor_id VARCHAR(30) PRIMARY KEY,
    machine_id VARCHAR(20) NOT NULL,
    sensor_type VARCHAR(30) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    installation_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',

    FOREIGN KEY (machine_id)
        REFERENCES machines(machine_id),

    UNIQUE (machine_id, sensor_type)
); 



-- Capteurs de température
INSERT INTO sensors
    (sensor_id, machine_id, sensor_type, unit, installation_date)
SELECT
    machine_id || '_TEMP',
    machine_id,
    'TEMPERATURE',
    'degC',
    installation_date
FROM machines
ON CONFLICT DO NOTHING;

-- Capteurs de vibration
INSERT INTO sensors
    (sensor_id, machine_id, sensor_type, unit, installation_date)
SELECT
    machine_id || '_VIB',
    machine_id,
    'VIBRATION',
    'mm/s',
    installation_date
FROM machines
ON CONFLICT DO NOTHING;

-- Capteurs de vitesse de rotation
INSERT INTO sensors
    (sensor_id, machine_id, sensor_type, unit, installation_date)
SELECT
    machine_id || '_RPM',
    machine_id,
    'ROTATIONAL_SPEED',
    'rpm',
    installation_date
FROM machines
ON CONFLICT DO NOTHING;