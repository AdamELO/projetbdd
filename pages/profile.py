from nicegui import ui
from components.navbar import navbar
from components.auth import get_username, require_auth

#page de profil
@ui.page('/profile')
def profile_page():
    require_auth()
    navbar()

    badges = [
        {'img': 'images/badge/circle_bronze.png', 'description': 'medaille de bronze'},
        {'img': 'images/badge/circle_silver.png', 'description': "medaille d'argent"},
        {'img': 'images/badge/diamond_silver.png', 'description': "medaille d'argent"},
        {'img': 'images/badge/flower_gold.png', 'description': "medaille d'or"},
        {'img': 'images/badge/clover.png', 'description': 'medaille chance'},
    ]

    with ui.card().classes('w-full max-w-4xl absolute-center card-theme'):
        ui.label('mes badges').classes('text-xl font-bold text-center w-full capitalize underline')

        with ui.grid(columns=3).classes('w-full gap-4 p-4 justify-items-center'):
            for badge in badges:
                ui.image(badge['img']).tooltip(badge['description']).classes('w-24 h-28 object-contain p-2').style('overflow: visible;')