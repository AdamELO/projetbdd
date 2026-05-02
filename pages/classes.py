from nicegui import ui, app
from components.dialogs import open_resumes_dialog
from components.filters import filter_list_cours, get_filtered_cours, apply_filters, reset_filters
from components.navbar import navbar
from components.auth import require_auth
from queries.cours import get_all_cours, get_resumes_by_cours, add_cours
from queries.resume import add_resume

PER_PAGE = 5

@ui.page('/classes')
def classes_page():
    require_auth()
    navbar()

    classes = get_all_cours()
    current_page = {'value': 1}
    filters = {}
    selected_cours = {'value': None}

    # --- Dialog ajout résumé ---
    with ui.dialog() as add_dialog, ui.card().classes('w-full max-w-lg'):
        dialog_title = ui.label('').classes('text-xl font-bold')
        dialog_subtitle = ui.label('').classes('text-sm text-gray-500 mb-2')
        ui.separator()
        titre_input = ui.input('Titre du résumé').classes('w-full')
        error_label = ui.label('').classes('text-red-500')

        def submit():
            print("SUBMIT APPELÉ", flush=True)
            cours = selected_cours['value']
            if not titre_input.value.strip():
                error_label.set_text('Le titre est obligatoire')
                return
            id_utilisateur = app.storage.user.get('id')
            if not id_utilisateur:
                error_label.set_text('Utilisateur non connecté')
                return
            success = add_resume(titre_input.value.strip(), None, cours['code'], id_utilisateur)
            if success:
                ui.notify(f'Résumé "{titre_input.value}" ajouté !', type='positive')
                add_dialog.close()
                ui.navigate.to('/classes')
            else:
                error_label.set_text('Erreur lors de l\'ajout du résumé')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=add_dialog.close).props('flat')
            ui.button('Ajouter', on_click=submit).props('color=primary')

    def open_add(cours):
        selected_cours['value'] = cours
        dialog_title.set_text(f'Ajouter un résumé - {cours["nom"]}')
        dialog_subtitle.set_text(cours['code'])
        titre_input.value = ''
        error_label.set_text('')
        add_dialog.open()

    # --- Dialog ajout cours ---
    with ui.dialog() as add_cours_dialog, ui.card().classes('w-full max-w-lg'):
        ui.label('Ajouter un nouveau cours').classes('text-xl font-bold')
        ui.separator()
        code_input = ui.input('Code du cours (ex: INFOH303)').classes('w-full')
        nom_input = ui.input('Nom du cours').classes('w-full')
        faculte_input = ui.input('Faculté').classes('w-full')
        credits_input = ui.number('Crédits', value=5, min=1, max=30).classes('w-full')
        error_cours = ui.label('').classes('text-red-500')

        def submit_cours():
            if not code_input.value.strip() or not nom_input.value.strip() or not faculte_input.value.strip():
                error_cours.set_text('Remplissez tous les champs obligatoires')
                return
            success = add_cours(
                code_input.value.strip().upper(),
                nom_input.value.strip(),
                faculte_input.value.strip(),
                int(credits_input.value)
            )
            if success:
                ui.notify(f'Cours "{nom_input.value}" ajouté !', type='positive')
                add_cours_dialog.close()
                ui.navigate.to('/classes')
            else:
                error_cours.set_text('Erreur — ce code cours existe peut-être déjà')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=add_cours_dialog.close).props('flat')
            ui.button('Ajouter', on_click=submit_cours).props('color=primary')

    # --- Filtres ---
    def show_list():
        list_classes(list_container, current_page, filters['code'], filters['nom'], filters['faculte'], classes, open_add)

    def search():
        apply_filters(show_list, current_page)

    def reset(sc, sn, sf):
        reset_filters(show_list, current_page, sc, sn, sf)

    search_code, search_nom, search_faculte = filter_list_cours(classes, search, reset)
    filters['code'] = search_code
    filters['nom'] = search_nom
    filters['faculte'] = search_faculte

    # --- Bouton nouveau cours ---
    with ui.row().classes('w-full justify-end max-w-4xl self-center px-4'):
        ui.button('+ Nouveau cours', on_click=add_cours_dialog.open).props('color=primary')

    list_container = ui.column().classes('w-full items-center p-4')
    show_list()





def list_classes(list_container, current_page, search_code, search_nom, search_faculte, classes, open_add):    
    list_container.clear()
    filtered = get_filtered_cours(classes, search_code, search_nom, search_faculte)
    start = (current_page['value'] - 1) * PER_PAGE
    end = start + PER_PAGE
    page_classes = filtered[start:end]
    total_pages = max(1, -(-len(filtered) // PER_PAGE))

    with list_container.classes('w-full'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            with ui.list().props('bordered separator').style('width: 100%'):
                ui.item_label(f'Liste des cours ({len(filtered)} résultat(s))').props('header').classes(
                    'text-bold text-theme capitalize text-2xl')
                ui.separator()

                if not page_classes:
                    ui.label('Aucun cours trouvé.').classes('text-gray-400 italic p-4')
                else:
                    for cours in page_classes:
                        with ui.item():
                            with ui.item_section().props('avatar'):
                                ui.label(cours['code']).classes('text-sm font-bold')
                            with ui.item_section():
                                ui.item_label(cours['nom'])
                                ui.item_label(f'{cours["faculte"]}').props('caption').classes('text-theme')
                            with ui.item_section().props('side'):
                                ui.label(f'{cours["nb_resumes"]} résumé(s)').classes('text-sm text-theme')
                            with ui.item_section().props('side'):
                                ui.button('Voir résumés', on_click=lambda c=cours: open_resumes_dialog({**c, 'resumes': get_resumes_by_cours(c['code'])})).classes('bg-gray-800').props('flat color=white')
                            with ui.item_section().props('side'):
                                ui.button('Ajouter', icon='add', on_click=lambda c=cours: open_add_resume_dialog(c)).props('flat color=positive').classes('border')

        with ui.card().classes('w-full justify-center max-w-4xl card-theme'):
            with ui.row().classes('w-full justify-center mt-4'):
                p = ui.pagination(1, total_pages, direction_links=True, value=current_page['value'], on_change=lambda e: change_page(e.value, current_page, lambda: list_classes(list_container, current_page, search_code, search_nom, search_faculte, classes)))

                ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')



def change_page(page, current_page, show_list):
    current_page['value'] = page
    show_list()

