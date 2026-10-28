-- 1. Machines de référence (à exécuter en premier)
CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(20) PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    installation_date DATE NOT NULL
); 

INSERT INTO machines (
    machine_id,
    machine_name,
    machine_type,
    location,
    installation_date
)
VALUES
('MACHINE_01', 'Presse hydraulique 01', 'Press', 'LINE_A', '2022-03-15'),
('MACHINE_02', 'Moteur industriel 01', 'Motor', 'LINE_A', '2023-06-20'),
('MACHINE_03', 'Pompe industrielle 01', 'Pump', 'LINE_A', '2021-11-10'),
('MACHINE_04', 'Convoyeur 01', 'Conveyor', 'LINE_A', '2022-09-05'),
('MACHINE_05', 'Compresseur 01', 'Compressor', 'LINE_A', '2024-01-12'),
('MACHINE_06', 'Presse hydraulique 02', 'Press', 'LINE_B', '2023-02-18'),
('MACHINE_07', 'Moteur industriel 02', 'Motor', 'LINE_B', '2022-07-22'),
('MACHINE_08', 'Pompe industrielle 02', 'Pump', 'LINE_B', '2024-04-08'),
('MACHINE_09', 'Convoyeur 02', 'Conveyor', 'LINE_B', '2021-08-14'),
('MACHINE_10', 'Compresseur 02', 'Compressor', 'LINE_B', '2023-12-01'),
('MACHINE_11', 'Presse hydraulique 03', 'Press', 'LINE_C', '2020-05-17'),
('MACHINE_12', 'Moteur industriel 03', 'Motor', 'LINE_C', '2024-02-25'),
('MACHINE_13', 'Pompe industrielle 03', 'Pump', 'LINE_C', '2022-10-30'),
('MACHINE_14', 'Convoyeur 03', 'Conveyor', 'LINE_C', '2023-04-11'),
('MACHINE_15', 'Compresseur 03', 'Compressor', 'LINE_C', '2021-01-19'),
('MACHINE_16', 'Presse hydraulique 04', 'Press', 'LINE_A', '2024-06-03'),
('MACHINE_17', 'Moteur industriel 04', 'Motor', 'LINE_B', '2020-09-27'),
('MACHINE_18', 'Pompe industrielle 04', 'Pump', 'LINE_C', '2023-08-16'),
('MACHINE_19', 'Convoyeur 04', 'Conveyor', 'LINE_A', '2022-12-09'),
('MACHINE_20', 'Compresseur 04', 'Compressor', 'LINE_B', '2024-05-21')
ON CONFLICT (machine_id) DO NOTHING;