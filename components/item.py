from nicegui import ui

def item_card(item):
    with ui.card().classes('w-60 card-theme'):
        ui.label(item['name']).classes('text-xl text-center')
        ui.label(f'nom : {item["name"]}')
        ui.label(f'description : {item["description"]}')
        ui.label(f'Prix : {item["price"]} pts')
        btn_buy = ui.button('Acheter', on_click=lambda: ui.notify('todo', position='top', type='info')).classes('bg-gray-800 w-full text-center').props('flat color=white')
        btn_buy.bind_enabled_from(item, 'is_bought', lambda x: not x)
        btn_buy.bind_icon_from(item, 'is_bought', lambda x: 'lock' if x else 'shopping_cart')
        btn_buy.bind_text_from(item, 'is_bought', lambda x: 'Acheter' if not x else 'déjà possédé')
