import os, sys, discord, json, time, asyncio, re
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from contextlib import redirect_stdout
from pathlib import Path

dev = 1092392902442893352
admin = 1092389025261826140
muted = 1092586422453682298
player = 1092392222646882404

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

    @commands.command()
    @commands.has_any_role(dev, admin)
    async def mute(self, ctx, member: discord.Member, *, time:TimeConverter = None, reason= None,):
        """Rend muet un utilisateur <cmd user>"""
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted 🔇")
        playerRole = discord.utils.get(ctx.guild.roles, name="Player 🗺️")
        await member.add_roles(mutedRole)
        await member.remove_roles(playerRole)
        await member.edit(mute=True)
        await ctx.send(f"L'utilisateur <@{member.id}> à été rendu muet pendant {time}s" if time else f"Muted <@{member.id}>")
        if time:
            await asyncio.sleep(time)
            await member.remove_roles(mutedRole)
            await member.add_roles(playerRole)
            await member.edit(mute=False)
            await ctx.send(f"L'utilisateur <@{member.id}> peut à nouveau parler" if time else f"Muted <@{member.id}>")

    @commands.command()
    @commands.has_any_role(dev, admin)
    async def unmute(self, ctx, member: discord.Member):
        """Permet de démute un utilisateur <cmd user>"""
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted 🔇")
        playerRole = discord.utils.get(ctx.guild.roles, name="Player 🗺️")
        await member.remove_roles(mutedRole)
        await member.add_roles(playerRole)
        await member.edit(mute=False)
        await ctx.send({member}, "à été démute")

async def setup(bot):
    await bot.add_cog(usersGestion(bot))