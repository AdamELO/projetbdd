from nicegui import ui, app
from components.navbar import navbar
from components.auth import get_id, get_title, get_theme_name, require_auth
from queries.object import user_titles, user_themes, user_badges, user_cosmetiques


#page de profil
@ui.page('/profile')
def profile_page():
    require_auth()
    navbar()

    user_id = get_id()
    active_title = get_title()
    active_theme = get_theme_name()

    with ui.column().classes('w-full items-center gap-4 p-4'):

        with ui.card().classes('w-full max-w-4xl card-theme'):
            with ui.row().classes('w-full items-center justify-center gap-6 p-4'):
                ui.icon('account_circle').classes('text-6xl')
            with ui.column().classes('gap-1'):
                ui.label(app.storage.user.get('username', '')).classes('text-2xl font-bold text-theme')
                ui.label(f'Niveau {app.storage.user.get("level", 0)}').classes('text-theme')
                ui.label(f'{app.storage.user.get("points", 0)} points').classes('text-theme')
                if active_title:
                    ui.label(f'🏆 {active_title}').classes('text-theme font-semibold')

        #partie badges
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('mes badges').classes('text-xl font-bold text-center w-full capitalize underline')
    
            badges = user_badges(user_id)
            if badges:
                with ui.grid(columns=3).classes('w-full gap-4 p-4 justify-items-center'):
                    for badge in badges:
                        with ui.column().classes('items-center gap-1'):
                            if badge['image']:
                                ui.image(f"/images/badge/{badge['image']}").tooltip(badge['description']).classes('w-24 h-28 object-contain p-2')
                            else:
                                ui.icon('military_tech').classes('text-5xl text-yellow-500')
                            ui.label(badge['name']).classes('text-xs text-center text-theme')
            else:
                ui.label('Aucun badge débloqué').classes('text-center text-gray-400 text-theme italic w-full p-4')
        
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
        

# Après la section thèmes :
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('mes cosmétiques').classes('text-xl font-bold text-center w-full capitalize underline')
    
            cosmetiques = user_cosmetiques(user_id)
            if cosmetiques:
                with ui.grid(columns=3).classes('w-full gap-4 p-4 justify-items-center'):
                    for c in cosmetiques:
                        with ui.column().classes('items-center gap-1'):
                            ui.icon('auto_awesome').classes('text-5xl text-yellow-500')
                            ui.label(c['name']).classes('text-xs text-center text-theme')
                            ui.label(c['description']).classes('text-xs text-center text-gray-400 italic')
            else:
                ui.label('Aucun cosmétique débloqué').classes('text-center text-gray-400 text-theme italic w-full p-4')