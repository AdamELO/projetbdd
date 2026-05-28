from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth, get_id
from queries.user import get_user_transactions

TYPE_LABELS = {
    'summary':  ('note_add',      'Résumé publié',       'text-green-600'),
    'comment':  ('comment',       'Commentaire publié',  'text-blue-500'),
    'purchase': ('shopping_cart', 'Achat boutique',      'text-red-500'),
    'other':    ('swap_horiz',    'Transaction',          'text-gray-500'),
}

@ui.page('/transactions')
def transactions_page():
    require_auth()
    navbar()

    user_id = get_id()
    transactions = get_user_transactions(user_id)

    with ui.column().classes('w-full items-center p-4 gap-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('Historique des transactions').classes('text-2xl font-bold text-center w-full underline mb-2')

            if not transactions:
                ui.label('Aucune transaction pour le moment.').classes('text-center text-gray-400 italic p-4')
            else:
                with ui.list().props('bordered separator').classes('w-full'):
                    for t in transactions:
                        icon, label, color = TYPE_LABELS.get(t['type'], TYPE_LABELS['other'])
                        if t['type'] == 'purchase' and t['item_name']:
                            label = f"Achat : {t['item_name']}"
                        montant = t['amount']
                        sign = '+' if montant > 0 else ''

                        with ui.item().classes('w-full'):
                            with ui.item_section().props('avatar'):
                                ui.icon(icon).classes(f'text-2xl {color}')
                            with ui.item_section():
                                ui.item_label(label).classes('font-semibold text-theme')
                                ui.item_label(str(t['date'])).props('caption').classes('text-theme')
                            with ui.item_section().props('side'):
                                ui.label(f'{sign}{montant} pts').classes(
                                    f'font-bold {"text-green-600" if montant > 0 else "text-red-500"}'
                                )
