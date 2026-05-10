from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth
from queries.stats import top_10_users, top_10_by_level


def draw_table(users):
    with ui.grid(columns=4).classes('w-full gap-2 p-4'):
        ui.label('Position').classes('font-bold text-center text-theme')
        ui.label('Utilisateur').classes('font-bold text-center text-theme')
        ui.label('Niveau').classes('font-bold text-center text-theme')
        ui.label('Points').classes('font-bold text-center text-theme')

        for i, u in enumerate(users, start=1):
            # Médailles pour le top 3
            icon = f'🥇 {i}' if i == 1 else f'🥈 {i}' if i == 2 else f'🥉 {i}' if i == 3 else str(i)
            
            ui.label(icon).classes('text-center text-theme')
            ui.label(u['nom']).classes('text-center text-theme')
            ui.label(str(u['niveau'])).classes('text-center text-theme font-bold text-primary')
            ui.label(f"{u['points']} pts").classes('text-center text-theme font-bold text-secondary')

@ui.refreshable
def points_board():
    users = top_10_users()
    draw_table(users)

@ui.refreshable
def level_board():
    users = top_10_by_level()
    draw_table(users)

@ui.page('/leaderboard')
def leaderboard_page():
    require_auth()
    navbar()

    with ui.column().classes('w-full items-center p-4'):
        with ui.card().classes('w-full max-w-4xl card-theme'):
            
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Tableaux des scores').classes('text-2xl font-bold')
                ui.button(icon='refresh', on_click=lambda: (points_board.refresh(), level_board.refresh())).props('flat round')

            with ui.tabs().classes('w-full text-primary') as tabs:
                tab_levels = ui.tab('Les plus Actifs (Niveau)', icon='military_tech')
                tab_points = ui.tab('Les plus Riches (Points)', icon='monetization_on')
            
            with ui.tab_panels(tabs, value=tab_levels).classes('w-full bg-transparent'):
                
                with ui.tab_panel(tab_levels):
                    level_board()
                    
                with ui.tab_panel(tab_points):
                    points_board()