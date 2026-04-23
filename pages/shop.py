from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth

#page de la boutique
@ui.page('/shop')
def shop_page():
    require_auth()
    navbar()

    ui.label('Boutique').classes('text-2xl m-4')