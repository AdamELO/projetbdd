from docutils.nodes import description
from nicegui import ui
from components.navbar import navbar
from components.auth import get_username, require_auth

#page d'accueil
@ui.page('/')
@require_auth
def home_page():
    navbar()

    ui.label(f'Bienvenue {get_username()}').classes('text-2xl m-1 w-full text-center capitalize')

    with ui.column().classes('w-full items-center p-4 gap-4'):
        # Nouveautés dans le shop
        with ui.card().classes('w-full max-w-4xl'):
            ui.label('Nouveautés dans la boutique :').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full justify-around gap-2'):
                fake_items = [
                    {'name' : 'item1', 'description': "badge", 'price': 10, 'is_bought': False},
                    {'name' : 'item2', 'description': "titre", 'price': 500, 'is_bought': True},
                    {'name' : 'item3', 'description': "theme noel", 'price': 30, 'is_bought': False}
                ]
                for item in fake_items:
                    with ui.card().classes("w-60"):
                        ui.label(f'{item['name']}').classes('text-xl text-center')
                        ui.label(f' nom : {item['name']}')
                        ui.label(f'description : {item['description']}')
                        ui.label(f'Prix : {item['price']} pts')
                        btn_buy = ui.button('Acheter', on_click=lambda : ui.notify("todo",position="top" ,type="info")).classes('bg-gray-800 w-full text-center').props('flat color=white').bind_enabled_from(item, 'is_bought', lambda x: not x)
                        btn_buy.bind_icon_from(item, 'is_bought', lambda x: 'lock' if x else 'shopping_cart')
                        btn_buy.bind_text_from(item, 'is_bought', lambda x: 'Acheter' if not x else 'déjà possédé')

        # Résumé du mois
        with ui.card().classes('w-full max-w-4xl'):
            ui.label('Meilleur résumé du mois').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full items-center justify-between p-4'):
                with ui.column().classes('gap-1'):
                    ui.label('Base de données pour les nuls').classes('text-lg font-bold')
                    ui.label('Cours : H303 - BDD').classes('text-sm text-gray-600')
                    ui.label('Par : xxx').classes('text-sm text-gray-500')

                with ui.column().classes('items-center gap-1'):
                    ui.label('Note moyenne').classes('text-sm text-gray-500')
                    with ui.row().classes('items-center gap-1'):
                        note_moyenne = 3
                        for i in range(5):
                            if i < int(note_moyenne):
                                ui.icon('star').classes('text-yellow-500 text-xl')
                            elif i < note_moyenne:
                                ui.icon('star_half').classes('text-yellow-500 text-xl')
                            else:
                                ui.icon('star_outline').classes('text-gray-300 text-xl')
                        ui.label(f'{note_moyenne}/5').classes('text-sm font-bold')

            ui.separator()

            fake_comments = [
                {'name': 'nom1', 'active_title': 'Étudiant' , 'rating': 5, 'comment': 'Très bien'},
                {'name': 'nom2', 'active_title': 'Expert en résumés', 'rating': 1, 'comment': 'Nul!!!'},
            ]

            if fake_comments:
                ui.label('Quelques Commentaires').classes('text-md font-bold px-4 pt-2')
                for com in fake_comments:
                    with ui.card().classes('w-full mx-4 my-1 bg-gray-50'):
                        with ui.row().classes('w-full items-center justify-between'):
                            ui.label(f'{com['name']} - {com['active_title']}').classes('font-bold text-sm capitalize')
                            with ui.row().classes('items-center'):
                                for i in range(5):
                                    if i < com['rating']:
                                        ui.icon('star').classes('text-yellow-500 text-sm')
                                    else:
                                        ui.icon('star_outline').classes('text-gray-300 text-sm')
                        ui.label(f'{com['comment']}').classes('text-sm text-gray-700')
            else:
                ui.label('Aucun commentaire pour le moment.').classes('text-sm text-gray-400 px-4 py-2 italic')

            ui.separator()
            with ui.row().classes('w-full justify-center'):
                ui.button('Télécharger le résumé', icon='download', on_click=lambda: ui.notify('résumé.pdf', position='top', type='positive')).classes('bg-gray-800').props('flat color=white')