--Utilisateur
CREATE TABLE Utilisateur (
    IdUtilisateur SERIAL PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL, --On va l'hacher et puis le stocker 
    DateInscription DATE NOT NULL DEFAULT CURRENT_DATE,
    Points INTEGER NOT NULL DEFAULT 0 CHECK (Points >= 0),
    Niveau INTEGER NOT NULL DEFAULT 1 CHECK (Niveau >= 1)
);

-- Cours
CREATE TABLE Cours (
    Code VARCHAR(20) PRIMARY KEY,
    Nom VARCHAR(255) NOT NULL,
    Faculte VARCHAR(255) NOT NULL
);


-- Objet cosmétique
CREATE TABLE ObjetCosmetique (
    Id SERIAL PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Description TEXT,
    Prix INTEGER NOT NULL CHECK (Prix > 0)
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

-- Cosmetique
CREATE TABLE Cosmetique (
    Id INTEGER PRIMARY KEY REFERENCES ObjetCosmetique(Id),
    Icone VARCHAR(255)
);

-- Objet possédé par utilisateur
CREATE TABLE ObjetUtilisateur (
    IdObjetCosmetique INTEGER REFERENCES ObjetCosmetique(Id) ON DELETE RESTRICT,
    IdUtilisateur INTEGER REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE,
    EstActif BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (IdObjetCosmetique, IdUtilisateur)
);

-- Contribution
CREATE TABLE Contribution (
    Id SERIAL PRIMARY KEY,
    Date DATE NOT NULL DEFAULT CURRENT_DATE,
    IdUtilisateur INTEGER NOT NULL REFERENCES Utilisateur(IdUtilisateur) ON DELETE CASCADE
);

-- Résumé
CREATE TABLE Resume (
    Id INTEGER PRIMARY KEY REFERENCES Contribution(Id) ON DELETE CASCADE,
    Titre VARCHAR(255) NOT NULL,
    Description TEXT,
    Version INTEGER NOT NULL DEFAULT 1 CHECK (Version >= 1),
    Visibilite VARCHAR(20) NOT NULL DEFAULT 'public' CHECK (Visibilite IN ('public', 'prive')),
    Code VARCHAR(20) NOT NULL REFERENCES Cours(Code)
);

-- Évaluation
CREATE TABLE Evaluation (
    Id INTEGER PRIMARY KEY REFERENCES Contribution(Id) ON DELETE CASCADE,
    Note INTEGER CHECK (Note BETWEEN 1 AND 5),
    Commentaire TEXT,
    IdResume INTEGER NOT NULL REFERENCES Resume(Id) ON DELETE CASCADE,
    CHECK (Note IS NOT NULL OR Commentaire IS NOT NULL)
);

-- Transaction
CREATE TABLE Transaction (
    Id SERIAL PRIMARY KEY,
    Date DATE NOT NULL DEFAULT CURRENT_DATE,
    Montant INTEGER NOT NULL,
    IdObjetCosmetique INTEGER REFERENCES ObjetCosmetique(Id) ON DELETE RESTRICT,
    IdUtilisateur INTEGER NOT NULL REFERENCES Utilisateur(IdUtilisateur) ON DELETE RESTRICT,
    IdContribution INTEGER REFERENCES Contribution(Id) ON DELETE SET NULL,
    Type VARCHAR(20) NOT NULL CHECK (Type IN ('gain', 'depense')),
    CHECK (
        (Type = 'gain' AND Montant > 0) 
        OR 
        (Type = 'depense' AND Montant < 0)
    )
);


-- Index utiles
CREATE INDEX idx_resume_cours ON Resume(Code);
CREATE INDEX idx_contribution_user ON Contribution(IdUtilisateur);
CREATE INDEX idx_evaluation_resume ON Evaluation(IdResume);
CREATE INDEX idx_transaction_user ON Transaction(IdUtilisateur);
CREATE INDEX idx_transaction_objet ON Transaction(IdObjetCosmetique);

-- Trigger qui empêche un utilisateur d'évaluer son 
--propre résumé
CREATE OR REPLACE FUNCTION check_self_evaluation()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT IdUtilisateur FROM Contribution WHERE Id = NEW.Id) =
     (SELECT IdUtilisateur FROM Contribution WHERE Id = NEW.IdResume) THEN
    RAISE EXCEPTION 'Un utilisateur ne peut pas évaluer son propre résumé';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_no_self_eval
BEFORE INSERT ON Evaluation
FOR EACH ROW EXECUTE FUNCTION check_self_evaluation();

--Trigger pour s'assurer qu'un seul titre est actif à la fois
CREATE OR REPLACE FUNCTION check_single_active_titre()
RETURNS TRIGGER AS $$
BEGIN
  -- Seulement si on essaie d'activer un objet (EstActif = TRUE)
  IF NEW.EstActif = TRUE THEN
    -- Vérifie que cet objet est bien un Titre
    IF EXISTS (SELECT 1 FROM Titre WHERE Id = NEW.IdObjetCosmetique) THEN
      -- Vérifie qu'il n'y a pas déjà un titre actif pour cet utilisateur
      IF EXISTS (
        SELECT 1 FROM ObjetUtilisateur ou
        JOIN Titre t ON t.Id = ou.IdObjetCosmetique
        WHERE ou.IdUtilisateur = NEW.IdUtilisateur
          AND ou.EstActif = TRUE
          AND ou.IdObjetCosmetique != NEW.IdObjetCosmetique
      ) THEN
        RAISE EXCEPTION 'Un utilisateur ne peut avoir qu''un seul titre actif';
      END IF;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_single_active_titre
BEFORE INSERT OR UPDATE ON ObjetUtilisateur
FOR EACH ROW EXECUTE FUNCTION check_single_active_titre();