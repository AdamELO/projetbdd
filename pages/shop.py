from docutils.nodes import title
from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth

#page de la boutique
@ui.page('/shop')
@require_auth
def shop_page():
    navbar()

    ui.label('Boutique').classes('text-2xl m-4')