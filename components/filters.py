from nicegui import ui

def filter_list_cours(classes, on_search, on_reset):
    facultes = list(set(c['faculte'] for c in classes))
    facultes.sort()
    with ui.card().classes('w-full max-w-4xl mx-auto mt-4 card-theme'):
        ui.label('Filtres').classes('text-lg font-bold')
        with ui.row().classes('w-full items-center gap-4'):
            search_code = ui.input(label='Code du cours').classes('w-48 text-theme').props("label-color='primary'").on('keydown.enter', lambda: on_search())
            search_nom = ui.input(label='Nom du cours').classes('w-64 text-theme').props("label-color='primary'").on('keydown.enter', lambda: on_search())
            search_faculte = ui.select(label='Faculté', options=['Toutes'] + facultes, on_change=lambda: on_search()).classes('w-48 text-theme').props("label-color='primary'")                

            ui.button('Rechercher', icon='search', on_click=lambda: on_search()).props('flat color=white')
            ui.button('Réinitialiser', icon='refresh', on_click=lambda: on_reset(search_code, search_nom, search_faculte)).props('flat color=white')

    return (search_code, search_nom, search_faculte)




def get_filtered_cours(list_cours, search_code, search_nom, search_faculte):
    filtered = list_cours
    if search_code.value:
        filtered = [c for c in filtered if search_code.value.upper() in c['code'].upper()]
    if search_nom.value:
        filtered = [c for c in filtered if search_nom.value.lower() in c['nom'].lower()]
    if search_faculte.value and search_faculte.value != 'Toutes':
        filtered = [c for c in filtered if c['faculte'] == search_faculte.value]
    return filtered

def apply_filters(show_list, current_page):
    current_page['value'] = 1
    show_list()

def reset_filters(show_list, current_page, search_code, search_nom, search_faculte):
    search_code.set_value('')
    search_nom.set_value('')
    search_faculte.set_value('Toutes')
    current_page['value'] = 1
    show_list()