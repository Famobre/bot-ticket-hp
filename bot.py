# -------------------------------
# IMPORTAÇÕES
# -------------------------------
import os
import json
import asyncio
import itertools
import threading
from typing import List

import discord
from discord.ext import commands
from flask import Flask, request
from rich.console import Console

# -------------------------------
# CONFIGURAÇÕES
# -------------------------------
LOG_CHANNEL_ID = 1447675219132289075  # Canal logs-tickets
STAFF_ROLE_ID = 1447675210789818386   # Cargo da staff
ARQUIVO_PLANTAO = "plantao.json"
BOT_PREFIX = "!"
STATUS_INTERVAL = 15  # segundos

console = Console()
console.print("[bold green]BOT INICIANDO...[/bold green]")

# -------------------------------
# CLASSE DO BOT
# -------------------------------
class PlantaoBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=BOT_PREFIX, intents=intents)

        # Lista de status cíclicos
        self.status_list = itertools.cycle([
            discord.Game(name="Salvando vidas 🏥"),
            discord.Activity(type=discord.ActivityType.watching, name="ajudando os pacientes 🩺"),
            discord.Activity(type=discord.ActivityType.listening, name="chamados do plantão 🚑"),
            discord.Game(name="Cuidando de todos 🏙️"),
        ])

        # Iniciar API Flask em thread separada
        self.app = Flask(__name__)
        self._setup_api()
        threading.Thread(target=self._start_api, daemon=True).start()
        console.print("[cyan]🌐 API Flask iniciada em thread separada[/cyan]")

    # -------------------------------
    # API FLASK
    # -------------------------------
    def _setup_api(self):
        @self.app.route("/plantao", methods=["POST"])
        def plantao_api():
            """Endpoint para adicionar/remover médicos do plantão via API."""
            data = request.json
            user_id = int(data["user_id"])
            acao = data["acao"]  # entrar / sair

            medicos = self.carregar_plantao()

            if acao == "entrar" and user_id not in medicos:
                medicos.append(user_id)
                console.print(f"[green]✅ Usuário {user_id} entrou no plantão[/green]")
            elif acao == "sair" and user_id in medicos:
                medicos.remove(user_id)
                console.print(f"[red]❌ Usuário {user_id} saiu do plantão[/red]")

            self.salvar_plantao(medicos)
            return {"status": "ok"}

    def _start_api(self):
        self.app.run(host="0.0.0.0", port=5000)

    # -------------------------------
    # ARQUIVOS DE PLANTÃO
    # -------------------------------
    def carregar_plantao(self) -> List[int]:
        """Carrega lista de médicos do plantão."""
        if not os.path.exists(ARQUIVO_PLANTAO):
            with open(ARQUIVO_PLANTAO, "w") as f:
                json.dump([], f)
        with open(ARQUIVO_PLANTAO, "r") as f:
            return json.load(f)

    def salvar_plantao(self, lista: List[int]) -> None:
        """Salva lista de médicos no arquivo JSON."""
        with open(ARQUIVO_PLANTAO, "w") as f:
            json.dump(lista, f, indent=4)

    # -------------------------------
    # EVENTOS DO BOT
    # -------------------------------
    async def setup_hook(self):
        """Carrega todos os cogs e sincroniza comandos slash."""
        await self.carregar_cogs()
        await self.tree.sync()
        console.print("[bold green]🌐 Slash Commands sincronizados globalmente[/bold green]")

    async def on_ready(self):
        console.print(f"[bold green]✅ Bot conectado como {self.user}[/bold green]")
        self.loop.create_task(self.status_task())

    # -------------------------------
    # STATUS CICLICO
    # -------------------------------
    async def status_task(self):
        """Atualiza o status do bot periodicamente com logs bonitos."""
        await self.wait_until_ready()
        while not self.is_closed():
            atividade = next(self.status_list)
            await self.change_presence(status=discord.Status.online, activity=atividade)
            console.print(f"[cyan]🔄 Status atualizado para:[/cyan] {atividade.name}")
            await asyncio.sleep(STATUS_INTERVAL)

    # -------------------------------
    # COGS
    # -------------------------------
    async def carregar_cogs(self):
        """Carrega todos os cogs da pasta ./cogs."""
        for arquivo in os.listdir("./cogs"):
            if arquivo.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{arquivo[:-3]}")
                    console.print(f"[yellow]📦 Cog carregado:[/yellow] {arquivo}")
                except Exception as e:
                    console.print(f"[red]⚠️ Erro ao carregar {arquivo}:[/red] {e}")

# -------------------------------
# RODAR O BOT
# -------------------------------
if __name__ == "__main__":
    bot = PlantaoBot()
    bot.run(os.getenv("DISCORD_TOKEN"))