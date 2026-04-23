from nicegui import ui
from components.auth import get_theme_name, get_theme_image

def background_theme() :
    if get_theme_image():
        ui.query('body').style (f'background-image: url("images/theme/{get_theme_image()}"); background-size: cover; background-attachment: fixed;')
        css_img_theme()
    elif get_theme_name():
        ui.query('body').style(f'background-color: {get_theme_name()}')
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