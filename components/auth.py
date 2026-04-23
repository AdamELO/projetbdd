from nicegui import app, ui

def is_logged_in() :
    return app.storage.user.get('authenticated', False)

#getter utilisateur connecté
def get_username() :
    return app.storage.user.get('username', '')

def get_id() :
    return app.storage.user.get('id', 0)

def get_level() :
    return app.storage.user.get('level', 0)

def get_points() :
    return app.storage.user.get('points', 0)

def get_theme_name() :
    return app.storage.user.get('theme_name', None)

def get_theme_image() :
    return app.storage.user.get('theme_image', None)

def get_title() :
    return app.storage.user.get('title_name', None)

def logout():
    app.storage.user['authenticated'] = False
    app.storage.user['id'] = 0
    app.storage.user['username'] = ''
    app.storage.user['level'] = 0
    app.storage.user['points'] = 0
    app.storage.user['theme_name'] = None
    app.storage.user['theme_image'] = None
    app.storage.user['title_name'] = None


def require_auth():
    if not is_logged_in():
        ui.navigate.to('/login')