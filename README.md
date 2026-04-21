# Projet bdd

## Prérequis

- Python 3.x
- PostgreSQL

## Installation
```bash
python3 -m pip install --break-system-packages nicegui psycopg2-binary bcrypt
```

Ensuite, créer un fichier `config.py` à la racine du projet avec les informations de connexion de la bdd PostgreSQL :

```python
DB_HOST = "localhost"
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_PORT = 5432  # port PostgreSQL par défaut
```

## Lancer le script python

```bash
python3 main.py
```