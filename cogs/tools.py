import os, sys, discord, json, time, asyncio, re
from logger import *
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path

# =========================================================
# ================== DATABASE CONNEXION ===================
# =========================================================

import sqlite3
db = sqlite3.connect("db.sqlite")
cur = db.cursor()

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    return args

args = getArgs()
logger = Logger("logs.log", args.debug)

class tools(commands.Cog):
    """Outils et fontionnalités"""

    def __init__(self, bot):
        self.bot = bot

    with open("config.json") as file:
        data = json.load(file)
        roles = data['roles']

# =========================================================
# ============== DISCORD INTERACTIONS TOOLS ===============
# =========================================================

    @commands.command(aliases=['reboot'])
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def restart (self, ctx):
        """Redémarre le bot"""
        try:
            embedDeco=discord.Embed(title="⚗️ Y-Guard Status.. 🛠️ ", description="""Y-Guard redémarre...
                                                                                                    Patientez quelques secondes.. """, color=0xF1D50E)
            await ctx.send(embed=embedDeco)
            logger.addWarning(f"{ctx.author.display_name} à demandé au bot de redémarrer")
            restart_bot()
        except: 
            logger.addError(f"{ctx.author.display_name} n'a pas pu utiliser la commande restart / reboot")
            await ctx.send("Vous n'avez pas la permission d'éxécuter cette commande")

# =========================================================
# ================= CHANNEL FORMATTING ====================
# =========================================================

    @commands.command(aliases=['purge'])                                 
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def clear(self, ctx, amount=0):
        """Permet de nettoyer un salon <cmd number> """
        await ctx.channel.purge(limit= amount+1)
        await ctx.send(f"<@{ctx.author.id}> a nettoyé le salon de {amount} messages")
        logger.addInfo(f"<{ctx.author.id}> à nettoyé le channel <{ctx.channel.id}> | {ctx.channel.name} de : {amount} messages")

    
    @commands.command()
    @commands.has_any_role(roles['Dev'], roles['777'])
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
            Membre_id = cur.execute("SELECT role_id FROM roles WHERE role_name = 'Player'").fetchone()[0]
            Membre_id = int(Membre_id)
            Membre = guild.get_role(Membre_id)
            Membermention = f"<@&{Membre_id}>"
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