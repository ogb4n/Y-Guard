import os, sys, discord, json, time, asyncio, re
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

dev = 1092392902442893352

class tools(commands.Cog):
    """Outils et fontionnalités"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Affiche la date et l'heure")
    async def date(self, ctx):
        """Affiche date et heure locale <cmd>"""
        await ctx.send(time.ctime())

    @commands.command(aliases=['reboot'])
    @commands.has_any_role(dev)
    async def restart (self, ctx):
        """Redémarre le bot"""
        embedDeco=discord.Embed(title="⚗️ Y-Guard Status.. 🛠️ ", description="""Y-Guard redémarre...
                                                                                                    Patientez quelques secondes.. """, color=0xF1D50E)
        await ctx.send(embed=embedDeco)
        restart_bot()

    @commands.command(aliases=['purge'])                                 
    @commands.has_any_role(dev)
    async def clear(self, ctx, amount=0):
        """Permet de nettoyer un salon <cmd number> """
        await ctx.channel.purge(limit= amount+1)
        await ctx.send(f"Ce salon a été nettoyé de {amount} messages")


async def setup(bot):
    await bot.add_cog(tools(bot))