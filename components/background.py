from nicegui import ui
from components.auth import get_theme_name, get_theme_image

THEMES = {
    'Profil sombre': {'bg': "#151538", 'navbar': "#14149c"},
    'Profil clair': {'bg': "#e7e79c", 'navbar': "#c4c47e"},
    'Thème nuit': {'bg': '#0d1117', 'navbar': '#010409'},
    'Thème pastel': {'bg': '#ffc5d3', 'navbar': '#ffee8c'},
    'Thème sombre premium': {'bg': '#1c1c1c', 'navbar': '#111111'},
    'Thème néon': {'bg': '#00FF1A', 'navbar': '#CCFF33'},
}

def background_theme():
    theme_name = get_theme_name()
    theme = THEMES.get(theme_name)

    if theme:
        ui.query('body').style(f'background-color: {theme["bg"]};')
        ui.query('.q-header').style(f'background-color: {theme["navbar"]} !important; border-color: {theme["navbar"]} !important;')
        ui.add_css(f'.q-header {{ background-color: {theme["navbar"]} !important; }}')
    else:
        ui.query('body').classes('bg-gray-200')

def css_img_theme() :
    ui.add_css('''
        .card-theme {
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(8px);
            color: white !important;
        }
        .text-theme {
            color: white !important;
        }
    ''')