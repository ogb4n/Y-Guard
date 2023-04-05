import os, sys, discord, json, time, asyncio, re
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

dev = 1092392902442893352
admin = 1092389025261826140

class tools(commands.Cog):
    """Outils et fontionnalités"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Affiche la date et l'heure")
    async def date(self, ctx):
        """Affiche date et heure locale <cmd>"""
        await ctx.send(time.ctime())

    @commands.command(aliases=['reboot'])
    @commands.has_any_role(dev, admin,)
    async def restart (self, ctx):
        """Redémarre le bot"""
        embedDeco=discord.Embed(title="⚗️ Y-Guard Status.. 🛠️ ", description="""Y-Guard redémarre...
                                                                                                    Patientez quelques secondes.. """, color=0xF1D50E)
        await ctx.send(embed=embedDeco)
        restart_bot()

    @commands.command(aliases=['purge'])                                 
    @commands.has_any_role(dev, admin)
    async def clear(self, ctx, amount=0):
        """Permet de nettoyer un salon <cmd number> """
        await ctx.channel.purge(limit= amount+1)
        await ctx.send(f"Ce salon a été nettoyé de {amount} messages")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.has_any_role(dev, admin)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        """Renvoie un utilisateur à la maison <cmd user>"""
        # if member.dm_channel == None:
        #     await member.create_dm()
        # await member.dm_channel.send(content=f"Vous avez été expulsé du serveur {ctx.guild} pour {reason}")

        if member is not None:
            await ctx.guild.kick(member, reason=reason)
            if member != ctx.guild.members:
                await ctx.send(f"{member} has been kicked from the server")
        else:
            await ctx.send("Merci de définir un utilisateur à renvoyer chez lui.")

async def setup(bot):
    await bot.add_cog(tools(bot))