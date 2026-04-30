from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth
from components.stars import stars_rating
from components.comments import comments
from queries.cours import get_resume_by_id, get_evaluations_by_resume

@ui.page('/summary/{summary_id}')
def summary_page(summary_id):
    require_auth()
    navbar()

    summary = get_resume_by_id(summary_id)
    if not summary:
        ui.navigate.to('/')
        return

    evaluations = get_evaluations_by_resume(summary_id)

    with ui.column().classes('w-full items-center p-4 gap-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label(summary['titre']).classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full items-center justify-between p-4'):
                with ui.column().classes('gap-1'):
                    ui.label(summary['titre']).classes('text-lg font-bold')
                    ui.label(f"Cours : {summary['code_cours']} - {summary['nom_cours']}").classes('text-sm text-gray-600 text-theme')
                    ui.label(f"Par : {summary['auteur']}").classes('text-sm text-gray-500 text-theme')
                    ui.label(f"Publié le : {summary['date']}").classes('text-sm text-gray-500 text-theme')

                with ui.column().classes('items-center gap-1'):
                    ui.label('Note moyenne').classes('text-sm text-gray-500 text-theme')
                    if summary['note'] is not None:
                        stars_rating(summary['note'], size='text-xl')
                        ui.label(f"{summary['note']} / 5 ({summary['nb_commentaires']} avis)").classes('text-sm text-theme')
                    else:
                        ui.label('Pas encore évalué').classes('text-sm text-gray-400 italic')

            ui.separator()
            comments(evaluations)
            ui.separator()

            with ui.row().classes('w-full justify-center'):
                ui.button('Télécharger le résumé', icon='download',
                          on_click=lambda: ui.notify('résumé.pdf', position='top', type='positive')) \
                    .classes('bg-gray-800').props('flat color=white')