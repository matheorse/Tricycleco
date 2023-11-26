-- Suppression des tables
DROP TABLE IF EXISTS Collecte;
DROP TABLE IF EXISTS Conteneur;
DROP TABLE IF EXISTS Tournee;
DROP TABLE IF EXISTS type_dechet;
DROP TABLE IF EXISTS Employe;
DROP TABLE IF EXISTS Camion;
DROP TABLE IF EXISTS se_compose;
DROP TABLE IF EXISTS se_termine;
DROP TABLE IF EXISTS Centre_recyclage;
DROP TABLE IF EXISTS Centre_collecte;

-- Création des tables
CREATE TABLE Camion(
   id_camion INT,
   immatriculation_camion VARCHAR(50),
   numero_camion INT,
   PRIMARY KEY(id_camion)
);

CREATE TABLE Centre_collecte(
   id_centre_collecte INT,
   lieu_collecte VARCHAR(50),
   PRIMARY KEY(id_centre_collecte)
);

CREATE TABLE Centre_recyclage(
   id_centre_recyclage INT,
   lieu_recyclage VARCHAR(50),
   PRIMARY KEY(id_centre_recyclage)
);

CREATE TABLE Employe(
   id_employe INT,
   numero_tel_employe INT,
   nom_employe VARCHAR(50),
   prenom_employe VARCHAR(50),
   adresse_employe VARCHAR(50),
   id_camion INT,
   PRIMARY KEY(id_employe),
   FOREIGN KEY(id_camion) REFERENCES Camion(id_camion)
);

CREATE TABLE type_dechet(
   id_type_dechet INT,
   libelle_type_dechet VARCHAR(50),
   PRIMARY KEY(id_type_dechet)
);

CREATE TABLE Tournee(
   id_tournee INT,
   date_tournee DATE,
   id_centre_recyclage INT NOT NULL,
   id_camion INT NOT NULL,
   temps TIME,
   PRIMARY KEY(id_tournee),
   FOREIGN KEY(id_centre_recyclage) REFERENCES Centre_recyclage(id_centre_recyclage),
   FOREIGN KEY(id_camion) REFERENCES Camion(id_camion)
);

CREATE TABLE Collecte(
   id_collecte INT,
   quantite_dechet_collecte INT,
   id_type_dechet INT NOT NULL,
   id_centre_collecte INT NOT NULL,
   id_tournee INT NOT NULL,
   PRIMARY KEY(id_collecte),
   FOREIGN KEY(id_type_dechet) REFERENCES type_dechet(id_type_dechet),
   FOREIGN KEY(id_centre_collecte) REFERENCES Centre_collecte(id_centre_collecte),
   FOREIGN KEY(id_tournee) REFERENCES Tournee(id_tournee)
);

CREATE TABLE Conteneur(
   id_conteneur INT,
   id_centre_collecte INT NOT NULL,
   id_type_dechet INT NOT NULL,
   id_centre_recyclage INT NOT NULL,
   PRIMARY KEY(id_conteneur),
   FOREIGN KEY(id_centre_collecte) REFERENCES Centre_collecte(id_centre_collecte),
   FOREIGN KEY(id_type_dechet) REFERENCES type_dechet(id_type_dechet),
   FOREIGN KEY(id_centre_recyclage) REFERENCES Centre_recyclage(id_centre_recyclage)
);

-- Insertion de données de test
INSERT INTO Camion VALUES (1, 'ABC123', 101);
INSERT INTO Camion VALUES (2, 'XYZ789', 102);

INSERT INTO Centre_collecte VALUES (1, 'Centre A');
INSERT INTO Centre_collecte VALUES (2, 'Centre B');

INSERT INTO Centre_recyclage VALUES (1, '14 rue de Paris');
INSERT INTO Centre_recyclage VALUES (2, '15 rue de Paris');

INSERT INTO Employe VALUES (1, 123456789, 'Lalai', 'Maria', '1 rue de Paris', 1);
INSERT INTO Employe VALUES (2, 987654321, 'Rose', 'Jean', '2 rue de Paris', 2);

INSERT INTO type_dechet VALUES (1, 'Bois');
INSERT INTO type_dechet VALUES (2, 'Aluminium');
INSERT INTO type_dechet VALUES (3, 'Plastique');
INSERT INTO type_dechet VALUES (4, 'Carton');
INSERT INTO type_dechet VALUES (5, 'Papier');
INSERT INTO type_dechet VALUES (6, 'Verre');
INSERT INTO type_dechet VALUES (7, 'Cuivre');
INSERT INTO type_dechet VALUES (8, 'Textile');

INSERT INTO Tournee VALUES (1, '2023-01-01', 1, 1, 35);
INSERT INTO Tournee VALUES (2, '2023-02-01', 2, 2, 40);
INSERT INTO Tournee VALUES (3, '2023-03-01', 1, 1, 30);
INSERT INTO Tournee VALUES (4, '2023-04-01', 2, 2, 45);
INSERT INTO Tournee VALUES (5, '2023-05-01', 1, 1, 35);
INSERT INTO Tournee VALUES (6, '2023-06-01', 2, 2, 40);
INSERT INTO Tournee VALUES (7, '2023-07-01', 1, 1, 30);
INSERT INTO Tournee VALUES (8, '2023-08-01', 2, 2, 50);



INSERT INTO Collecte VALUES (1, 100, 1, 1, 1);
INSERT INTO Collecte VALUES (2, 200, 2, 2, 2);
INSERT INTO Collecte Values (3, 300, 3, 3, 3);

INSERT INTO Conteneur VALUES (1, 1, 1, 1);
INSERT INTO Conteneur VALUES (2, 2, 2, 2);

-- Afficher qté tot collectée par type déchet
SELECT type_dechet.libelle_type_dechet, SUM(Collecte.quantite_dechet_collecte) AS total_quantite
FROM type_dechet
JOIN Collecte ON type_dechet.id_type_dechet = Collecte.id_type_dechet
GROUP BY type_dechet.libelle_type_dechet;

-- Afficher employés +  tournées
SELECT Employe.nom_employe, Employe.prenom_employe, Tournee.date_tournee, Tournee.id_tournee
FROM Employe
JOIN Tournee ON Employe.id_camion = Tournee.id_camion;
