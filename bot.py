LOG_CHANNEL_ID = 1447675219132289075 # canal logs-tickets
STAFF_ROLE_ID = 1447675210789818386 # cargo da staff

import discord
from discord.ext import commands
import asyncio
import itertools
import os
from discord.ext import tasks
import json
import os
from flask import Flask, request
import threading

app = Flask(__name__)

ARQUIVO_PLANTAO = "plantao.json"

def carregar_plantao():
    if not os.path.exists(ARQUIVO_PLANTAO):
        with open(ARQUIVO_PLANTAO, "w") as f:
            json.dump([], f)
    with open(ARQUIVO_PLANTAO, "r") as f:
        return json.load(f)

def salvar_plantao(lista):
    with open(ARQUIVO_PLANTAO, "w") as f:
        json.dump(lista, f, indent=4)

@app.route("/plantao", methods=["POST"])
def plantao_api():
    data = request.json
    user_id = int(data["user_id"])
    acao = data["acao"]  # entrar / sair

    medicos = carregar_plantao()

    if acao == "entrar" and user_id not in medicos:
        medicos.append(user_id)

    if acao == "sair" and user_id in medicos:
        medicos.remove(user_id)

    salvar_plantao(medicos)
    return {"status": "ok"}

def iniciar_api():
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=iniciar_api, daemon=True).start()

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)
@bot.event
async def setup_hook():
    await carregar_cogs()
    await bot.tree.sync()
    print("🌐 Slash Commands sincronizados globalmente")



status_list = itertools.cycle([
    discord.Game(name="Salvando vidas 🏥"),
    discord.Game(name="Atendendo pacientes 🩺"),
    discord.Game(name="Em plantão 24h 🚑"),
    discord.Game(name="Cuidando de todos 🏙️"),
])

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    bot.loop.create_task(status_task())

async def status_task():
    await bot.wait_until_ready()

    while not bot.is_closed():
        atividade = next(status_list)
        await bot.change_presence(
            status=discord.Status.online,
            activity=atividade
        )
        await asyncio.sleep(15)




async def carregar_cogs():
    for arquivo in os.listdir("./cogs"):
        if arquivo.endswith(".py"):
            await bot.load_extension(f"cogs.{arquivo[:-3]}")


bot.run(os.getenv("DISCORD_TOKEN"))
