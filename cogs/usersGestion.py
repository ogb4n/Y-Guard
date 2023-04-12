import os, sys, discord, json, time, asyncio, re
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path
from logger import *

with open('config.json') as file:
    data = json.load(file)
    roles = data['roles']

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

class usersGestion(commands.Cog):
    """Outils et fontionnalités"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(roles['Dev'], roles['777'])
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        """Renvoie un utilisateur à la maison <cmd user>"""

        if member is not None:
            await ctx.guild.kick(member, reason=reason)
            if member != ctx.guild.members:
                await ctx.send(f"{member} has been kicked from the server")
                logger.addWarning((f"{member.id} has been kicked from the server pour la raison {reason}"))
        else:
            await ctx.send("Merci de définir un utilisateur à renvoyer chez lui.")
            logger.addWarning(f"{ctx.author.display_name} a essayé de kick : personne")

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