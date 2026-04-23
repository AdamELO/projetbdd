from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth
from components.stars import stars_rating
from components.comments import comments


@ui.page('/summary/{summary_id}')
def summary_page(summary_id):
    require_auth()
    navbar()
    summary = {'title': 'test', 'cours': 'bdd'}
    if not summary:
        ui.navigate.to('/')

    with ui.column().classes('w-full items-center p-4 gap-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label(f'{summary['title']}').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full items-center justify-between p-4'):
                with ui.column().classes('gap-1'):
                    ui.label(f"{summary['title']}").classes('text-lg font-bold')
                    ui.label(f"Cours : {summary['cours']}").classes('text-sm text-gray-600 text-theme')
                    ui.label('Par : xxx').classes('text-sm text-gray-500 text-theme')

                with ui.column().classes('items-center gap-1'):
                    ui.label('Note moyenne').classes('text-sm text-gray-500 text-theme')
                    note_moyenne = 3
                    stars_rating(note_moyenne, size='text-xl')

            ui.separator()

            fake_comments = [
                {'name': 'nom1', 'active_title': 'Étudiant', 'rating': 5, 'comment': 'Très bien'},
                {'name': 'nom2', 'active_title': 'Expert en résumés', 'rating': 1, 'comment': 'Nul!!!'},
            ]
            comments(fake_comments)

            ui.separator()
            with ui.row().classes('w-full justify-center'):
                ui.button('Télécharger le résumé', icon='download', on_click=lambda: ui.notify('résumé.pdf', position='top', type='positive')).classes('bg-gray-800').props('flat color=white')