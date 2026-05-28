from nicegui import ui, app
from components.navbar import navbar
from components.auth import get_points, require_auth, get_id
from components.stars import stars_rating
from components.comments import comments
from queries.cours import get_summary_by_id, get_evaluations_by_summary
from queries.summary import update_summary, delete_summary, add_evaluation, get_summary_file, save_summary_file
import io


def generate_blank_pdf(title):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont("Helvetica", 16)
    c.drawCentredString(297, 750, title)
    c.save()
    return buffer.getvalue()


@ui.page('/summary/{summary_id}')
def summary_page(summary_id):
    require_auth()
    navbar()

    summary = get_summary_by_id(summary_id)
    if not summary:
        ui.navigate.to('/')
        return

    evaluations = get_evaluations_by_summary(summary_id)
    current_user = app.storage.user.get('username', '')
    is_author = current_user == summary['author']

    file_bytes = {'value': None}

    # --- Dialog modification ---
    with ui.dialog() as edit_dialog, ui.card().classes('w-full max-w-lg'):
        ui.label('Modifier le résumé').classes('text-xl font-bold')
        ui.separator()
        title_edit = ui.input('Titre', value=summary['title']).classes('w-full')
        async def on_upload(e):
            file_bytes['value'] = await e.file.read()

        upload_edit = ui.upload(label='Nouveau fichier (PDF)', auto_upload=True,
                                max_file_size=10_000_000, on_upload=on_upload) \
            .props('accept=".pdf"').classes('w-full')
        error_edit = ui.label('').classes('text-red-500')

        def submit_edit():
            if not title_edit.value.strip():
                error_edit.set_text('Le titre est obligatoire')
                return
            success = update_summary(summary_id, title_edit.value.strip(), None)
            if success and file_bytes['value']:
                save_summary_file(summary_id, file_bytes['value'])
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
            success = delete_summary(summary_id, get_id())
            if success:
                ui.notify('Résumé supprimé !', type='positive')
                delete_dialog.close()
                ui.navigate.to('/classes')
            else:
                ui.notify('Erreur lors de la suppression', type='negative')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=delete_dialog.close).props('flat')
            ui.button('Supprimer', on_click=confirm_delete).props('color=negative')

    # --- Dialog ajout commentaire ---
    with ui.dialog() as comment_dialog, ui.card().classes('w-full max-w-lg'):
        ui.label('Ajouter un commentaire').classes('text-xl font-bold')
        ui.separator()

        note_value = {'value': 5}
        ui.label('Note :').classes('text-sm font-bold mt-2')
        with ui.row().classes('gap-1'):
            def set_note(n, label):
                note_value['value'] = n
                label.set_text(f'Note : {n}/5')
            note_label = ui.label('Note : 5/5').classes('text-sm text-gray-500 text-theme')
            with ui.row().classes('gap-1'):
                for i in range(1, 6):
                    ui.button(str(i), on_click=lambda n=i: set_note(n, note_label)).props('flat').classes('text-yellow-500')

        comment_input = ui.textarea('Commentaire').classes('w-full')
        error_comment = ui.label('').classes('text-red-500')

        def submit_comment():
            if is_author:
                ui.notify('Vous ne pouvez pas commenter votre propre résumé', type='warning')
                comment_dialog.close()
                return
            if not comment_input.value.strip():
                error_comment.set_text('Le commentaire est obligatoire')
                return
            user_id = app.storage.user.get('id')
            success = add_evaluation(note_value['value'], comment_input.value.strip(), summary_id, user_id)
            if success:
                app.storage.user['points'] = get_points() + 50
                ui.notify('Commentaire ajouté !', type='positive')
                comment_dialog.close()
                ui.navigate.to(f'/summary/{summary_id}')
            else:
                error_comment.set_text('Erreur lors de l\'ajout du commentaire')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=comment_dialog.close).props('flat')
            ui.button('Publier', on_click=submit_comment).props('color=primary')

    # --- Fonction téléchargement ---
    def download():
        data = get_summary_file(summary_id)
        if data and data['fichier']:
            pdf_bytes = bytes(data['fichier'])
        else:
            pdf_bytes = generate_blank_pdf(summary['title'])
        ui.download(pdf_bytes, f"resume_{summary_id}.pdf")

    # --- Page ---
    with ui.column().classes('w-full items-center p-4 gap-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label(summary['title']).classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full items-center justify-between p-4'):
                with ui.column().classes('gap-1'):
                    ui.label(summary['title']).classes('text-lg font-bold')
                    ui.label(f"Cours : {summary['course_code']} - {summary['course_name']}").classes('text-sm text-gray-600 text-theme')
                    ui.label(f"Par : {summary['author']}").classes('text-sm text-gray-500 text-theme')
                    ui.label(f"Publié le : {summary['date']}").classes('text-sm text-gray-500 text-theme')
                    ui.label(f"Version : {summary['version']}").classes('text-sm text-gray-500 text-theme')

                with ui.column().classes('items-center gap-1'):
                    ui.label('Note moyenne').classes('text-sm text-gray-500 text-theme')
                    if summary['note'] is not None:
                        stars_rating(summary['note'], size='text-xl')
                        ui.label(f"{summary['note']} / 5 ({summary['comment_count']} avis)").classes('text-sm text-theme')
                    else:
                        ui.label('Pas encore évalué').classes('text-sm text-gray-400 italic')

            ui.separator()
            comments(evaluations)
            ui.separator()

            with ui.row().classes('w-full justify-center gap-2 p-2'):
                ui.button('Télécharger le résumé', icon='download', on_click=download) \
                    .classes('bg-gray-800').props('flat color=white')
                if not is_author:
                    ui.button('Ajouter un commentaire', icon='comment',
                              on_click=comment_dialog.open).props('flat color=primary')

                if is_author:
                    ui.button('Modifier', icon='edit', on_click=edit_dialog.open).props('flat color=primary')
                    ui.button('Supprimer', icon='delete', on_click=delete_dialog.open).props('flat color=negative')
