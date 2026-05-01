from nicegui import ui, app
import re
from components.navbar import navbar
from queries.user import register

#page d'inscription
@ui.page('/register')
def register_page():
    navbar()
    with ui.card().classes('absolute-center w-96'):
        ui.label('Inscription').classes('text-2xl font-bold mb-4 text-center w-full underline')
        username = ui.input('Nom d\'utilisateur').classes('w-full')
        email = ui.input('Email').classes('w-full')
        password = ui.input('Mot de passe', password=True, password_toggle_button=True).classes('w-full')
        confirm = ui.input('Confirmer', password=True, password_toggle_button=True).classes('w-full')
        error = ui.label('').classes('text-red-500')

        ui.button('S\'inscrire', on_click=lambda: check_register(username, email, password, confirm, error)).classes('w-full mt-4 bg-gray-800').props('flat color=white')

        with ui.row().classes('w-full justify-center mt-2'):
            ui.label('Déjà un compte ?')
            ui.link('Se connecter', '/login').classes('text-blue-500')


def check_register(username, email, password, confirm, error):
    if not username.value or not password.value or not email.value:
        error.set_text('Remplissez tous les champs svp')
    elif not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email.value):
        error.set_text('Email invalide')
    elif password.value != confirm.value:
        error.set_text('Les mots de passe ne correspondent pas')
    else:
        print(f"Appel register avec: {username.value}, {email.value}")
        result = register(username.value, email.value, password.value)
        print(f"Résultat register: {result}")
        if result:
            app.storage.user['authenticated'] = True
            app.storage.user['id'] = result['id']
            app.storage.user['username'] = username.value
            app.storage.user['email'] = email.value
            app.storage.user['level'] = 1
            app.storage.user['points'] = 0
            app.storage.user['title_name'] = None
            app.storage.user['theme_name'] = None
            app.storage.user['theme_image'] = None
            ui.navigate.to('/')
        else:
            error.set_text('Nom d\'utilisateur ou email déjà pris')