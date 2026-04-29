-- Extensions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Utilisateur
CREATE TABLE Utilisateur (
    IdUtilisateur SERIAL PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL,
    DateInscription DATE NOT NULL DEFAULT CURRENT_DATE,
    Points INTEGER NOT NULL DEFAULT 0 CHECK (Points >= 0),
    Niveau INTEGER NOT NULL DEFAULT 1 CHECK (Niveau >= 1)
);

-- Cours
CREATE TABLE Cours (
    Code VARCHAR(20) PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL,
    Faculte VARCHAR(255) NOT NULL,
    Credits INTEGER NOT NULL DEFAULT 0
);
-- Année académique
CREATE TABLE AnneeAcademique (
    PeriodeAcademique VARCHAR(20) PRIMARY KEY
);

-- Cours par année
CREATE TABLE CoursParAnnee (
    Code VARCHAR(20) REFERENCES Cours(Code),
    PeriodeAcademique VARCHAR(20) REFERENCES AnneeAcademique(PeriodeAcademique),
    PRIMARY KEY (Code, PeriodeAcademique)
);

-- Objet cosmétique
CREATE TABLE ObjetCosmetique (
    Id SERIAL PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Description TEXT,
    Prix INTEGER NOT NULL CHECK (Prix >= 0)
);

-- Titre
CREATE TABLE Titre (
    Id INTEGER PRIMARY KEY REFERENCES ObjetCosmetique(Id)
);

-- Badge
CREATE TABLE Badge (
    Id INTEGER PRIMARY KEY REFERENCES ObjetCosmetique(Id),
    Image VARCHAR(255)
);

-- Theme
CREATE TABLE Theme (
    Id INTEGER PRIMARY KEY REFERENCES ObjetCosmetique(Id),
    Image VARCHAR(255)
);

-- Objet possédé par utilisateur
CREATE TABLE ObjetUtilisateur (
    IdObjetCosmetique INTEGER REFERENCES ObjetCosmetique(Id),
    IdUtilisateur INTEGER REFERENCES Utilisateur(IdUtilisateur),
    EstActif BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (IdObjetCosmetique, IdUtilisateur)
);

-- Contribution
CREATE TABLE Contribution (
    Id SERIAL PRIMARY KEY,
    Date DATE NOT NULL DEFAULT CURRENT_DATE,
    IdUtilisateur INTEGER NOT NULL REFERENCES Utilisateur(IdUtilisateur)
);

-- Résumé
CREATE TABLE Resume (
    Id INTEGER PRIMARY KEY REFERENCES Contribution(Id),
    Titre VARCHAR(255) NOT NULL,
    Description TEXT,
    Version INTEGER NOT NULL DEFAULT 1 CHECK (Version >= 1),
    Visibilite VARCHAR(20) NOT NULL DEFAULT 'public' CHECK (Visibilite IN ('public', 'prive')),
    Code VARCHAR(20) NOT NULL REFERENCES Cours(Code)
);

-- Évaluation
CREATE TABLE Evaluation (
    Id INTEGER PRIMARY KEY REFERENCES Contribution(Id),
    Note INTEGER CHECK (Note BETWEEN 1 AND 5),
    Commentaire TEXT,
    IdResume INTEGER NOT NULL REFERENCES Resume(Id)
);

-- Transaction
CREATE TABLE Transaction (
    Id SERIAL PRIMARY KEY,
    Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Montant INTEGER NOT NULL,
    IdObjetCosmetique INTEGER REFERENCES ObjetCosmetique(Id),
    IdUtilisateur INTEGER NOT NULL REFERENCES Utilisateur(IdUtilisateur),
    IdContribution INTEGER REFERENCES Contribution(Id)
);

-- Leaderboard
CREATE TABLE Leaderboard (
    Periode VARCHAR(20),
    IdUtilisateur INTEGER REFERENCES Utilisateur(IdUtilisateur),
    PointsTotal INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (Periode, IdUtilisateur)
);

-- Index utiles
CREATE INDEX idx_resume_cours ON Resume(Code);
CREATE INDEX idx_contribution_user ON Contribution(IdUtilisateur);
CREATE INDEX idx_evaluation_resume ON Evaluation(IdResume);
CREATE INDEX idx_transaction_user ON Transaction(IdUtilisateur);