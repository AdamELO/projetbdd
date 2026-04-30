from nicegui import ui
from components.dialogs import open_resumes_dialog, open_add_resume_dialog
from components.filters import filter_list_cours, get_filtered_cours, apply_filters, reset_filters
from components.navbar import navbar
from components.auth import require_auth

from queries.cours import get_all_cours, get_resumes_by_cours

PER_PAGE = 5

#page des cours
@ui.page('/classes')
def classes_page():
    require_auth()
    navbar()

    classes = get_all_cours() 

    current_page = {'value': 1}
    filters = {}

    def show_list():
        list_classes(list_container, current_page, filters['code'], filters['nom'], filters['faculte'], classes)

    def search():
        apply_filters(show_list, current_page)

    def reset(sc, sn, sf):
        reset_filters(show_list, current_page, sc, sn, sf)

    search_code, search_nom, search_faculte = filter_list_cours(classes, search, reset)

    filters['code'] = search_code
    filters['nom'] = search_nom
    filters['faculte'] = search_faculte

    list_container = ui.column().classes('w-full items-center p-4')
    show_list()



def list_classes(list_container, current_page, search_code, search_nom, search_faculte, classes):
    
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

