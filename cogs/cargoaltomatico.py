import discord
from discord.ext import commands

# ID DO CARGO QUE VAI SER DADO AUTOMATICAMENTE
AUTO_ROLE_ID =   # coloque o ID do cargo aqui

class CargoAutomatico(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Evento quando alguém entra no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        cargo = member.guild.get_role(AUTO_ROLE_ID)

        if cargo:
            try:
                await member.add_roles(cargo)
                print(f"✅ Cargo '{cargo.name}' dado para {member.name}")
            except Exception as e:
                print(f"❌ Erro ao dar cargo para {member.name}: {e}")
        else:
            print("⚠️ Cargo não encontrado. Verifique o ID.")

async def setup(bot):
    await bot.add_cog(CargoAutomatico(bot))