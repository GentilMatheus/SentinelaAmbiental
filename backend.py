#importa as bibliotecas JSON, sistema operacional e datas
import json
import os
from datetime import datetime

#define o nome do arquivo que sera o "banco de dados" local
ARQUIVO = "denuncias.json"

#classe que gerencia toda a lógica de dados do aplicativo
class BackendSentinela:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def capturar_localizacao(self):
        #simula a obtenção de dados via GPS do dispositivo (focado na cidade de Rio Grande-RS)
        self.latitude = -32.0332
        self.longitude = -52.0986

    def listar_denuncias(self):
        #verifica se o arquivo JSON existe
        if not os.path.exists(ARQUIVO):
            return [] # Se não existir, retorna uma lista vazia

        #abre o arquivo em modo leitura
        with open(
            ARQUIVO,
            "r",
            encoding="utf-8"
        ) as arquivo:
            #converte o texto do arquivo em uma lista
            return json.load(arquivo)

    def salvar_denuncias(self, denuncias):
        #abre o arquivo em modo de escrita ("w") pra salvar dados
        with open(
            ARQUIVO,
            "w",
            encoding="utf-8"
        ) as arquivo:
            #transforma a lista do Python em formato JSON e salva no arquivo
            json.dump(
                denuncias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def processar_denuncia(
        self,
        nome,
        categoria,
        descricao
    ):
        #Validação 1: impede o envio se o usuário não escolher uma categoria
        if not categoria:
            raise ValueError(
                "Selecione uma categoria."
            )

        #Validação 2: impede o envio se o GPS não tiver sido acionado
        if self.latitude is None:
            raise ValueError(
                "Capture a localização."
            )

        #puxa o histórico de denúncias já salvas para adicionar a nova
        denuncias = self.listar_denuncias()

        #estrutura os dados (Payload) do novo chamado
        dados = {
            #gera um ID único baseado na quantidade de denúncias que já existe
            "id":
                f"SENTINELA-{len(denuncias)+1:04}",

            #se o usuário não digitar nome, salva como "Morador"
            "autor":
                nome.strip()
                if nome and nome.strip()
                else "Morador",

            "cidade":
                "Rio Grande",

            "categoria":
                categoria,

            #se não houver descrição, adiciona um texto padrão
            "descricao":
                descricao
                if descricao
                else "Sem detalhes",

            #captura a data e hora exata do momento do envio
            "data":
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),

            "status":
                "Registrado",

            #salva as coordenadas que estavam guardadas na memória
            "coordenadas": {
                "lat": self.latitude,
                "lng": self.longitude
            }
        }

        #adiciona a nova denúncia à lista existente
        denuncias.append(dados)

        #chama a função que grava a lista atualizada no arquivo JSON
        self.salvar_denuncias(
            denuncias
        )

        #reseta as coordenadas na memória para preparar o sistema para a próxima denúncia
        self.latitude = None
        self.longitude = None

        return dados