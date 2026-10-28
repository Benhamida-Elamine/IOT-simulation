-- Migration des données existantes (MySQL, data warehouse).
-- Même correction que 001 côté PostgreSQL, puis création des vues à jour.
-- Faire une sauvegarde avant de l'exécuter.

UPDATE metadata
SET machine_id = CONCAT('MACHINE_', RIGHT(machine_id, 2))
WHERE machine_id REGEXP '^MACHINE_00[0-9]{2}$';

ALTER TABLE metadata
    ADD CONSTRAINT fk_metadata_machines
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id);

-- Puis exécuter sql/db_destination/views/machine_summary.sql
-- et sql/db_destination/views/maintenance_summary.sql
