from nicegui import ui, app
from components.navbar import navbar
from components.auth import require_auth
from components.stars import stars_rating
from components.comments import comments
from queries.cours import get_resume_by_id, get_evaluations_by_resume
from queries.resume import update_resume, delete_resume

@ui.page('/summary/{summary_id}')
def summary_page(summary_id):
    require_auth()
    navbar()

    summary = get_resume_by_id(summary_id)
    if not summary:
        ui.navigate.to('/')
        return

    evaluations = get_evaluations_by_resume(summary_id)
    current_user = app.storage.user.get('username', '')
    is_author = current_user == summary['auteur']

    # --- Dialog modification ---
    with ui.dialog() as edit_dialog, ui.card().classes('w-full max-w-lg'):
        ui.label('Modifier le résumé').classes('text-xl font-bold')
        ui.separator()
        titre_edit = ui.input('Titre', value=summary['titre']).classes('w-full')
        upload_edit = ui.upload(label='Nouveau fichier (PDF ou DOCX)', auto_upload=True,
                            max_file_size=10_000_000) \
            .props('accept=".pdf,.docx"').classes('w-full')
        error_edit = ui.label('').classes('text-red-500')

        def submit_edit():
            if not titre_edit.value.strip():
                error_edit.set_text('Le titre est obligatoire')
                return
            success = update_resume(summary_id, titre_edit.value.strip(), None)
            if success:
                ui.notify('Résumé modifié !', type='positive')
                edit_dialog.close()
                ui.navigate.to(f'/summary/{summary_id}')
            else:
                error_edit.set_text('Erreur lors de la modification')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=edit_dialog.close).props('flat')
            ui.button('Modifier', on_click=submit_edit).props('color=primary')
    # --- Dialog suppression ---
    with ui.dialog() as delete_dialog, ui.card().classes('w-full max-w-sm'):
        ui.label('Supprimer ce résumé ?').classes('text-xl font-bold')
        ui.label('Cette action est irréversible.').classes('text-gray-500')

        def confirm_delete():
            success = delete_resume(summary_id)
            if success:
                ui.notify('Résumé supprimé !', type='positive')
                delete_dialog.close()
                ui.navigate.to('/classes')
            else:
                ui.notify('Erreur lors de la suppression', type='negative')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=delete_dialog.close).props('flat')
            ui.button('Supprimer', on_click=confirm_delete).props('color=negative')

    # --- Page ---
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

            with ui.row().classes('w-full justify-center gap-2'):
                ui.button('Télécharger le résumé', icon='download',
                          on_click=lambda: ui.notify('résumé.pdf', position='top', type='positive')) \
                    .classes('bg-gray-800').props('flat color=white')

                if is_author:
                    ui.button('Modifier', icon='edit', on_click=edit_dialog.open).props('flat color=primary')
                    ui.button('Supprimer', icon='delete', on_click=delete_dialog.open).props('flat color=negative')