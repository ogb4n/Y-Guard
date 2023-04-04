import os, sys, discord, json, time
from discord.ext import commands
from pathlib import Path

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

class tools(commands.Cog):
    """Outils et fontionnalités"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Affiche la date et l'heure")
    async def date(self, ctx):
        """Affiche date et heure locale <cmd>"""
        await ctx.send(time.ctime())

    @commands.command(aliases=['reboot'])
    async def restart (self, ctx):
        """Redémarre le bot"""
        embedDeco=discord.Embed(title="⚗️ Y-Guard Status.. 🛠️ ", description="""Y-Guard redémarre...
                                                                                                    Patientez quelques secondes.. """, color=0xF1D50E)
        await ctx.send(embed=embedDeco)
        restart_bot()


async def setup(bot):
    await bot.add_cog(tools(bot))