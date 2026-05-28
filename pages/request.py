from nicegui import ui
from components.navbar import navbar
from components.auth import require_auth
import queries.stats as stats

@ui.page('/request')
def request_page():
    require_auth()
    navbar()

    with ui.column().classes('w-full p-8 max-w-6xl mx-auto gap-4'):

        # 1. Top 10 des Utilisateurs
        with ui.expansion('Top 10 des Utilisateurs').classes('w-full border rounded-lg'):
            data = stats.top_10_users()
            columns = [
                {'name': 'name', 'label': 'Nom', 'field': 'name', 'align': 'left'},
                {'name': 'level', 'label': 'Niveau', 'field': 'level'},
                {'name': 'points', 'label': 'Points', 'field': 'points', 'sortable': True},
            ]
            ui.table(columns=columns, rows=data).classes('w-full')

        # 2. Utilisateurs actifs (> 3 cours)
        with ui.expansion('Contributeurs actifs (résumés dans au moins 3 cours différents)').classes('w-full border rounded-lg'):
            data = stats.users_min_3_courses()
            columns = [
                {'name': 'name', 'label': 'Nom', 'field': 'name', 'align': 'left'},
                {'name': 'course_count', 'label': 'Nombre de cours différents', 'field': 'course_count'},
            ]
            ui.table(columns=columns, rows=data).classes('w-full')

        # 3. Le ou les cours ayant le plus de résumés
        with ui.expansion('Cours le(s) plus populaire(s)').classes('w-full border rounded-lg'):
            data = stats.most_summarized_course()
            columns_course = [
                {'name': 'name', 'label': 'Nom du cours', 'field': 'name', 'align': 'left'},
                {'name': 'summary_count', 'label': 'Nombre de résumés', 'field': 'summary_count', 'align': 'center', 'sortable': True},
                {'name': 'code', 'label': 'Code', 'field': 'code', 'align': 'right'},
            ]
            ui.table(columns=columns_course, rows=data).classes('w-full')

        # 4. Les résumés les mieux notés par cours
        with ui.expansion('Meilleurs résumés par cours').classes('w-full border rounded-lg'):
            data_best = stats.best_rated_summaries()
            columns_best = [
                {'name': 'code', 'label': 'Code Cours', 'field': 'code', 'align': 'left'},
                {'name': 'title', 'label': 'Titre du Résumé', 'field': 'title', 'align': 'left'},
                {'name': 'avg_rating', 'label': 'Note Moyenne', 'field': 'avg_rating', 'align': 'center'},
            ]
            if data_best:
                ui.table(columns=columns_best, rows=data_best).classes('w-full')
            else:
                ui.label("Aucune évaluation disponible pour le moment.").classes('p-4 italic text-gray-500')

        # 5. Utilisateurs n'ayant jamais publié
        with ui.expansion('Utilisateurs sans aucune publication').classes('w-full border rounded-lg'):
            data_no_summary = stats.users_no_summary()
            columns_no_summary = [
                {'name': 'name', 'label': 'Nom de l\'utilisateur', 'field': 'name', 'align': 'left'}
            ]
            ui.table(columns=columns_no_summary, rows=data_no_summary).classes('w-full')

        # 6. L'objet cosmétique le plus acheté
        with ui.expansion('Objet cosmétique le plus populaire').classes('w-full border rounded-lg'):
            res = stats.most_bought_item()
            if res:
                with ui.row().classes('w-full bg-white p-4'):
                    ui.label(f"L'objet le plus vendu est '{res['name']}' avec un total de {res['purchase_count']} achats.")
            else:
                with ui.row().classes('w-full bg-white p-4'):
                    ui.label("Aucun achat n'a été enregistré.")

        # 7. Alertes : Utilisateurs ayant trop dépensé
        with ui.expansion('Utilisateurs avec soldes négatifs').classes('w-full border rounded-lg'):
            data = stats.users_overspent()
            if not data:
                ui.label("Aucune anomalie de solde détectée.").classes('p-4 italic')
            else:
                columns = [
                    {'name': 'name', 'label': 'Utilisateur', 'field': 'name', 'align': 'left'},
                    {'name': 'points', 'label': 'Points actuels', 'field': 'points'},
                    {'name': 'points_spent', 'label': 'Total dépensé', 'field': 'points_spent'},
                ]
                ui.table(columns=columns, rows=data).classes('w-full text-red-600')

        # 8. Moyenne de résumés par utilisateur
        with ui.expansion('Nombre moyen de résumés publiés').classes('w-full border rounded-lg'):
            res = stats.avg_summaries_per_user()
            if res:
                with ui.row().classes('w-full bg-white p-4'):
                    ui.label(f"En moyenne, chaque utilisateur a publié {res['average']} résumés sur la plateforme.")
            else:
                with ui.row().classes('w-full bg-white p-4'):
                    ui.label("Aucun achat n'a été enregistré.")
