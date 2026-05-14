from nicegui import ui, app
from components.navbar import navbar
from components.auth import get_username, require_auth, get_id
from components.stars import stars_rating
from components.item import item_card
from components.comments import comments
from queries.object import get_lasts_items
from queries.resume import get_best_resume_of_month
from queries.cours import get_evaluations_by_resume

#page d'accueil
@ui.page('/')
def home_page():
    require_auth()
    navbar()

    username = get_username()
    display_name = username.replace('_', ' ').title()
    ui.label(f'Bienvenue {display_name}').classes('text-3xl m-6 w-full text-center text-theme font-bold')
    
    with ui.column().classes('w-full items-center p-4 gap-4'):
        # Nouveautés dans le shop
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label().bind_text_from(app.storage.user, 'points', lambda pts: f'Suggestions de la boutique : vous avez actuellement {pts} pts').classes('text-2xl m-1 w-full text-center text-theme capitalize underline')
            with ui.row().classes('w-full justify-around gap-2'):
                lasts_items = get_lasts_items(get_id())
                for item in lasts_items:
                    item_card(item)

   

    with ui.card().classes('w-full max-w-4xl card-theme'):
        ui.label('Meilleur résumé du mois').classes('text-xl m-4 w-full text-center capitalize underline')
    
        best = get_best_resume_of_month()
        if best:
            with ui.row().classes('w-full items-center justify-between p-4'):
                with ui.column().classes('gap-1'):
                    ui.label(best['titre']).classes('text-lg font-bold')
                    ui.label(f"Cours : {best['code_cours']} - {best['nom_cours']}").classes('text-sm text-gray-600 text-theme')
                    ui.label(f"Par : {best['auteur']}").classes('text-sm text-gray-500 text-theme')

            with ui.column().classes('items-center gap-1'):
                ui.label('Note moyenne').classes('text-sm text-gray-500 text-theme')
                stars_rating(best['note'], size='text-xl')
                ui.label(f"{best['note']} / 5 ({best['nb_commentaires']} avis)").classes('text-sm text-theme')

            ui.separator()
            evaluations = get_evaluations_by_resume(best['id'])
            comments(evaluations, "Quelques commentaires")
            ui.separator()

            with ui.row().classes('w-full justify-center'):
                ui.button('Voir le résumé', icon='visibility',
                      on_click=lambda: ui.navigate.to(f'/summary/{best["id"]}')).classes('bg-gray-800').props('flat color=white')
        else:
            ui.label('Aucun résumé évalué ce mois-ci.').classes('text-gray-400 italic p-4 text-center w-full')