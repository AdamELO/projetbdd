from nicegui import ui

def stars_rating(note, size='text-sm'):
    with ui.row().classes('items-center gap-0'):
        for i in range(5):
            if i < int(note):
                ui.icon('star').classes(f'text-yellow-500 {size}')
            elif i < note:
                ui.icon('star_half').classes(f'text-yellow-500 {size}')
            else:
                ui.icon('star_outline').classes(f'text-gray-300 {size}')
        ui.label(f'{note}/5').classes('text-xs ml-1')