from nicegui import ui, app
from components.navbar import navbar
from components.auth import get_username, require_auth, get_id
from components.stars import stars_rating
from components.item import item_card
from components.comments import comments
from queries.object import get_lasts_items
from queries.summary import get_random_top_summary

#page d'accueil
@ui.page('/')
def home_page():
    require_auth()
    navbar()

    display_name = get_username().replace('_', ' ').title()
    ui.label(f'Bienvenue {display_name}').classes('text-2xl m-1 w-full text-center text-theme')

    with ui.column().classes('w-full items-center p-4 gap-4'):
        # Nouveautés dans le shop
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label().bind_text_from(app.storage.user, 'points', lambda pts: f'Nouveautés dans la boutique : vous avez actuellement {pts} pts').classes('text-2xl m-1 w-full text-center text-theme capitalize underline')
            with ui.row().classes('w-full justify-around gap-2'):
                lasts_items = get_lasts_items(get_id())
                for item in lasts_items:
                    item_card(item)

        # Résumé du mois
        with ui.card().classes('w-full max-w-4xl card-theme'):
            top = get_random_top_summary()

            if top:
                ui.label('Meilleur résumé d\'un cours aléatoire').classes('text-xl m-4 w-full text-center capitalize underline')
                with ui.row().classes('w-full items-center justify-between p-4'):
                    with ui.column().classes('gap-1'):
                        ui.label(top['title']).classes('text-lg font-bold')
                        ui.label(f"Cours : {top['course_code']} - {top['course_name']}").classes('text-sm text-gray-600 text-theme')
                        display_author = top['author'].replace('_', ' ').title()
                        ui.label(f'Par : {display_author}').classes('text-sm text-gray-500 text-theme')
                with ui.column().classes('items-center gap-1'):
                    ui.label('Note moyenne').classes('text-sm text-gray-500 text-theme')
                stars_rating(float(top['avg_rating'] or 0), size='text-xl')

                ui.separator()
                with ui.row().classes('w-full justify-center'):
                    ui.button('Voir le résumé', icon='visibility',
                      on_click=lambda: ui.navigate.to(f'/summary/{top["id"]}')).classes('bg-gray-800').props('flat color=white')
            else:
                ui.label('Aucun résumé disponible pour le moment.').classes('text-center text-gray-500 p-4')