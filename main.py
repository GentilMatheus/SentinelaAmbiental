import flet as ft
from backend import BackendSentinela
from interface import InterfaceApp

def main(page: ft.Page):
    backend = BackendSentinela()
    InterfaceApp(page, backend)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=8550)