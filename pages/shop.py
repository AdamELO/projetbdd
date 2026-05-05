from nicegui import ui, app
from components.item import item_card
from components.navbar import navbar
from components.auth import require_auth, get_id
from queries.object import get_badges_not_owned, get_cosmetic_not_owned, get_themes_not_owned, get_titles_not_owned

#page de la boutique
@ui.page('/shop')
def shop_page():
    require_auth()
    navbar()

    userId = get_id()
    titles = get_titles_not_owned(userId)
    badges = get_badges_not_owned(userId)
    themes = get_themes_not_owned(userId)
    cosmetic = get_cosmetic_not_owned(userId)


    ui.label().bind_text_from(app.storage.user, 'points', lambda pts: f'Boutique : vous avez actuellement {pts} pts').classes('text-2xl m-1 w-full text-center text-theme capitalize underline')

    with ui.column().classes('w-full items-center p-4 gap-4'):

        # achats titres
        with ui.card().classes('w-full max-w-5xl card-theme text-theme'):
            ui.label('Titres').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full justify-around gap-2 items-stretch'):
                titles_label = ui.label('Pas de titres disponible!')
                titles_label.set_visibility(len(titles) == 0)
                titles_counter = [0]
                for item in titles:
                    item_card(item, on_hidden=lambda: item_hidden(titles_counter, len(titles), titles_label))

        # achats badges
        with ui.card().classes('w-full max-w-5xl card-theme text-theme'):
            ui.label('Badges').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full justify-around gap-2 items-stretch'):
                badges_label = ui.label('Pas de badges disponible!')
                badges_label.set_visibility(len(badges) == 0)
                badges_counter = [0]
                for item in badges:
                    item_card(item, on_hidden=lambda: item_hidden(badges_counter, len(badges), badges_label))

        # achats themes
        with ui.card().classes('w-full max-w-5xl card-theme text-theme'):
            ui.label('Thèmes').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full justify-around gap-2 items-stretch'):
                themes_label = ui.label('Pas de thèmes disponible!')
                themes_label.set_visibility(len(themes) == 0)
                themes_counter = [0]
                for item in themes:
                    item_card(item, on_hidden=lambda: item_hidden(themes_counter, len(themes), themes_label))

        # achats cosmetic
        with ui.card().classes('w-full max-w-5xl card-theme text-theme'):
            ui.label('Autre cosmétique').classes('text-xl m-4 w-full text-center capitalize underline')
            with ui.row().classes('w-full justify-around gap-2 items-stretch'):
                cosmetic_label = ui.label('Pas d\'autre cosmétique disponible!')
                cosmetic_label.set_visibility(len(cosmetic) == 0)
                cosmetic_counter = [0]
                for item in cosmetic:
                    item_card(item, on_hidden=lambda: item_hidden(cosmetic_counter, len(cosmetic), cosmetic_label))



def item_hidden(counter, total, label):
    counter[0] += 1
    if counter[0] >= total:
        label.set_visibility(True)