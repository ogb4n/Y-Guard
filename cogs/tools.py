import os, sys, discord, json, time, asyncio, re
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

dev = 1092392902442893352
admin = 1092389025261826140
muted = 1092586422453682298
player = 1092392222646882404

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
    @commands.has_any_role(dev, admin)
    @commands.has_permissions(manage_roles=True)
    async def verifmessage(self, ctx):

        embedRegles3 = discord.Embed(
            title="J'ai lu les règles et suis prêt à rejoindre le serveur",
            color=6340196)
        embedRegles3.set_footer(
            text="cliques sur le bouton pour avoir accès au serveur et files prendre tes rôles !",
            icon_url="https://cdn3.emoji.gg/emojis/5704-verify.png")

        verifButton = discord.ui.Button(label="Accepter les règles",emoji="<:verify:1007821405682925588>", style=discord.ButtonStyle.green)


        async def verifButton_callback(interaction):

            guild = ctx.guild
            Membre = discord.utils.get(guild.roles, id=1092392222646882404)
            Membermention = '<@&1092392222646882404>'
            if Membre not in interaction.user.roles:
                await interaction.user.add_roles(Membre)
                await interaction.response.send_message(f"Vous avez obtenu le rôle {Membermention}. Bienvenue sur le serveur ! ✅", ephemeral = True)
            else:
                await interaction.response.send_message(f"Vous avez déjà le rôle {Membermention}.", ephemeral = True)


        verifButton.callback = verifButton_callback

        view = discord.ui.View(timeout=None)
        view.add_item(item=verifButton)
        await ctx.send(embed = embedRegles3,view = view)

async def setup(bot):
    await bot.add_cog(tools(bot))