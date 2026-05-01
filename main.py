from nicegui import ui, app

app.add_static_files('/images', 'images')

#importation des pages
import pages.home
import pages.login
import pages.register
import pages.shop
import pages.profile
import pages.classes
import pages.summary
import pages.leaderboard
import pages.register

ui.run(storage_secret='6291b522e702e0a8efca3352571403225edeb284d06fe75e2c7d21f25f2f959b')