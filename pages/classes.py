from nicegui import ui
from components.dialogs import open_resumes_dialog, open_add_resume_dialog
from components.filters import filter_list_cours, get_filtered_cours, apply_filters, reset_filters
from components.navbar import navbar
from components.auth import require_auth

# Données simulées
classes = [
    {'code': 'INFO101', 'nom': 'Introduction à la programmation', 'faculte': 'Sciences', 'annee': '2024-2025', 'nb_resumes': 3,
     'resumes': [
         {'id': 1, 'titre': 'Résumé chapitre 1-3', 'date': '2024-10-15', 'note': 4.5, 'nb_commentaires': 8},
         {'id': 2, 'titre': 'Résumé chapitre 4-6', 'date': '2024-11-02', 'note': 3.8, 'nb_commentaires': 3},
         {'id': 3, 'titre': 'Résumé examen', 'date': '2024-12-10', 'note': None, 'nb_commentaires': 0},
     ]},
    {'code': 'MATH201', 'nom': 'Algèbre linéaire', 'faculte': 'Sciences', 'annee': '2024-2025', 'nb_resumes': 2,
     'resumes': [
         {'id': 4, 'titre': 'Matrices et déterminants', 'date': '2024-09-20', 'note': 4.0, 'nb_commentaires': 5},
         {'id': 5, 'titre': 'Espaces vectoriels', 'date': '2024-10-30', 'note': None, 'nb_commentaires': 0},
     ]},
    {'code': 'PHYS101', 'nom': 'Physique générale', 'faculte': 'Sciences', 'annee': '2024-2025', 'nb_resumes': 1,
     'resumes': [
         {'id': 6, 'titre': 'Mécanique newtonienne', 'date': '2024-11-15', 'note': 4.8, 'nb_commentaires': 12},
     ]},
    {'code': 'DROIT100', 'nom': 'Introduction au droit', 'faculte': 'Droit', 'annee': '2024-2025', 'nb_resumes': 4,
     'resumes': [
         {'id': 7, 'titre': 'Sources du droit', 'date': '2024-09-10', 'note': 3.5, 'nb_commentaires': 2},
         {'id': 8, 'titre': 'Droit civil', 'date': '2024-10-05', 'note': 4.2, 'nb_commentaires': 6},
         {'id': 9, 'titre': 'Droit pénal', 'date': '2024-11-20', 'note': None, 'nb_commentaires': 0},
         {'id': 10, 'titre': 'Résumé final', 'date': '2024-12-15', 'note': 4.9, 'nb_commentaires': 15},
     ]},
    {'code': 'ECON101', 'nom': 'Microéconomie', 'faculte': 'Économie', 'annee': '2024-2025', 'nb_resumes': 0, 'resumes': []},
    {'code': 'HIST200', 'nom': 'Histoire contemporaine', 'faculte': 'Lettres', 'annee': '2023-2024', 'nb_resumes': 2,
     'resumes': [
         {'id': 11, 'titre': 'Guerres mondiales', 'date': '2024-03-10', 'note': 4.1, 'nb_commentaires': 7},
         {'id': 12, 'titre': 'Guerre froide', 'date': '2024-04-22', 'note': 3.9, 'nb_commentaires': 4},
     ]},
    {'code': 'CHIM101', 'nom': 'Chimie organique', 'faculte': 'Sciences', 'annee': '2024-2025', 'nb_resumes': 1,
     'resumes': [
         {'id': 13, 'titre': 'Hydrocarbures', 'date': '2024-10-08', 'note': None, 'nb_commentaires': 0},
     ]},
    {'code': 'PSYC100', 'nom': 'Psychologie générale', 'faculte': 'Sciences humaines', 'annee': '2024-2025', 'nb_resumes': 3,
     'resumes': [
         {'id': 14, 'titre': 'Cognition', 'date': '2024-09-25', 'note': 4.6, 'nb_commentaires': 9},
         {'id': 15, 'titre': 'Mémoire et apprentissage', 'date': '2024-10-30', 'note': 4.3, 'nb_commentaires': 5},
         {'id': 16, 'titre': 'Émotions', 'date': '2024-11-28', 'note': 3.7, 'nb_commentaires': 2},
     ]},
    {'code': 'LANG300', 'nom': 'Linguistique appliquée', 'faculte': 'Lettres', 'annee': '2023-2024', 'nb_resumes': 0, 'resumes': []},
    {'code': 'BIO101', 'nom': 'Biologie cellulaire', 'faculte': 'Sciences', 'annee': '2024-2025', 'nb_resumes': 2,
     'resumes': [
         {'id': 17, 'titre': 'La cellule', 'date': '2024-09-15', 'note': 4.4, 'nb_commentaires': 6},
         {'id': 18, 'titre': 'Division cellulaire', 'date': '2024-11-10', 'note': None, 'nb_commentaires': 0},
     ]},
]

PER_PAGE = 5

#page des cours
@ui.page('/classes')
def classes_page():
    require_auth()
    navbar()

    current_page = {'value': 1}

    def search():
        apply_filters(lambda: list_classes(list_container, current_page, search_code, search_nom, search_faculte), current_page)

    def reset(sc, sn, sf):
        reset_filters(lambda: list_classes(list_container, current_page, search_code, search_nom, search_faculte), current_page, sc, sn, sf)

    search_code, search_nom, search_faculte = filter_list_cours(classes, search, reset)
    list_container = ui.column().classes('w-full items-center p-4')
    list_classes(list_container, current_page, search_code, search_nom, search_faculte)






def list_classes(list_container, current_page, search_code, search_nom, search_faculte):
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
                                ui.item_label(f'{cours["faculte"]} - {cours["annee"]}').props('caption').classes('text-theme')
                            with ui.item_section().props('side'):
                                ui.label(f'{cours["nb_resumes"]} résumé(s)').classes('text-sm text-theme')
                            with ui.item_section().props('side'):
                                ui.button('Voir résumés', on_click=lambda c=cours: open_resumes_dialog(c)).classes('bg-gray-800').props('flat color=white')
                            with ui.item_section().props('side'):
                                ui.button('Ajouter', icon='add', on_click=lambda c=cours: open_add_resume_dialog(c)).props('flat color=positive').classes('border')

        with ui.card().classes('w-full justify-center max-w-4xl card-theme'):
            with ui.row().classes('w-full justify-center mt-4'):
                p = ui.pagination(1, total_pages, direction_links=True, value=current_page['value'], on_change=lambda e: change_page(e.value, current_page, lambda: list_classes(list_container, current_page, search_code, search_nom, search_faculte)))
                ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')



def change_page(page, current_page, show_list):
    current_page['value'] = page
    show_list()

