-- Table des prix historiques
CREATE TABLE IF NOT EXISTS prix_historique (
    id SERIAL PRIMARY KEY,
    ville VARCHAR(100) NOT NULL,
    quartier VARCHAR(100),
    date DATE NOT NULL,
    prix_m2 DECIMAL(10,2) NOT NULL,
    nb_transactions INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des projets urbains
CREATE TABLE IF NOT EXISTS projets_urbains (
    id SERIAL PRIMARY KEY,
    ville VARCHAR(100) NOT NULL,
    nom VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    description TEXT,
    date_prevue DATE,
    impact_estime VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Données de démonstration - Prix historiques
INSERT INTO prix_historique (ville, date, prix_m2, nb_transactions) VALUES
('Montpellier', '2023-04-01', 3100, 450),
('Montpellier', '2023-07-01', 3150, 520),
('Montpellier', '2023-10-01', 3200, 480),
('Montpellier', '2024-01-01', 3250, 510),
('Montpellier', '2024-04-01', 3300, 540),
('Toulouse', '2023-04-01', 3200, 620),
('Toulouse', '2023-07-01', 3280, 680),
('Toulouse', '2023-10-01', 3350, 650),
('Toulouse', '2024-01-01', 3400, 700),
('Toulouse', '2024-04-01', 3424, 720),
('Carcassonne', '2023-04-01', 1350, 120),
('Carcassonne', '2023-07-01', 1380, 135),
('Carcassonne', '2023-10-01', 1410, 128),
('Carcassonne', '2024-01-01', 1440, 140),
('Carcassonne', '2024-04-01', 1461, 145),
('Perpignan', '2023-04-01', 1580, 180),
('Perpignan', '2023-07-01', 1610, 195),
('Perpignan', '2023-10-01', 1640, 188),
('Perpignan', '2024-01-01', 1660, 200),
('Perpignan', '2024-04-01', 1675, 210);

-- Données de démonstration - Projets urbains
INSERT INTO projets_urbains (ville, nom, type, date_prevue, impact_estime) VALUES
('Montpellier', 'Extension ligne 5 tramway', 'Transport', '2025-06-01', 'positif'),
('Montpellier', 'Nouveau quartier Cambacérès', 'Urbanisme', '2025-12-01', 'positif'),
('Montpellier', 'Gare TGV Sud de France - Extension', 'Transport', '2026-03-01', 'très positif'),
('Toulouse', 'Ligne 3 métro', 'Transport', '2028-01-01', 'très positif'),
('Toulouse', 'Toulouse Aerospace Express', 'Transport', '2026-06-01', 'positif'),
('Toulouse', 'Écoquartier Guillaumet', 'Urbanisme', '2025-09-01', 'positif'),
('Perpignan', 'Rénovation centre-ville', 'Urbanisme', '2025-03-01', 'positif'),
('Perpignan', 'Nouveau parc des expositions', 'Infrastructure', '2025-12-01', 'positif'),
('Carcassonne', 'Zone commerciale La Bouriette', 'Commerce', '2025-06-01', 'positif');
