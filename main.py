# made by msfdhoney(ogb4n) & eltitch
# 2022 | for private use only

from unicodedata import category
from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View
from discord import app_commands
from dotenv import load_dotenv
from logger import *
import os, sys, discord, json, dotenv, datetime, asyncio, argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    return args

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
load_dotenv()

bot = commands.Bot(command_prefix= '.', intents=intents)
@bot.remove_command('help')

# =========================================================
# ===================== BOT BEHAVIOUR =====================
# =========================================================

@bot.event
async def on_ready():
    logger.addInfo("The bot is ready")
    channel = bot.get_channel(int(1092393670772265010))
    embedCo= discord.Embed(title="⚗️ Y-Guard est connecté  ✅ ", description="Y-Guard est prêt à bosser !", color=0x49FF37)
    embedLoad= discord.Embed(title="⚗️ Y-Guard Commands  ✅ ", description="Y-Guard Loaded commands !", color=0x79b8ff)

    await channel.send(embed=embedCo)

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            logger.addInfo(f"les commandes {filename[:-3]} ont été chargées")
    await channel.send(embed=embedLoad)
    # members = 0
    # for guild in bot.guilds:
    #     members += guild.member_count - 3
    await bot.change_presence(activity=discord.Streaming(name="Dhoney", url="https://twitch.tv/idhoney"))


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        if after.channel.id == 1092388849176551438:
            for guild in bot.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=1092394010955497503)
                channel2 = await guild.create_voice_channel(name=f'📎 {member.display_name} ', category=maincategory, user_limit=5)
                await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                await member.move_to(channel2)
                logger.addInfo(f"un channel temporaire à été créé pour : {member.display_name}")

                def check(x, y, z):
                    return len(channel2.members) == 0
                await bot.wait_for('voice_state_update', check=check)
                await channel2.delete()
                logger.addInfo(f"Le channel de {member.display_name} a été supprimé ")


# =========================================================
# ================== BOT MAIN COMMANDS ====================
# =========================================================

    @commands.command(name="load")
    @commands.has_any_role(1092392902442893352)
    async def load(self, ctx, extension):
        """Permet de charger les modules"""
        bot.load_extension(f'cogs.{extension}')
        logger.addInfo('Les cogs on été chargés')



if __name__ == '__main__':
    args = getArgs()
    logger = Logger("logs.log", args.debug)
    token = os.getenv("TOKEN")
    bot.run(token)
