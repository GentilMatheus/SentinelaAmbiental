import flet as ft


class InterfaceApp:
    def __init__(self, page, backend):
        self.page = page
        self.backend = backend
        self.page.title = "Sentinela Ambiental"
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = ft.ThemeMode.LIGHT

        #variável para controlar o estado do alto contraste
        self.alto_contraste = False

        self.criar_interface()

    def alternar_contraste(self, e=None):
        self.alto_contraste = not self.alto_contraste
        if self.alto_contraste:
            self.page.bgcolor = ft.Colors.YELLOW_100
            self.btn_contraste.content = ft.Text("Modo Padrão", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
        else:
            self.page.bgcolor = None
            self.btn_contraste.content = ft.Text("Alto Contraste")
        self.page.update()

    def mostrar_feed(self, e=None):
        self.tela_formulario.visible = False
        self.tela_feed.visible = True
        self.atualizar_feed()
        self.page.update()

    def mostrar_formulario(self, e=None):
        self.tela_feed.visible = False
        self.tela_formulario.visible = True
        self.page.update()

    def aviso(self, texto, cor):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(texto), bgcolor=cor)
        self.page.snack_bar.open = True
        self.page.update()

    def capturar_localizacao(self, e):
        self.backend.capturar_localizacao()
        self.status.value = "📍 Localização adicionada com sucesso!"
        self.page.update()

    def enviar_denuncia(self, e):
        try:
            self.backend.processar_denuncia(
                self.nome.value,
                self.categoria.value,
                self.descricao.value
            )
            self.nome.value = ""
            self.categoria.value = None
            self.descricao.value = ""
            self.status.value = "Aguardando localização..."

            self.aviso("Sua denuncia foi enviada!", ft.Colors.GREEN)
            self.mostrar_feed()

        except ValueError as erro:
            self.aviso(str(erro), ft.Colors.RED)

    def atualizar_feed(self):
        self.feed.controls.clear()
        denuncias = self.backend.listar_denuncias()
        total = len(denuncias)

        lixo = 0
        fogo = 0
        arvore = 0
        esgoto = 0

        for denuncia in denuncias:
            if denuncia["categoria"] == "Lixo jogado na rua":
                lixo += 1
            elif denuncia["categoria"] == "Fogo ou Queimada":
                fogo += 1
            elif denuncia["categoria"] == "Árvore caída":
                arvore += 1
            elif denuncia["categoria"] == "Esgoto vazando":
                esgoto += 1

        #card de estatísticas usando apenas emojis
        self.feed.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text("📊 Estatísticas da Comunidade", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Total de denúncias registradas: {total}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Text(f"🗑️ Lixo: {lixo}"),
                        ft.Text(f"🔥 Queimadas: {fogo}"),
                        ft.Text(f"🌳 Árvores caídas: {arvore}"),
                        ft.Text(f"🚰 Esgoto vazando: {esgoto}")
                    ])
                )
            )
        )

        for denuncia in reversed(denuncias):
            self.feed.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.Text(f"👤 {denuncia['autor']}", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(f"📍 {denuncia['cidade']}"),
                            ft.Text(f"📅 {denuncia['data']}"),
                            ft.Text(denuncia["categoria"], size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(denuncia["descricao"]),
                            ft.Text(f"Status: {denuncia['status']}")
                        ])
                    )
                )
            )

        self.page.update()

    def criar_interface(self):
        self.nome = ft.TextField(label="Primeiro nome (opcional)")
        self.categoria = ft.Dropdown(
            label="Categoria",
            options=[
                ft.dropdown.Option("Lixo jogado na rua"),
                ft.dropdown.Option("Fogo ou Queimada"),
                ft.dropdown.Option("Árvore caída"),
                ft.dropdown.Option("Esgoto vazando")
            ]
        )
        self.descricao = ft.TextField(label="Descrição", multiline=True, min_lines=3, max_lines=5)
        self.status = ft.Text("Aguardando localização...")
        self.feed = ft.Column()

        #botão de alto contraste
        self.btn_contraste = ft.Button(
            content=ft.Text("Alto Contraste"),
            icon=ft.Icons.CONTRAST,
            on_click=self.alternar_contraste
        )

        # tela do feed
        self.tela_feed = ft.Container(
            width=500,
            visible=True,
            content=ft.Column([
                ft.Row([
                    ft.Text("Projeto aluno Matheus Gentil, RU:4476283", size=10, color=ft.Colors.GREY_500),
                    self.btn_contraste
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # titulo usando o icone na pasta assets
                ft.Row([
                    ft.Image(src="img.png", width=45, height=45, fit="contain"),
                    ft.Text("Sentinela Ambiental", size=28, weight=ft.FontWeight.BOLD)
                ]),

                ft.Text("Ajude a cuidar de nossa querida cidade", size=16),
                ft.Divider(),

                # botão usando apenas Emojis
                ft.Button(
                    content=ft.Text("➕ Adicionar Denúncia", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    height=55,
                    bgcolor=ft.Colors.GREEN_700,
                    on_click=self.mostrar_formulario
                ),

                ft.Divider(),
                ft.Text("📢 Feed Comunitário", size=24, weight=ft.FontWeight.BOLD),
                self.feed
            ])
        )

        # tela do formulario
        self.tela_formulario = ft.Container(
            width=500,
            visible=False,
            content=ft.Column([
                ft.Text("projeto de atividade extensionista Aluno Matheus Gentil RU 4476283", size=10,
                        color=ft.Colors.GREY_500),

                ft.Text("📝 Nova Denúncia", size=24, weight=ft.FontWeight.BOLD),
                self.nome,
                self.categoria,
                self.descricao,

                ft.Button(
                    content=ft.Text("📍 Capturar Localização"),
                    height=55,
                    on_click=self.capturar_localizacao
                ),
                self.status,

                ft.Button(
                    content=ft.Text("✅ Enviar Denúncia", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    height=60,
                    bgcolor=ft.Colors.GREEN_700,
                    on_click=self.enviar_denuncia
                ),
                ft.Button(
                    content=ft.Text("❌ Cancelar", color=ft.Colors.GREY_700),
                    height=50,
                    on_click=self.mostrar_feed
                )
            ])
        )
        self.page.add(self.tela_feed, self.tela_formulario)
        self.atualizar_feed()
