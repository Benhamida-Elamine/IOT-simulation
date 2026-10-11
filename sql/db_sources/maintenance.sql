-- 3. Historique des interventions de maintenance
CREATE TABLE maintenance (
    maintenance_id varchar(30) PRIMARY KEY,
    machine_id VARCHAR(30) NOT NULL,
    maintenance_date TIMESTAMPTZ NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    technician VARCHAR(100) NOT NULL,
    cost_eur NUMERIC(10, 2) NOT NULL,

    FOREIGN KEY (machine_id)
        REFERENCES machines(machine_id),

    CHECK (cost_eur >= 0)
); 


INSERT INTO maintenance (
    machine_id,
    maintenance_date,
    maintenance_type,
    description,
    technician,
    cost_eur
)
VALUES
    ('MACHINE_01', '2025-01-15 09:00:00+01', 'PREVENTIVE',
     'Remplacement de l''huile hydraulique', 'Technicien A', 420.00),

    ('MACHINE_03', '2025-02-10 14:30:00+01', 'CORRECTIVE',
     'Remplacement du joint de pompe', 'Technicien B', 680.00),

    ('MACHINE_07', '2025-03-04 08:15:00+01', 'PREVENTIVE',
     'Inspection des roulements moteur', 'Technicien C', 250.00),

    ('MACHINE_09', '2025-04-22 11:00:00+02', 'CORRECTIVE',
     'Alignement de la bande transporteuse', 'Technicien A', 310.00),

    ('MACHINE_12', '2025-05-13 10:00:00+02', 'PREVENTIVE',
     'Inspection du système de refroidissement', 'Technicien D', 190.00),

    ('MACHINE_15', '2025-06-02 15:45:00+02', 'CORRECTIVE',
     'Remplacement du filtre du compresseur', 'Technicien B', 540.00),

    ('MACHINE_18', '2025-07-19 07:30:00+02', 'PREVENTIVE',
     'Inspection des vibrations de la pompe', 'Technicien C', 230.00),

    ('MACHINE_20', '2025-08-08 13:00:00+02', 'CORRECTIVE',
     'Remplacement de la valve de pression', 'Technicien D', 760.00);