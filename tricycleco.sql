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


CREATE TABLE Camion(
   id_camion INT ,
   immatriculation_camion VARCHAR(50),
   numero_camion INT,
   PRIMARY KEY(id_camion)
);

CREATE TABLE Centre_collecte(
   id_centre_collecte INT AUTO_INCREMENT,
   lieu_collecte VARCHAR(50),
   PRIMARY KEY(id_centre_collecte)
);

CREATE TABLE Centre_recyclage(
   id_centre_recyclage INT AUTO_INCREMENT,
   lieu_recyclage VARCHAR(50),
   PRIMARY KEY(id_centre_recyclage)
);

CREATE TABLE Employe(
   id_employe INT AUTO_INCREMENT,
   numero_telephone_employe INT,
   nom_employe VARCHAR(50),
   prenom_employe VARCHAR(50),
   salaire_employe NUMERIC,
   adresse_employe VARCHAR(50),
   id_camion INT,
   PRIMARY KEY(id_employe),
   FOREIGN KEY(id_camion) REFERENCES Camion(id_camion)
);

CREATE TABLE type_dechet(
   id_type_dechet INT AUTO_INCREMENT,
   libelle_type_dechet VARCHAR(50),
   PRIMARY KEY(id_type_dechet)
);

CREATE TABLE Tournee(
   id_tournee INT AUTO_INCREMENT,
   date_tournee DATE,
   id_centre_recyclage INT NOT NULL,
   id_camion INT NOT NULL,
   temps TIME,
   PRIMARY KEY(id_tournee),
   FOREIGN KEY(id_centre_recyclage) REFERENCES Centre_recyclage(id_centre_recyclage),
   FOREIGN KEY(id_camion) REFERENCES Camion(id_camion)
);

CREATE TABLE Collecte(
   id_collecte INT AUTO_INCREMENT,
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
   id_conteneur INT AUTO_INCREMENT,
   id_centre_collecte INT NOT NULL,
   id_type_dechet INT NOT NULL,
   id_centre_recyclage INT NOT NULL,
   PRIMARY KEY(id_conteneur),
   FOREIGN KEY(id_centre_collecte) REFERENCES Centre_collecte(id_centre_collecte),
   FOREIGN KEY(id_type_dechet) REFERENCES type_dechet(id_type_dechet),
   FOREIGN KEY(id_centre_recyclage) REFERENCES Centre_recyclage(id_centre_recyclage)
);

INSERT INTO Camion VALUES (1, 'ABC123', 101);
INSERT INTO Camion VALUES (2, 'XYZ789', 102);
INSERT INTO Camion VALUES (3, 'DEF456', 103);
INSERT INTO Camion VALUES (4, 'GHI157', 104);
INSERT INTO Camion VALUES (5, 'JKL945', 105);
INSERT INTO Camion VALUES (6, 'MNO849', 106);

INSERT INTO Centre_collecte VALUES (1, 'Paris Nord');
INSERT INTO Centre_collecte VALUES (2, 'Lyon Ouest');
INSERT INTO Centre_collecte VALUES (3, 'Marseille Est');
INSERT INTO Centre_collecte VALUES (4, 'Bordeaux Sud');
INSERT INTO Centre_collecte VALUES (5, 'Lille Centre');
INSERT INTO Centre_collecte VALUES (6, 'Toulouse Nord');
INSERT INTO Centre_collecte VALUES (7, 'Nice Ouest');
INSERT INTO Centre_collecte VALUES (8, 'Strasbourg Sud');

INSERT INTO Centre_recyclage VALUES (1, '14 rue de Paris');
INSERT INTO Centre_recyclage VALUES (2, '2 rue de Belfort');
INSERT INTO Centre_recyclage VALUES (4, '7 rue Marconi');
INSERT INTO Centre_recyclage VALUES (5, '28 rue Branly');


