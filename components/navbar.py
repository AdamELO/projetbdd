from nicegui import ui
from components.auth import is_logged_in,get_username, get_level, get_points, logout

def navbar():
    ui.page_title('projet bdd')
    ui.query('body').classes('bg-gray-200')
    with ui.header().classes('bg-gray-800 text-white items-center'):
        #icone d'accueil
        ui.button(icon='school', on_click=lambda: ui.navigate.to('/')) \
            .props('flat round color=white')

        #afficher btns utilisateur connecté
        if is_logged_in():
            ui.button('Cours-résumés', on_click=lambda: ui.navigate.to('/classes')) \
                .props('flat color=white')
            ui.button('Classement', on_click=lambda: ui.navigate.to('/leaderboard')) \
                .props('flat color=white')
            ui.button('Boutique', on_click=lambda: ui.navigate.to('/shop')) \
                .props('flat color=white')

            ui.space()

            #niv + pts
            ui.badge(f'lv {get_level()}').props('color=primary').classes("text-xl rounded-full p-2")
            ui.badge(f'{get_points()} pts').props('color=primary').classes("text-xl p-2")

            # Menu déroulant profil et déco
            with ui.button(icon='account_circle', text=f"{get_username()}").props('flat color=white'):
                with ui.menu():
                    ui.menu_item('Mon profil', lambda: ui.navigate.to('/profile'))
                    ui.separator()
                    with ui.menu_item(on_click=lambda:(logout(), ui.navigate.to('/login'))):
                        ui.icon('logout').classes('text-lg')
                        ui.label(' Déconnexion')

        #btn connexion/inscription si pas connecté
        else:
            ui.space()
            ui.button('Connexion', on_click=lambda: ui.navigate.to('/login')) \
                .props('outline color=white')
            ui.button('Inscription', on_click=lambda: ui.navigate.to('/register')) \
                .props('outline color=white')