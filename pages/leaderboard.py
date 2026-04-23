from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth

#page du classement
@ui.page('/leaderboard')
def leaderboard_page():
    require_auth()
    navbar()

    ui.label('Classement').classes('text-2xl m-4')