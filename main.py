#importa o Flet, framework responsavel pela interface
import flet as ft

#importa as classes personalizadas separadas nos outros arquivos
from backend import BackendSentinela
from interface import InterfaceApp

#função principal que inicializa o aplicativo
def main(page: ft.Page):

    #instancia a classe responsável pelo backend
    backend = BackendSentinela()

    #instancia a interface, passandoa pagina do Flet e o backend para ela
    InterfaceApp(page, backend)

#executa o aplicativo
ft.run(main, assets_dir="assets")