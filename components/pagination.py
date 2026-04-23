from nicegui import ui

def pagination(total_pages, current_page, change_page) :
    with ui.card().classes('w-full justify-center max-w-4xl card-theme'):
        with ui.row().classes('w-full justify-center mt-4'):
            p = ui.pagination(1, total_pages, direction_links=True,
                              value=current_page['value'],
                              on_change=lambda e: change_page(e.value))
            ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')