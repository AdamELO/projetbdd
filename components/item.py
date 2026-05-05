from nicegui import ui, app
from components.auth import get_id, get_points
from queries.object import buy_object

def item_card(item, on_hidden=None):
    show_bought_state = 'is_bought' in item
    with ui.card().classes('w-60 card-theme text-theme').style("height: stretch !important;") as card:
        ui.label(item['name']).classes('text-xl text-center italic underline')
        ui.label(f'{item["description"]}')
        ui.label(f'Prix : {item["price"]} pts').classes('font-bold border-2 border-solid rounded p-1')
        ui.space()
        is_bought = item.get('is_bought', False)
        btn_buy = ui.button( 'déjà possédé' if is_bought else 'Acheter', icon='lock' if is_bought else 'shopping_cart', 
                            on_click=lambda: buy_item(item['id'], item['price'], get_id(), get_points(), btn_buy, card, show_bought_state, on_hidden)
                            ).classes('bg-gray-800 w-full text-center').props('flat color=white')
        if is_bought:
            btn_buy.disable()


def buy_item(item_id, item_price, user_id, user_points, btn, card, show_bought_state, on_hidden=None):
    if user_points < item_price:
        ui.notify('Pas assez de points', position='top', type='negative')
        return
    if buy_object(item_id, user_id, item_price):
        app.storage.user['points'] = user_points - item_price
        ui.notify('Objet acheté!', position='top', type='positive')
        if show_bought_state:
            btn.set_text('déjà possédé')
            btn.props('icon=lock')
            btn.disable()
        else:
            card.set_visibility(False)
            if on_hidden:
                on_hidden()
    else:
        ui.notify('Pas assez de points ou problème survenu!', position='top', type='negative')

