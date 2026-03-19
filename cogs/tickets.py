import discord
from discord.ext import commands
from datetime import datetime
import asyncio

LOG_CHANNEL_NAME = "🩹・log-ticket"

# =======================
# DESCRIÇÕES POR SETOR
# ======================
tickets = {
    1482815765798322418: {  # PEDIATRIA
        "titulo": "🧒 PEDIATRIA",
        "descricao": (
            "**NOME DA CRIANÇA:**\n"
            "**ID DA CRIANÇA:**\n\n"
            "**NOME DO(S) RESPONSÁVEL(IS):**\n"
            "**ID DO(S) RESPONSÁVEL(IS):**\n"
            "**TELEFONE(S) PARA CONTATO:**\n\n"
            "**PRIMEIRA CONSULTA?** ( ) SIM / ( ) NÃO\n"
            "**JÁ TEVE PEDIATRA ANTERIOR?** ( ) SIM / ( ) NÃO\n"
            "**SE SIM, MARQUE O @ DO PEDIATRA ANTERIOR:**\n\n"
            "📌 **INFORMAÇÃO IMPORTANTE:**\n"
            "Após o agendamento, o médico tem até **24 horas** para entrar em contato com o paciente "
            "para marcar o melhor dia e horário para ambos.\n\n"
        ),
        "image": "https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/14D3AF2A-3AAD-4EC6-A073-74A019A1D0A3.png"
    },

    1482816148679557373: {  # PSICOLOGIA
        "titulo": "🧠 PSICOLOGIA",
        "descricao": (
            "**NOME COMPLETO:**\n"
            "**PASSAPORTE:**\n"
            "**TELEFONE:**\n\n"
            "**MOTIVO DA CONSULTA:**\n"
            "[Adoção / Cirurgia Plástica / Redesignação Sexual / Limpeza de Ficha / "
            "Porte e Renovação de Porte / Terapia]\n\n"
            "**DIA E HORÁRIO:**\n"
            "[Manhã / Tarde / Noite]\n\n"
            "**PRINT DO [F11] LEGÍVEL!**\n\n"
            "📌 **INFORMAÇÃO IMPORTANTE:**\n"
            "Após o agendamento, o médico tem até **24 horas** para entrar em contato "
            "com o paciente para marcar o melhor dia e horário para ambos.\n\n"
            "🧠 **Desejo um ótimo atendimento** 🩵"
        ),
        "image": "https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/1488EEF0-1380-4EF8-930D-8C8F560E8BA7.png"
    },

    1482816097274298451: {  # CIRURGIA
        "titulo": "💉 CIRURGIA",
        "descricao": (
            "**INFORMAÇÕES DO PACIENTE**\n"
            "• Nome:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Tipo de cirurgia:\n"
        ),
        "image": "https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/A013B021-450B-4A4E-81CA-F62AD02C668A.png"
    },

    1482815912183857383: {  # OBSTETRÍCIA
        "titulo": "🤰 OBSTETRÍCIA",
        "descricao": (
            "📌 **AGENDAMENTOS ABERTOS!**\n\n"
            "Para realizar seu agendamento, não se esqueça de adicionar as informações essenciais "
            "para que seu pedido possa ser aceito e concluído com sucesso:\n\n"
            "**NOME:**\n"
            "**ID:**\n"
            "**TELEFONE:**\n"
            "**DATA DE NASCIMENTO:**\n"
            "**DATA E HORÁRIO DISPONÍVEIS:**\n"
            "**QUANTAS CRIANÇAS E O SEXO DOS BEBÊS:**\n\n"
            "**Enviar resultado do BetaHCG para primeira consulta.**\n"
            "Caso seu pré-natal já tenha sido iniciado antes, informe no ticket qual foi seu último "
            "pré-natal realizado e marque a médica responsável.\n\n"
            "**Agendamentos devem ser realizados com 1 dia de antecedência** "
            "e devem ser respeitados. Caso não possa comparecer, avise antes para reagendar. "
            "O não comparecimento pode gerar multa por atraso ou falta na consulta."
        ),
        "image": "https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/CBF1DA5A-5A6D-42B2-9971-5C358A215655.png"
    },

    1447675217500442636: {  # LAUDOS
        "titulo": "📋 LAUDOS MÉDICOS",
        "descricao": (
            "Bem-vindo ao setor de **Laudos Médicos** 📋\n\n"
            "📌 Informe:\n"
            "• Tipo de laudo\n"
            "• Nome do paciente\n"
            "• Data do exame\n\n"
            "Nossa equipe irá analisar sua solicitação."
        ),
        "image": "https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/CBF1DA5A-5A6D-42B2-9971-5C358A215655.png"
    },
}
DESCRICOES_SETOR = {

    1482816338572607618: {  # CLÍNICO GERAL
        "titulo": "🩺 CLÍNICO GERAL",
        "descricao": (
            "**TIPO DE CONSULTA: EXAME DE DNA**\n"
            "**INFORMAÇÕES DO RESPONSÁVEL:**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Sexo: (   ) Feminino  (   ) Masculino\n\n"

            "**INFORMAÇÕES DA CRIANÇA:**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Sexo: (   ) Feminino  (   ) Masculino\n\n"

            "**TIPO DE CONSULTA: BETA-HCG**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n\n"

            "**TIPO DE CONSULTA: RISCO CIRÚRGICO**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Sexo: (   ) Feminino  (   ) Masculino\n\n"

            "**TIPO DE CONSULTA: ADMISSÃO / DEMISSÃO**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Sexo: (   ) Feminino  (   ) Masculino\n"
            "• Cargo/Função:\n"
            "• Empresa/Instituição:\n\n"

            "**TIPO DE CONSULTA: DOSAGEM HORMONAL**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Sexo: (   ) Feminino  (   ) Masculino\n\n"

            "**TIPO DE CONSULTA: HEMOGRAMA COMPLETO**\n"
            "• Nome:\n"
            "• Data de Nascimento:\n"
            "• Idade:\n"
            "• ID:\n"
            "• Telefone:\n"
            "• Sexo: (   ) Feminino  (   ) Masculino\n"
        ),
         "image": "https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/6BB1561E-828E-4653-868B-A164FAEC1D23.png"
    },
}
CARGOS_SETOR = {
    1482815765798322418: 1459032319380819999,  # PEDIATRIA -> ID do cargo Pediatria
    1482816148679557373: 1459032319380819997,  # PSICOLOGIA -> ID do cargo Psicologia
    1482816097274298451: 1459032319380820000,  # CIRURGIA -> ID do cargo Cirurgia
    1482815912183857383: 1459032319380820001,  # OBSTETRÍCIA -> ID do cargo Obstetrícia
    1482816338572607618: 1459032321977225360,  # CLÍNICO GERAL -> ID do cargo Clínico Geral
}
# =======================
# BOTÃO FECHAR TICKET
# =======================
class CloseTicketView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def send_log(self, guild: discord.Guild, embed: discord.Embed):
        log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
        if log_channel:
            await log_channel.send(embed=embed)

    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        guild = interaction.guild

        log = discord.Embed(
            title="🔒 Ticket Fechado",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        log.add_field(name="Canal", value=channel.name)
        log.add_field(name="Fechado por", value=interaction.user.mention)

        await self.send_log(guild, log)

        await interaction.response.send_message(
            "🔒 Ticket será fechado em 5 segundos...",
            ephemeral=True
        )

        await asyncio.sleep(5)

        if not channel.permissions_for(guild.me).manage_channels:
            await interaction.followup.send(
                "❌ Não tenho permissão para apagar este canal.",
                ephemeral=True
            )
            return

        await channel.delete()


# =======================
# PAINEL DE TICKETS
# =======================
class TicketView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def send_log(self, guild: discord.Guild, embed: discord.Embed):
        log_channel = discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)
        if log_channel:
            await log_channel.send(embed=embed)

    async def criar_ticket(self, interaction: discord.Interaction, categoria_id: int):
        guild = interaction.guild

        categoria = discord.utils.get(guild.categories, id=categoria_id)
        if not categoria:
            await interaction.response.send_message(
                f"❌ Categoria com ID {categoria_id} não encontrada.",
                ephemeral=True
            )
            return

        cargo_id = CARGOS_SETOR.get(categoria_id)
        cargo_setor = guild.get_role(cargo_id)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        if cargo_setor:
            overwrites[cargo_setor] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=categoria,
            overwrites=overwrites
        )

        info = tickets.get(categoria_id) or DESCRICOES_SETOR.get(categoria_id)

        if info:
            embed = discord.Embed(
                title=info["titulo"],
                description=info["descricao"],
                color=discord.Color.dark_gold()
            )
            if "image" in info:
                embed.set_image(url=info["image"])
        else:
            embed = discord.Embed(
                title="🎫 ABERTURA DE TICKET – HOSPITAL FLOW",
                description="Descreva sua solicitação.",
                color=discord.Color.dark_gold()
            )
            embed.set_image(url="https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/image.png")

        await channel.send(
            f"{interaction.user.mention}",
            embed=embed,
            view=CloseTicketView(self.bot)
        )

        log = discord.Embed(
            title="🎫 Ticket Criado",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        log.add_field(name="Usuário", value=interaction.user.mention)
        log.add_field(name="Categoria", value=categoria.name)
        log.add_field(name="Canal", value=channel.mention)

        await self.send_log(guild, log)

        await interaction.response.send_message(
            f"✅ Ticket criado em {channel.mention}",
            ephemeral=True
        )

    @discord.ui.button(label="🧒 Pediatria", style=discord.ButtonStyle.danger)
    async def pediatria(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, 1482815765798322418)

    @discord.ui.button(label="🤰 Obstetrícia", style=discord.ButtonStyle.danger)
    async def obstetria(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, 1482815912183857383)

    @discord.ui.button(label="🧠 Psicologia", style=discord.ButtonStyle.danger)
    async def psicologia(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, 1482816148679557373)

    @discord.ui.button(label="💉 Cirurgia", style=discord.ButtonStyle.danger)
    async def cirurgia(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, 1482816097274298451)

    @discord.ui.button(label="🩺 Clínico Geral", style=discord.ButtonStyle.danger)
    async def clinico(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_ticket(interaction, 1482816338572607618)
# =======================
# COG
# =======================
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def painel(self, ctx):
        embed = discord.Embed(
            title="🎫 PAINEL DE TICKETS – HOSPITAL FLOW",
            description="Escolha abaixo o setor desejado.",
            color=discord.Color.dark_gold()
        )

        embed.set_image(url="https://r2.fivemanage.com/7sUTqcu7vprswr5yQCsH5/image.png")

        await ctx.send(embed=embed, view=TicketView(self.bot))
async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))