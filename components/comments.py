from nicegui import ui
from components.stars import stars_rating

def comments(comments, text_comm = "tout les commentaires"):
    if comments:
        ui.label(f'{text_comm}').classes('text-md font-bold px-4 pt-2')
        for comment in comments:
            with ui.card().classes('w-full mx-4 my-1 bg-gray-50 card-theme'):
                with ui.row().classes('w-full items-center justify-between'):
                    ui.label(f'{comment["name"]} - {comment["active_title"]}').classes('font-bold text-sm capitalize')
                    stars_rating(comment['rating'], size='text-sm')
                ui.label(comment['comment']).classes('text-sm text-gray-700 text-theme')
    else:
        ui.label('Aucun commentaire pour le moment.').classes('text-sm text-gray-400 px-4 py-2 italic')
