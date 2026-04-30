from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth
from queries.stats import top_10_users

@ui.page('/leaderboard')
def leaderboard_page():
    require_auth()
    navbar()

    with ui.column().classes('w-full items-center gap-4 p-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            ui.label('Classement').classes('text-xl font-bold text-center w-full capitalize underline')

            users = top_10_users()

            with ui.grid(columns=4).classes('w-full gap-2 p-4'):
                # en-têtes
                ui.label('Position').classes('font-bold text-center text-theme')
                ui.label('Utilisateur').classes('font-bold text-center text-theme')
                ui.label('Niveau').classes('font-bold text-center text-theme')
                ui.label('Points').classes('font-bold text-center text-theme')

                # lignes
                for i, user in enumerate(users, start=1):
                    # médaille pour le top 3
                    if i == 1:
                        ui.label(f'🥇 {i}').classes('text-center text-theme')
                    elif i == 2:
                        ui.label(f'🥈 {i}').classes('text-center text-theme')
                    elif i == 3:
                        ui.label(f'🥉 {i}').classes('text-center text-theme')
                    else:
                        ui.label(str(i)).classes('text-center text-theme')

                    ui.label(user['nom']).classes('text-center text-theme')
                    ui.label(str(user['niveau'])).classes('text-center text-theme')
                    ui.label(str(user['points'])).classes('text-center text-theme')