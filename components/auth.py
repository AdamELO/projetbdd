from functools import wraps
from nicegui import app, ui

def is_logged_in() :
    return app.storage.user.get('authenticated', False)

#getter utilisateur connecté
def get_username() :
    return app.storage.user.get('username', '')

def get_level() -> int:
    return app.storage.user.get('level', 0)

def get_points() -> int:
    return app.storage.user.get('points', 0)


def logout():
    app.storage.user['authenticated'] = False
    app.storage.user['username'] = ''
    app.storage.user['level'] = 0
    app.storage.user['points'] = 0


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            ui.navigate.to('/login')
            return
        return func(*args, **kwargs)
    return wrapper