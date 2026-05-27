from nicegui import ui
from components.auth import get_theme_name, get_theme_image

THEMES = {
    'Profil sombre': {
        'bg': "#151538", 'navbar': "#14149c",
        'text': "white", 'text_muted': "#a0a0cc",
        'card': "rgba(255,255,255,0.07)", 'btn': "#14149c", 'btn_text': "white"
    },
    'Profil clair': {
        'bg': "#e7e79c", 'navbar': "#c4c47e",
        'text': "#1a1a00", 'text_muted': "#4a4a10",
        'card': "rgba(0,0,0,0.08)", 'btn': "#8a8a30", 'btn_text': "white"
    },
    'Thème nuit': {
        'bg': '#0d1117', 'navbar': '#010409',
        'text': "#e6edf3", 'text_muted': "#8b949e",
        'card': "rgba(255,255,255,0.05)", 'btn': "#238636", 'btn_text': "white"
    },
    'Thème pastel': {
        'bg': '#ffc5d3', 'navbar': '#ffee8c',
        'text': "#3d001a", 'text_muted': "#7a3050",
        'card': "rgba(255,255,255,0.45)", 'btn': "#c2185b", 'btn_text': "white"
    },
    'Thème sombre premium': {
        'bg': '#1c1c1c', 'navbar': '#111111',
        'text': "#e0c97f", 'text_muted': "#a08c50",
        'card': "rgba(255,255,255,0.05)", 'btn': "#4a3800", 'btn_text': "#e0c97f"
    },
    'Thème néon': {
        'bg': '#00FF1A', 'navbar': '#CCFF33',
        'text': "#000000", 'text_muted': "#1a3300",
        'card': "rgba(0,0,0,0.15)", 'btn': "#003300", 'btn_text': "#00FF1A"
    },
}

def background_theme():
    theme_name = get_theme_name()
    theme = THEMES.get(theme_name)

    if theme:
        ui.query('body').style(f'background-color: {theme["bg"]};')
        ui.query('.q-header').style(
            f'background-color: {theme["navbar"]} !important; '
            f'border-color: {theme["navbar"]} !important;'
        )
        ui.add_css(f"""
            .q-header {{ background-color: {theme["navbar"]} !important; }}
            .q-header .q-btn {{ color: {theme["text"]} !important; }}
            .q-header .q-btn .q-icon {{ color: {theme["text"]} !important; }}

            .text-theme {{ color: {theme["text"]} !important; }}
            .text-gray-400, .text-gray-500, .text-gray-600 {{ color: {theme["text_muted"]} !important; }}

            .card-theme {{
                background: {theme["card"]} !important;
                backdrop-filter: blur(8px);
                color: {theme["text"]} !important;
                border: 0.5px solid {theme["text_muted"]} !important;
            }}
            .card-theme .q-item__label {{ color: {theme["text"]} !important; }}
            .card-theme .q-item__label--caption {{ color: {theme["text_muted"]} !important; }}

            .bg-gray-800 {{
                background-color: {theme["btn"]} !important;
                color: {theme["btn_text"]} !important;
            }}
            .bg-gray-800 .q-icon {{ color: {theme["btn_text"]} !important; }}

            .q-tab__label {{ color: {theme["text"]} !important; }}
            .q-tab--active .q-tab__label {{ color: {theme["text"]} !important; font-weight: bold; }}

            .q-field__label {{ color: {theme["text_muted"]} !important; }}
            .q-field__native {{ color: {theme["text"]} !important; }}

            .q-separator {{ background-color: {theme["text_muted"]} !important; opacity: 0.3; }}
        """)
    else:
        ui.query('body').classes('bg-gray-200')

def css_img_theme():
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