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
                {'name': 'nom', 'label': 'Nom', 'field': 'nom', 'align': 'left'},
                {'name': 'niveau', 'label': 'Niveau', 'field': 'niveau'},
                {'name': 'points', 'label': 'Points', 'field': 'points', 'sortable': True},
            ]
            ui.table(columns=columns, rows=data).classes('w-full')

        # 2. Utilisateurs actifs (> 3 cours)
        with ui.expansion('Contributeurs actifs (résumés dans au moins 3 cours différents)').classes('w-full border rounded-lg'):
            data = stats.users_min_3_courses()
            columns = [
                {'name': 'nom', 'label': 'Nom', 'field': 'nom', 'align': 'left'},
                {'name': 'nb_cours', 'label': 'Nombre de cours différents', 'field': 'nb_cours'},
            ]
            ui.table(columns=columns, rows=data).classes('w-full')

        # 3. Le ou les cours ayant le plus de résumés
        # 3. Le ou les cours ayant le plus de résumés
        with ui.expansion('Cours le(s) plus populaire(s)').classes('w-full border rounded-lg'):
            data = stats.most_summarized_course()
    
            columns_cours = [
                        {'name': 'nom', 'label': 'Nom du cours', 'field': 'nom', 'align': 'left'},
                    {'name': 'nb', 'label': 'Nombre de résumés', 'field': 'nb_resumes', 'align': 'center', 'sortable': True},
                        {'name': 'code', 'label': 'Code', 'field': 'code', 'align': 'right'},
                        ]
            ui.table(columns=columns_cours, rows=data).classes('w-full')

        # 4. Les résumés les mieux notés par cours
        with ui.expansion('Meilleurs résumés par cours').classes('w-full border rounded-lg'):
            data = stats.best_rated_resumes()
            columns = [
                {'name': 'code', 'label': 'Code Cours', 'field': 'code', 'align': 'left'},
                {'name': 'titre', 'label': 'Titre du Résumé', 'field': 'titre', 'align': 'left'},
                {'name': 'note', 'label': 'Note Moyenne', 'field': 'note_moyenne', 'format': '(val) => val.toFixed(2)'},
            ]
            ui.table(columns=columns, rows=data).classes('w-full')

        # 5. Utilisateurs n'ayant jamais publié
        with ui.expansion('Utilisateurs sans aucune publication').classes('w-full border rounded-lg'):
            data = stats.users_no_resume()
            with ui.column().classes('p-4'):
                for u in data:
                    ui.label(f"• {u['nom']}")

        # 6. L'objet cosmétique le plus acheté
        with ui.expansion('Objet cosmétique le plus populaire').classes('w-full border rounded-lg'):
            res = stats.most_bought_item()
            if res:
                ui.label(f"L'objet le plus vendu est '{res['nom']}' avec un total de {res['nb_achats']} achats.").classes('p-4')

        # 7. Alertes : Utilisateurs ayant trop dépensé
        with ui.expansion('Alertes : Soldes négatifs / Dépenses excessives').classes('w-full border rounded-lg'):
            data = stats.users_overspent()
            if not data:
                ui.label("Aucune anomalie de solde détectée.").classes('p-4 italic')
            else:
                columns = [
                    {'name': 'nom', 'label': 'Utilisateur', 'field': 'nom', 'align': 'left'},
                    {'name': 'points', 'label': 'Points actuels', 'field': 'points'},
                    {'name': 'depenses', 'label': 'Total dépensé', 'field': 'points_depenses'},
                ]
                ui.table(columns=columns, rows=data).classes('w-full text-red-600')

        # 8. Moyenne de résumés par utilisateur
        with ui.expansion('Statistique : Moyenne de publications').classes('w-full border rounded-lg'):
            res = stats.avg_resumes_per_user()
            ui.label(f"En moyenne, chaque utilisateur a publié {res['moyenne']} résumés sur la plateforme.").classes('p-4 text-lg')