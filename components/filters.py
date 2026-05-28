from nicegui import ui

def filter_list_courses(courses, on_search, on_reset):
    faculties = list(set(c['faculty'] for c in courses))
    faculties.sort()
    with ui.card().classes('w-full max-w-4xl mx-auto mt-4 card-theme'):
        ui.label('Filtres').classes('text-lg font-bold')
        with ui.row().classes('w-full items-center gap-4'):
            search_code = ui.input(label='Code du cours').classes('w-48 text-theme').props("label-color='primary'").on('keydown.enter', lambda: on_search())
            search_name = ui.input(label='Nom du cours').classes('w-64 text-theme').props("label-color='primary'").on('keydown.enter', lambda: on_search())
            search_faculty = ui.select(label='Faculté', options=['Toutes'] + faculties, on_change=lambda: on_search()).classes('w-48 text-theme').props("label-color='primary'")

            ui.button('Rechercher', icon='search', on_click=lambda: on_search()).props('flat color=white')
            ui.button('Réinitialiser', icon='refresh', on_click=lambda: on_reset(search_code, search_name, search_faculty)).props('flat color=white')

    return (search_code, search_name, search_faculty)


def get_filtered_courses(course_list, search_code, search_name, search_faculty):
    filtered = course_list
    if search_code.value:
        filtered = [c for c in filtered if search_code.value.upper() in c['code'].upper()]
    if search_name.value:
        filtered = [c for c in filtered if search_name.value.lower() in c['name'].lower()]
    if search_faculty.value and search_faculty.value != 'Toutes':
        filtered = [c for c in filtered if c['faculty'] == search_faculty.value]
    return filtered

def apply_filters(show_list, current_page):
    current_page['value'] = 1
    show_list()

def reset_filters(show_list, current_page, search_code, search_name, search_faculty):
    search_code.set_value('')
    search_name.set_value('')
    search_faculty.set_value('Toutes')
    current_page['value'] = 1
    show_list()
