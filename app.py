from database import Database
from menu import Menu

__author__ = "chansen"

Database.initialize()

menu = Menu()

while True:
    menu.run_menu()
