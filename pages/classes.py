from nicegui import ui, app
from components.dialogs import open_resumes_dialog
from components.filters import filter_list_courses, get_filtered_courses, apply_filters, reset_filters
from components.navbar import navbar
from components.auth import get_points, require_auth
from queries.cours import get_all_courses, get_summaries_by_course, add_course
from queries.summary import add_summary

PER_PAGE = 5

@ui.page('/classes')
def courses_page():
    require_auth()
    navbar()

    courses = get_all_courses()
    current_page = {'value': 1}
    filters = {}
    selected_course = {'value': None}

    # --- Dialog ajout résumé ---
    with ui.dialog() as add_dialog, ui.card().classes('w-full max-w-lg'):
        dialog_title = ui.label('').classes('text-xl font-bold')
        dialog_subtitle = ui.label('').classes('text-sm text-gray-500 mb-2')
        ui.separator()
        title_input = ui.input('Titre du résumé').classes('w-full')
        upload = ui.upload(label='Fichier (PDF ou DOCX)', auto_upload=True,
                           max_file_size=10_000_000) \
            .props('accept=".pdf,.docx"').classes('w-full')
        error_label = ui.label('').classes('text-red-500')

        def submit():
            course = selected_course['value']
            if not title_input.value.strip():
                error_label.set_text('Le titre est obligatoire')
                return
            user_id = app.storage.user.get('id')
            if not user_id:
                error_label.set_text('Utilisateur non connecté')
                return
            success = add_summary(title_input.value.strip(), None, course['code'], user_id)
            if success:
                app.storage.user['points'] = get_points() + 300
                ui.notify(f'Résumé "{title_input.value}" ajouté !', type='positive')
                add_dialog.close()
                ui.timer(2, lambda: ui.navigate.to('/classes'), once=True)
            else:
                error_label.set_text('Erreur lors de l\'ajout du résumé')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=add_dialog.close).props('flat')
            ui.button('Ajouter', on_click=submit).props('color=primary')

    def open_add(course):
        selected_course['value'] = course
        dialog_title.set_text(f'Ajouter un résumé - {course["name"]}')
        dialog_subtitle.set_text(course['code'])
        title_input.value = ''
        error_label.set_text('')
        upload.reset()
        add_dialog.open()

    # --- Dialog ajout cours ---
    with ui.dialog() as add_course_dialog, ui.card().classes('w-full max-w-lg'):
        ui.label('Ajouter un nouveau cours').classes('text-xl font-bold')
        ui.separator()
        code_input = ui.input('Code du cours (ex: INFOH303)').classes('w-full')
        name_input = ui.input('Nom du cours').classes('w-full')
        faculty_input = ui.input('Faculté').classes('w-full')
        credits_input = ui.number('Crédits', value=5, min=1, max=30).classes('w-full')
        error_course = ui.label('').classes('text-red-500')

        def submit_course():
            if not code_input.value.strip() or not name_input.value.strip() or not faculty_input.value.strip():
                error_course.set_text('Remplissez tous les champs obligatoires')
                return
            success = add_course(
                code_input.value.strip().upper(),
                name_input.value.strip(),
                faculty_input.value.strip(),
                int(credits_input.value)
            )
            if success:
                ui.notify(f'Cours "{name_input.value}" ajouté !', type='positive')
                add_course_dialog.close()
                ui.navigate.to('/classes')
            else:
                error_course.set_text('Erreur — ce code cours existe peut-être déjà')

        with ui.row().classes('w-full justify-end mt-4 gap-2'):
            ui.button('Annuler', on_click=add_course_dialog.close).props('flat')
            ui.button('Ajouter', on_click=submit_course).props('color=primary')

    # --- Filtres ---
    def show_list():
        list_courses(list_container, current_page, filters['code'], filters['name'], filters['faculty'], courses, open_add)

    def search():
        apply_filters(show_list, current_page)

    def reset(sc, sn, sf):
        reset_filters(show_list, current_page, sc, sn, sf)

    search_code, search_name, search_faculty = filter_list_courses(courses, search, reset)
    filters['code'] = search_code
    filters['name'] = search_name
    filters['faculty'] = search_faculty

    # --- Bouton nouveau cours ---
    with ui.row().classes('w-full justify-end max-w-4xl self-center px-4'):
        ui.button('+ Nouveau cours', on_click=add_course_dialog.open).props('color=primary')

    list_container = ui.column().classes('w-full items-center p-4')
    show_list()


def list_courses(list_container, current_page, search_code, search_name, search_faculty, courses, open_add):
    list_container.clear()
    filtered = get_filtered_courses(courses, search_code, search_name, search_faculty)
    start = (current_page['value'] - 1) * PER_PAGE
    end = start + PER_PAGE
    page_courses = filtered[start:end]
    total_pages = max(1, -(-len(filtered) // PER_PAGE))

    with list_container.classes('w-full'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            with ui.list().props('bordered separator').style('width: 100%'):
                ui.item_label(f'Liste des cours ({len(filtered)} résultat(s))').props('header').classes(
                    'text-bold text-theme capitalize text-2xl')
                ui.separator()

                if not page_courses:
                    ui.label('Aucun cours trouvé.').classes('text-gray-400 italic p-4')
                else:
                    for course in page_courses:
                        with ui.item():
                            with ui.item_section().props('avatar'):
                                ui.label(course['code']).classes('text-sm font-bold')
                            with ui.item_section():
                                ui.item_label(course['name'])
                                ui.item_label(f'{course["faculty"]}').props('caption').classes('text-theme')
                            with ui.item_section().props('side'):
                                ui.label(f'{course["summary_count"]} résumé(s)').classes('text-sm text-theme')
                            with ui.item_section().props('side'):
                                ui.button('Voir résumés', on_click=lambda c=course: open_resumes_dialog({**c, 'summaries': get_summaries_by_course(c['code'])})).classes('bg-gray-800').props('flat color=white')
                            with ui.item_section().props('side'):
                                ui.button('Ajouter', icon='add', on_click=lambda c=course: open_add(c)).props('flat color=positive').classes('border')

        with ui.card().classes('w-full justify-center max-w-4xl card-theme'):
            with ui.row().classes('w-full justify-center mt-4'):
                p = ui.pagination(1, total_pages, direction_links=True, value=current_page['value'], on_change=lambda e: change_page(e.value, current_page, lambda: list_courses(list_container, current_page, search_code, search_name, search_faculty, courses, open_add)))

                ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')



def change_page(page, current_page, show_list):
    current_page['value'] = page
    show_list()
