# Projet Base de Données — Plateforme de partage de résumés de cours

## Prérequis

- Python 3.x
- PostgreSQL (version 13+)

## Installation des dépendances

```bash
pip install nicegui psycopg2-binary bcrypt reportlab
```

## Configuration

Créer un fichier `config.py` à la racine du projet avec les informations de connexion à ta base PostgreSQL :

```python
DB_HOST = "localhost"
DB_NAME = ""       # nom de ta base
DB_USER = ""       # ton utilisateur PostgreSQL
DB_PASSWORD = ""   # ton mot de passe
DB_PORT = 5432     # port par défaut
```

## Initialisation de la base de données

Deux étapes à effectuer une seule fois, dans cet ordre.

**1. Créer les tables :**

```bash
psql -U <utilisateur> -d <nom_base> -f database/sql/create.sql
```

**2. Insérer les données initiales :**

```bash
python -m database.init_db
```

## Lancer l'application

```bash
python main.py
```

L'application est ensuite accessible sur [http://localhost:8080](http://localhost:8080).

## Structure du projet

```
.
├── main.py                  # Point d'entrée
├── config.py                # Configuration de la base (à créer)
├── database/
│   ├── db.py                # Connexion PostgreSQL
│   ├── init_db.py           # Script d'initialisation des données
│   └── sql/
│       ├── create.sql       # Schéma de la base (DDL)
│       └── queries.sql      # Requêtes nommées
├── components/              # Composants NiceGUI réutilisables
├── pages/                   # Pages de l'application
├── queries/                 # Fonctions d'accès à la base
│   ├── cours.py
│   ├── object.py
│   ├── resume.py
│   ├── stats.py
│   └── user.py
└── data/                    # Données initiales (CSV, XML, JSON)
```

## Comptes de test

Tous les utilisateurs insérés par `init_db.py` ont le mot de passe par défaut :

```
password123
```