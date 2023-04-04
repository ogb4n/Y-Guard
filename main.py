# made by msfdhoney(ogb4n) & eltitch
# 2022 | for private use only



from unicodedata import category
from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View
from discord import app_commands
from dotenv import load_dotenv

import os, sys, discord, json, dotenv

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
load_dotenv()

bot = commands.Bot(command_prefix= '.', intents=intents)
@bot.remove_command('help')


def commandsLoader():
    loadEmbed=discord.Embed(title="⚗️ Commands Loader  ✅ ", description="Les commandes ont bien chargé !", color=0x49FF37)
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            channel.send(embed=loadEmbed)


# =========================================================
# ===================== Bot Behaviour =====================
# =========================================================

@bot.event
async def on_ready():

    print("""

░█▀▄░█░█░█▀█░▀█▀░█▀█░█▀▀
░█▀▄░█░█░█░█░░█░░█░█░█░█
░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀
code by b4n
""")
    commandsLoader()

    channel = bot.get_channel(int(1092393670772265010))
    embedco=discord.Embed(title="⚗️ Y-Guard est connecté  ✅ ", description="Y-Guard est prêt à bosser !", color=0x49FF37)
    await channel.send(embed=embedco)
    
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity=discord.Streaming(name="Dhoney", url="https://twitch.tv/idhoney"))


# @bot.event
# async def on_voice_state_update(member, before, after):
#     if after.channel != None:
#         if after.channel.id == 1007795192914530375:
#             for guild in bot.guilds:
#                 maincategory = discord.utils.get(
#                     guild.categories, id=1007389171498881045)
#                 channel2 = await guild.create_voice_channel(name=f'📎 room de  {member.display_name} ', category=maincategory, user_limit=5)
#                 await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
#                 await member.move_to(channel2)

#                 def check(x, y, z):
#                     return len(channel2.members) == 0
#                 await bot.wait_for('voice_state_update', check=check)
#                 await channel2.delete()


# =========================================================
# ===================== Server Commands ===================
# =========================================================


"""@bot.command()
@commands.has_any_role(1007389794365603931)
async def load(extension):
    Permet de charger les modules 
    bot.load_extension(f'fonctions.{extension}')
    print('Cog chargés')"""



token = os.getenv("TOKEN")
        
bot.run(token)
