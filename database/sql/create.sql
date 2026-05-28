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
    Credits INTEGER NOT NULL DEFAULT 0,
    AnneeAcademique VARCHAR(20)
);

-- Objet
CREATE TABLE Objet (
    Id SERIAL PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Description TEXT,
    Prix INTEGER NOT NULL CHECK (Prix >= 0)
);

-- Titre
CREATE TABLE Titre (
    Id INTEGER PRIMARY KEY REFERENCES Objet(Id) ON DELETE CASCADE
);

-- Badge
CREATE TABLE Badge (
    Id INTEGER PRIMARY KEY REFERENCES Objet(Id) ON DELETE CASCADE
);

-- Theme
CREATE TABLE Theme (
    Id INTEGER PRIMARY KEY REFERENCES Objet(Id) ON DELETE CASCADE
);

-- Cosmetique
CREATE TABLE Cosmetique (
    Id INTEGER PRIMARY KEY REFERENCES Objet(Id) ON DELETE CASCADE,
    Icone VARCHAR(255)
);

-- Table ObjetUtilisateur
CREATE TABLE ObjetUtilisateur (
    IdObjet INTEGER REFERENCES Objet(Id) ON DELETE CASCADE,
    IdUtilisateur INTEGER REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE,
    EstActif BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (IdObjet, IdUtilisateur)
);
-- Contribution
CREATE TABLE Contribution (
    Id SERIAL PRIMARY KEY,
    Date DATE NOT NULL DEFAULT CURRENT_DATE,
    IdUtilisateur INTEGER NOT NULL REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE,
    EstSupprime BOOLEAN NOT NULL DEFAULT FALSE
);

-- Résumé
CREATE TABLE Resume (
    Id INTEGER PRIMARY KEY REFERENCES Contribution(Id) ON DELETE RESTRICT,
    Titre VARCHAR(255) NOT NULL,
    Description TEXT,
    Fichier BYTEA,
    Version INTEGER NOT NULL DEFAULT 1 CHECK (Version >= 1),
    Visibilite VARCHAR(20) NOT NULL DEFAULT 'public' CHECK (Visibilite IN ('public', 'prive')),
    Code VARCHAR(20) NOT NULL REFERENCES Cours(Code)
);

-- Évaluation
CREATE TABLE Evaluation (
    Id INTEGER PRIMARY KEY REFERENCES Contribution(Id) ON DELETE RESTRICT,
    Note INTEGER CHECK (Note BETWEEN 1 AND 5),
    Commentaire TEXT,
    IdResume INTEGER NOT NULL REFERENCES Resume(Id) ON DELETE CASCADE
);

-- Transaction
CREATE TABLE Transaction (
    Id SERIAL PRIMARY KEY,
    Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Montant INTEGER NOT NULL,
    IdObjet INTEGER REFERENCES Objet(Id) ON DELETE SET NULL,
    IdUtilisateur INTEGER NOT NULL REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE,
    IdContribution INTEGER REFERENCES Contribution(Id) ON DELETE SET NULL
);

CREATE TABLE Leaderboard (
    IdUtilisateur INTEGER REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE,
    Annee INTEGER DEFAULT EXTRACT(year FROM CURRENT_DATE),
    PointsTotaux INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (IdUtilisateur, Annee)
);

CREATE INDEX idx_resume_cours ON Resume(Code);
CREATE INDEX idx_contribution_user ON Contribution(IdUtilisateur);
CREATE INDEX idx_evaluation_resume ON Evaluation(IdResume);
CREATE INDEX idx_transaction_user ON Transaction(IdUtilisateur);
CREATE INDEX idx_objet_utilisateur ON ObjetUtilisateur(IdUtilisateur);
CREATE INDEX idx_utilisateur_points ON Utilisateur(Points DESC);
CREATE INDEX idx_transaction_objet ON Transaction(IdObjet);
CREATE INDEX idx_contribution_user_resume ON Contribution(IdUtilisateur, Id);
CREATE INDEX idx_contribution_not_deleted ON Contribution(IdUtilisateur) WHERE EstSupprime = FALSE;
CREATE INDEX idx_leaderboard_annee_points ON Leaderboard(Annee, PointsTotaux DESC);