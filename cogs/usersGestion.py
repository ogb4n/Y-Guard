# =========================================================
# ================== FILE REQUIREMENTS ====================
# =========================================================

import os, sys, discord, json, time, asyncio, re
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path
from logger import *

# =========================================================
# ================== DATABASE CONNEXION ===================
# =========================================================

import sqlite3
db = sqlite3.connect("db.sqlite")
cur = db.cursor()

# =========================================================
# =============== SOME USEFULL DECLARATIONS ===============
# =========================================================

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

# =========================================================
# ================== CLASS FOR COMMANDS ===================
# =========================================================

class usersGestion(commands.Cog):
    """Outils et fontionnalités"""

    def __init__(self, bot):
        self.bot = bot

    with open('config.json') as file:
        data = json.load(file)
        roles = data['roles']

# ================== USER MGMT COMMANDS ====================

   # @commands.command()
   # @commands.has_any_role(roles['Staff'], roles['Dev'], roles['777'])
   # async def checkup(self, ctx):
   #     """Vérifie le nombre de sanctions et applique un blacklist en fonction"""
   #     cur.execute(f"SELECT discord_id FROM SANCTIONS WHERE warns >= 3")
   #     db.commit()


    @commands.command()
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        """Renvoie un utilisateur à la maison <cmd user>"""
    
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
            if member != ctx.guild.members:
                await ctx.send(f"{member} has been kicked from the server")
                logger.addWarning((f"{member.id} has been kicked from the server pour la raison {reason}"))
                cur.execute(f"UPDATE sanctions SET kicks = (kicks + 1) WHERE discord_id = ?",(str(member.id),))
                db.commit()
        else:
            await ctx.send("Merci de définir un utilisateur à renvoyer chez lui.")
            logger.addWarning(f"{ctx.author.display_name} a essayé de kick : personne")

    @commands.command()
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        """Banni un utilisateur du serveur <cmd user>"""
        # if member.dm_channel == None:
        #     await member.create_dm()
        # await member.dm_channel.send(
        #     content=f"Vous avez été banni du serveur {ctx.guild} pour {reason}")

        if member is not None:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"{member} has been banned")
            logger.addWarning((f"{member.id} has been banned from the server pour la raison {reason}"))
            cur.execute(f"UPDATE sanctions SET bans = (bans + 1) WHERE discord_id = ?",(str(member.id),))
            db.commit()
        else:
            await ctx.send("Merci de définir un utilisateur à renvoyer chez lui.")
            logger.addWarning(f"{ctx.author.display_name} a essayé de bannir : personne")

# ================== USER MUTE COMMANDS ====================

    @commands.command()
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def mute(self, ctx, member: discord.Member, *, time:TimeConverter = None, reason= None,):
        """Rend muet un utilisateur <cmd user>"""
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted 🔇")
        playerRole = discord.utils.get(ctx.guild.roles, name="Player 🗺️")
        await member.add_roles(mutedRole)
        await member.remove_roles(playerRole)
        await ctx.send(f"{ctx.author.display_name} a rendu muet <@{member.id}> pendant {time}s" if time else f"Muted <@{member.id}>")
        logger.addWarning(f"{ctx.author.display_name} a rendu muet <@{member.id}> pendant {time}s" if time else f"Muted <@{member.id}>")
        cur.execute(f"UPDATE sanctions SET mutes = (mutes + 1) WHERE discord_id = ?",(str(member.id),))
        db.commit()
        if time:
            await asyncio.sleep(time)
            await member.remove_roles(mutedRole)
            await member.add_roles(playerRole)
            await ctx.send(f"L'utilisateur <@{member.id}> peut à nouveau parler" if time else f"Muted <@{member.id}>")

    @commands.command()
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def unmute(self, ctx, member: discord.Member):
        """Permet de démute un utilisateur <cmd user>"""
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted 🔇")
        playerRole = discord.utils.get(ctx.guild.roles, name="Player 🗺️")
        await member.remove_roles(mutedRole)
        await member.add_roles(playerRole)
        await member.edit(mute=False)
        await ctx.send(f"{member} à été démute par {ctx.author.display_name}")
        logger.addWarning(f"{member} à été démute par {ctx.author.display_name}")

async def setup(bot):
    await bot.add_cog(usersGestion(bot))