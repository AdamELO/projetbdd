from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth
from queries.stats import top_10_users


@ui.refreshable
def display_leaderboard():
    users = top_10_users()
    with ui.grid(columns=4).classes('w-full gap-2 p-4'):
        ui.label('Position').classes('font-bold text-center text-theme')
        ui.label('Utilisateur').classes('font-bold text-center text-theme')
        ui.label('Niveau').classes('font-bold text-center text-theme')
        ui.label('Points').classes('font-bold text-center text-theme')
        for i, user in enumerate(users, start=1):
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
            ui.label(f"{user['points']} pts").classes('text-center text-theme font-bold')


@ui.page('/leaderboard')
def leaderboard_page():
    require_auth()
    navbar()

    with ui.column().classes('w-full items-center gap-4 p-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            
            with ui.row().classes('w-full items-center justify-between px-4'):
                ui.space()
                ui.label('Classement').classes('text-xl font-bold capitalize underline')
                ui.space()
                ui.button(icon='refresh', on_click=display_leaderboard.refresh).props('flat round color=primary')

            display_leaderboard()