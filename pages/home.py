from nicegui import ui
from components.navbar import navbar
from components.auth import get_username, require_auth
from components.stars import stars_rating
from components.item import item_card
from components.comments import comments

#page d'accueil
@ui.page('/')
def home_page():
    require_auth()
    navbar()

    ui.label(f'Bienvenue {get_username()}').classes('text-2xl m-1 w-full text-center text-theme capitalize')

    with ui.column().classes('w-full items-center p-4 gap-4'):
        # Nouveautés dans le shop
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('Nouveautés dans la boutique :').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full justify-around gap-2'):
                fake_items = [
                    {'name' : 'item1', 'description': "badge", 'price': 10, 'is_bought': False},
                    {'name' : 'item2', 'description': "titre", 'price': 500, 'is_bought': True},
                    {'name' : 'item3', 'description': "theme noel", 'price': 30, 'is_bought': False}
                ]
                for item in fake_items:
                    item_card(item)

        # Résumé du mois
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('Meilleur résumé du mois').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full items-center justify-between p-4'):
                with ui.column().classes('gap-1'):
                    ui.label('Base de données pour les nuls').classes('text-lg font-bold')
                    ui.label('Cours : H303 - BDD').classes('text-sm text-gray-600 text-theme')
                    ui.label('Par : xxx').classes('text-sm text-gray-500 text-theme')

                with ui.column().classes('items-center gap-1'):
                    ui.label('Note moyenne').classes('text-sm text-gray-500 text-theme')
                    note_moyenne = 3
                    stars_rating(note_moyenne, size='text-xl')

            ui.separator()

            fake_comments = [
                {'name': 'nom1', 'active_title': 'Étudiant' , 'rating': 5, 'comment': 'Très bien'},
                {'name': 'nom2', 'active_title': 'Expert en résumés', 'rating': 1, 'comment': 'Nul!!!'},
            ]
            comments(fake_comments, "Quelque commentaires")

            ui.separator()
            with ui.row().classes('w-full justify-center'):
                ui.button('Télécharger le résumé', icon='download', on_click=lambda: ui.notify('résumé.pdf', position='top', type='positive')).classes('bg-gray-800').props('flat color=white')