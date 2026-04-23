from nicegui import ui
from components.stars import stars_rating


#dialog liste résumés
def open_resumes_dialog(cours):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl'):
        ui.label(f'Résumés - {cours["nom"]}').classes('text-xl font-bold')
        ui.label(f'{cours["code"]} - {cours["faculte"]}').classes('text-sm text-gray-500 mb-2')
        ui.separator()

        if not cours['resumes']:
            ui.label('Aucun résumé disponible pour ce cours.').classes('text-gray-400 italic py-4')
        else:
            with ui.scroll_area().classes('w-full').style('max-height: 400px;'):
                for resume in cours['resumes']:
                    with ui.card().classes('w-full my-2'):
                        with ui.row().classes('w-full items-center justify-between'):
                            with ui.column().classes('gap-0'):
                                ui.label(resume['titre']).classes('font-bold')
                                ui.label(f'Publié le {resume["date"]}').classes('text-xs text-gray-500')

                            with ui.row().classes('items-center gap-4'):
                                if resume['note'] is not None:
                                    stars_rating(resume['note'])
                                    ui.label(f'{resume["nb_commentaires"]} commentaire(s)').classes('text-xs text-gray-500')
                                else:
                                    ui.label('Pas encore évalué').classes('text-xs text-gray-400 italic')

                                ui.button(icon='visibility',
                                          on_click=lambda r=resume: (dialog.close(), ui.navigate.to(f'/summary/{r["id"]}'))) \
                                    .props('flat round color=primary')

        with ui.row().classes('w-full justify-end mt-2'):
            ui.button('Fermer', on_click=dialog.close).props('flat')

    dialog.open()



#dialog ajout résumé
def open_add_resume_dialog(cours):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-lg'):
        ui.label(f'Ajouter un résumé - {cours["nom"]}').classes('text-xl font-bold')
        ui.label(f'{cours["code"]}').classes('text-sm text-gray-500 mb-2')
        ui.separator()

        titre = ui.input('Titre du résumé').classes('w-full')
        description = ui.textarea('Description').classes('w-full')
        upload = ui.upload(label='Fichier (PDF ou DOCX)', auto_upload=True,
                           max_file_size=10_000_000) \
            .props('accept=".pdf,.docx"').classes('w-full')

        error = ui.label('').classes('text-red-500')

        def submit():
            if not titre.value:
                error.set_text('Le titre est obligatoire')
                return
            ui.notify(f'Résumé "{titre.value}" ajouté !', type='positive')
            dialog.close()

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=dialog.close).props('flat')
            ui.button('Ajouter', on_click=submit).props('color=primary')

    dialog.open()