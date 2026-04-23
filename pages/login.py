from nicegui import ui, app
from components.navbar import navbar
from queries.user import login
from queries.object import user_active_title, user_active_theme

#page de connexion
@ui.page('/login')
def login_page():
    navbar()
    with ui.card().classes('absolute-center w-96'):
        ui.label('Connexion').classes('text-2xl font-bold mb-4 text-center w-full underline')
        username_input = ui.input('Nom d\'utilisateur').classes('w-full')
        password_input = ui.input('Mot de passe', password=True, password_toggle_button=True).classes('w-full')
        error = ui.label('').classes('text-red-500')

        ui.button('Se connecter', on_click=lambda: check_login(username_input, password_input, error)).classes('w-full mt-4 bg-gray-800').props('flat color=white')

        with ui.row().classes('w-full justify-center mt-2'):
            ui.label('Pas de compte ?')
            ui.link('S\'inscrire', '/register').classes('text-blue-500')



def check_login(username_input, password_input, error):
    user = login(username_input.value, password_input.value)
    if user:
        app.storage.user['authenticated'] = True
        app.storage.user['username'] = user['username']
        app.storage.user['id'] = user['id']
        app.storage.user['email'] = user['email']
        app.storage.user['level'] = user['level']
        app.storage.user['points'] = user['points']

        active_theme = user_active_theme(user['id'])
        active_title = user_active_title(user['id'])
        if active_theme:
            app.storage.user['theme_name'] = active_theme['name']
            app.storage.user['theme_image'] = active_theme['image']
        else:
            app.storage.user['theme_name'] = None
            app.storage.user['theme_image'] = None

        if active_title:
            app.storage.user['title_name'] = active_title['title']['name']
        else:
            app.storage.user['title_name'] = None

        ui.navigate.to('/')
    else:
        error.set_text('Identifiants incorrects')