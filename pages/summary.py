from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth


@ui.page('/summary/{summary_id}')
def summary_page(summary_id):
    require_auth()
    navbar()

    # Requête SQL avec l'id
    # summary = get_summary_by_id(summary_id)
    summary = {'titre': 'test', 'cours': 'bdd'}

    if not summary:
        ui.navigate.to('/')

    ui.label(summary['titre']).classes('text-2xl font-bold')
    ui.label(f'Cours : {summary["cours"]}')