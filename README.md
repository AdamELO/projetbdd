# Projet Base de Données — Plateforme de partage de résumés de cours

## Prérequis

- Python 3.x
- PostgreSQL (version 13+)

## Installation des dépendances

```bash
python3 -m pip install nicegui psycopg2-binary bcrypt reportlab
```

> Sur certains systèmes (Debian/Ubuntu récents, Arch…), pip peut refuser l'installation hors environnement virtuel. Dans ce cas, utiliser :
>
> ```bash
> python3 -m pip install nicegui psycopg2-binary bcrypt reportlab --break-system-packages
> ```

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

> Toutes les commandes sont à exécuter depuis la **racine du projet**.
> Selon ton OS, utilise `python3` (Linux/macOS) ou `python` (Windows).

Deux étapes à effectuer une seule fois, dans cet ordre.

**1. Créer les tables :**

Via le script Python (recommandé) :

```bash
python3 database/create_tables_db.py
```

Ou directement avec psql :

```bash
psql -U <utilisateur> -d <nom_base> -f database/sql/create.sql
```

**2. Insérer les données initiales :**

Linux/macOS :

```bash
PYTHONPATH=. python3 database/init_db.py
```

Windows (CMD) :

```cmd
set PYTHONPATH=. && python database/init_db.py
```

Windows (PowerShell) :

```powershell
$env:PYTHONPATH="."; python database/init_db.py
```

## Lancer l'application

```bash
python3 main.py
```

L'application est ensuite accessible sur [http://localhost:8080](http://localhost:8080).

## Structure du projet

```
.
├── main.py                  # Point d'entrée
├── config.py                # Configuration de la base de donnée (à créer)
├── database/
│   ├── db.py                # Connexion PostgreSQL
│   ├── init_db.py           # Script d'initialisation des données
│   ├── create_tables_db.py  # Script de création des tables
│   └── sql/
│       ├── create.sql       # Schéma de la base (DDL)
│       └── queries.sql      # Requêtes nommées
├── components/              # Composants NiceGUI réutilisables
├── pages/                   # Pages de l'application
├── queries/                 # Fonctions d'accès à la base
│   ├── cours.py
│   ├── object.py
│   ├── summary.py
│   ├── stats.py
│   └── user.py
└── data/                    # Données initiales (CSV, XML, JSON)
```

## Comptes de test

Tous les utilisateurs insérés par `init_db.py` ont le mot de passe par défaut :

```
password123
```