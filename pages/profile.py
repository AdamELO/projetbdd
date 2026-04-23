from nicegui import ui, app
from components.navbar import navbar
from components.auth import get_id, get_title, get_theme_name, require_auth
from queries.object import user_titles, user_themes

#page de profil
@ui.page('/profile')
def profile_page():
    require_auth()
    navbar()

    user_id = get_id()
    active_title = get_title()
    active_theme = get_theme_name()

    with ui.column().classes('w-full items-center gap-4 p-4'):

        #partie badges
        badges = [
            {'img': 'images/badge/circle_bronze.png', 'description': 'medaille de bronze'},
            {'img': 'images/badge/circle_silver.png', 'description': "medaille d'argent"},
            {'img': 'images/badge/diamond_silver.png', 'description': "medaille d'argent"},
            {'img': 'images/badge/flower_gold.png', 'description': "medaille d'or"},
            {'img': 'images/badge/clover.png', 'description': 'medaille chance'},
        ]

        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('mes badges').classes('text-xl font-bold text-center w-full capitalize underline')

            with ui.grid(columns=3).classes('w-full gap-4 p-4 justify-items-center'):
                for badge in badges:
                    ui.image(badge['img']).tooltip(badge['description']).classes('w-24 h-28 object-contain p-2').style('overflow: visible;')

        #partie titre
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('mes titres').classes('text-xl font-bold text-center w-full capitalize underline')

            if active_title:
                ui.label(f'Titre actif : {active_title}').classes('text-center text-gray-600 text-theme font-semibold mb-2')
            else:
                ui.label('Aucun titre actif').classes('text-center text-theme italic mb-2')

            titles = user_titles(user_id)
            if titles:
                with ui.grid(columns=2).classes('w-full gap-2 p-4'):
                    for t in titles:
                        with ui.row().classes('items-center justify-between w-full border rounded p-2'):
                            ui.label(t['name']).classes('font-semibold text-gray-600 text-theme')
                            ui.button('Activer', on_click=lambda: ui.notify('Titre activé')).props('flat color="white"').classes('text-xs bg-gray-800')
            else:
                ui.label('Aucun titre débloqué').classes('text-center text-gray-400 text-theme italic w-full')

        #partie theme
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('mes thèmes').classes('text-xl font-bold text-center w-full capitalize underline')

            if active_theme:
                ui.label(f'Thème actif : {active_theme}').classes('text-center text-gray-600 text-theme font-semibold mb-2')
            else:
                ui.label('Aucun thème actif').classes('text-center text-gray-400 italic mb-2')

            themes = user_themes(user_id)
            if themes:
                with ui.grid(columns=2).classes('w-full gap-2 p-4'):
                    for th in themes:
                        with ui.row().classes('items-center justify-between w-full border rounded p-2'):
                            if th['image']:
                                ui.image(f"/images/theme/{th['image']}").classes('w-8 h-8 object-cover rounded')
                                ui.label(th['name']).classes('font-semibold text-gray-600 text-theme')
                            ui.button('Activer', on_click= lambda : ui.notify('Thème activé')).props('flat color="white"').classes('text-xs bg-gray-800')
            else:
                ui.label('Aucun thème débloqué').classes('text-center text-gray-400 text-theme italic w-full')