INSERT INTO Employe VALUES (1, 123456789, 'Doe', 'John', 50000, '123 Main St', 1);
INSERT INTO Employe VALUES (2, 987654321, 'Smith', 'Jane', 55000, '456 Oak St', 2);
INSERT INTO Employe VALUES (3, 555555555, 'Johnson', 'Bob', 48000, '789 Pine St', 3);
INSERT INTO Employe VALUES (4, 111222333, 'Williams', 'Emily', 60000, '101 Cedar St', 1);
INSERT INTO Employe VALUES (5, 999888777, 'Davis', 'Mike', 52000, '202 Elm St', 2);
INSERT INTO Employe VALUES (6, 444333222, 'Brown', 'Amy', 47000, '303 Maple St', 3);
INSERT INTO Employe VALUES (7, 666666666, 'Miller', 'David', 58000, '404 Birch St', 1);
INSERT INTO Employe VALUES (8, 777777777, 'Wilson', 'Jessica', 51000, '505 Spruce St', 2);
INSERT INTO Employe VALUES (9, 222222222, 'Moore', 'Kevin', 49000, '606 Pine St', 3);
INSERT INTO Employe VALUES (10, 888888888, 'Taylor', 'Sophie', 57000, '707 Cedar St', 1);
INSERT INTO Employe VALUES (11, 333333333, 'Anderson', 'Ryan', 53000, '808 Oak St', 2);
INSERT INTO Employe VALUES (12, 444444444, 'Martin', 'Lily', 46000, '909 Elm St', 3);


INSERT INTO type_dechet VALUES (1, 'Bois');
INSERT INTO type_dechet VALUES (2, 'Aluminium');
INSERT INTO type_dechet VALUES (3, 'Plastique');
INSERT INTO type_dechet VALUES (4, 'Carton');
INSERT INTO type_dechet VALUES (5, 'Papier');
INSERT INTO type_dechet VALUES (6, 'Verre');
INSERT INTO type_dechet VALUES (7, 'Cuivre');
INSERT INTO type_dechet VALUES (8, 'Textile');

INSERT INTO Tournee VALUES (1, '2023-02-01', 2, 2, 40);
INSERT INTO Tournee VALUES (2,'2023-03-01', 1, 1, 45);
INSERT INTO Tournee VALUES (3,'2023-04-01', 2, 2, 30);
INSERT INTO Tournee VALUES (4,'2023-01-01', 1, 1, 35);
INSERT INTO Tournee VALUES (5,'2023-05-01', 1, 1, 35);
INSERT INTO Tournee VALUES (6,'2023-06-01', 2, 2, 40);
INSERT INTO Tournee VALUES (7,'2023-07-01', 1, 1, 30);
INSERT INTO Tournee VALUES (8,'2023-08-01', 2, 2, 50);
INSERT INTO Tournee VALUES (9,'2023-10-01', 2, 2, 30);
INSERT INTO Tournee VALUES (10,'2023-09-01', 2, 2, 25);
INSERT INTO Tournee VALUES (11,'2023-08-01', 2, 2, 35);


INSERT INTO Collecte VALUES (1, 273, 1, 1, 1);
INSERT INTO Collecte VALUES (2, 089, 2, 2, 2);
INSERT INTO Collecte Values (3, 358, 3, 3, 3);
INSERT INTO Collecte Values (4, 424, 4, 4, 4);
INSERT INTO Collecte Values (5, 289, 5, 5, 5);
INSERT INTO Collecte Values (6, 681, 6, 6, 6);
INSERT INTO Collecte Values (7, 602, 7, 7, 7);
INSERT INTO Collecte Values (8, 456, 8, 8, 8);

INSERT INTO Conteneur VALUES (1, 1, 1, 1);
INSERT INTO Conteneur VALUES (2, 2, 2, 2);

SELECT type_dechet.libelle_type_dechet, SUM(Collecte.quantite_dechet_collecte) AS total_quantite
FROM type_dechet
JOIN Collecte ON type_dechet.id_type_dechet = Collecte.id_type_dechet
GROUP BY type_dechet.libelle_type_dechet;

SELECT Employe.nom_employe, Employe.prenom_employe, Tournee.date_tournee, Tournee.id_tournee
FROM Employe
JOIN Tournee ON Employe.id_camion = Tournee.id_camion;

SELECT Conteneur.id_conteneur AS id, Centre_collecte.lieu_collecte AS collecte, td.libelle_type_dechet AS type, Centre_recyclage.lieu_recyclage AS recyclage
FROM Conteneur
INNER JOIN Centre_recyclage ON Conteneur.id_centre_recyclage = Centre_recyclage.id_centre_recyclage
INNER JOIN type_dechet td ON Conteneur.id_type_dechet = td.id_type_dechet
INNER JOIN Centre_collecte ON Conteneur.id_centre_collecte = Centre_collecte.id_centre_collecte
ORDER BY Conteneur.id_conteneur;

SELECT id_type_dechet AS id, libelle_type_dechet AS libelle
             FROM type_dechet;


