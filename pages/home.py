from nicegui import ui
from components.navbar import navbar
from components.auth import get_username, require_auth

#page d'accueil
@ui.page('/')
@require_auth
def home_page():
    navbar()

    ui.label(f'Bienvenue {get_username()}').classes('text-2xl m-4')