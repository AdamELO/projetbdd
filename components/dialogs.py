from nicegui import ui, app
from components.auth import get_points
from components.stars import stars_rating
from queries.summary import add_summary

#dialog liste résumés
def open_resumes_dialog(course):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
        ui.label(f'Résumés - {course["name"]}').classes('text-xl font-bold')
        ui.label(f'{course["code"]} - {course["faculty"]}').classes('text-sm text-gray-500 mb-2')
        ui.separator()

        if not course['summaries']:
            ui.label('Aucun résumé disponible pour ce cours.').classes('text-gray-400 italic py-4')
        else:
            with ui.scroll_area().classes('w-full').style('max-height: 400px;'):
                for summary in course['summaries']:
                    with ui.card().classes('w-full my-2'):
                        with ui.row().classes('w-full items-center justify-between'):
                            with ui.column().classes('gap-0'):
                                ui.label(summary['title']).classes('font-bold')
                                ui.label(f'Publié le {summary["date"]}').classes('text-xs text-gray-500')

                            with ui.row().classes('items-center gap-4'):
                                if summary['note'] is not None:
                                    stars_rating(summary['note'])
                                    ui.label(f'{summary["comment_count"]} commentaire(s)').classes('text-xs text-gray-500')
                                else:
                                    ui.label('Pas encore évalué').classes('text-xs text-gray-400 italic')

                                ui.button(icon='visibility',
                                          on_click=lambda s=summary: (dialog.close(), ui.navigate.to(f'/summary/{s["id"]}'))) \
                                    .props('flat round color=primary')

        with ui.row().classes('w-full justify-end mt-2'):
            ui.button('Fermer', on_click=dialog.close).props('flat')

    dialog.open()



#dialog ajout résumé
def open_add_resume_dialog(course):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-lg'):
        ui.label(f'Ajouter un résumé - {course["name"]}').classes('text-xl font-bold')
        ui.label(f'{course["code"]}').classes('text-sm text-gray-500 mb-2')
        ui.separator()

        title = ui.input('Titre du résumé').classes('w-full')
        upload = ui.upload(label='Fichier (PDF ou DOCX)', auto_upload=True,
                           max_file_size=10_000_000) \
            .props('accept=".pdf,.docx"').classes('w-full')

        error = ui.label('').classes('text-red-500')

        def submit():
            print("SUBMIT CALLED")

            if not title.value:
                error.set_text('Le titre est obligatoire')
                return
            user_id = app.storage.user.get('id')
            success = add_summary(title.value, None, course['code'], user_id)
            if success:
                app.storage.user['points'] = get_points() + 500
                ui.notify(f'Résumé "{title.value}" ajouté !', type='positive')
                dialog.close()
                ui.timer(2, lambda: ui.navigate.to('/classes'), once=True)
            else:
                error.set_text('Erreur lors de l\'ajout du résumé')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=dialog.close).props('flat')
            ui.button('Ajouter', on_click=lambda: submit()).props('color=primary')

    dialog.open()
