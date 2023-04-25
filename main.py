# made by reapex
# 2023

from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View
from discord import app_commands
from dotenv import load_dotenv
from logger import *
import os, sys, discord, json, dotenv, datetime, asyncio, argparse

# =========================================================
# ================== DATABASE CONNEXION ===================
# =========================================================

import sqlite3
db = sqlite3.connect("db.sqlite")
cur = db.cursor()


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    return args

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

with open('config.json') as file:
    data = json.load(file)
    roles = data['roles']

load_dotenv()

bot = commands.Bot(command_prefix= '.', intents=intents)
guild = bot.get_guild(1092388848044101694)
@bot.remove_command('help')


# =========================================================
# ===================== BOT BEHAVIOUR =====================
# =========================================================

@tasks.loop(hours=1)
async def warns_check():
    cur.execute(f"SELECT discord_id FROM SANCTIONS WHERE warns >= 3")
    rows = cur.fetchall()

    for row in rows:
        discord_id = row[1]
        user = guild.get_member(discord_id)
        await user.add_roles(roles['blacklisted'])
    logger.addInfo('Le check à bien été exécuté et les utilisateurs concernés ont été blacklistés')
    cur.execute("UPDATE sanctions SET warns = 0 WHERE warns >= 3")
    db.commit()
    logger.addInfo('La liste des avertissements à été actualisée')

@bot.event
async def on_ready():
    logger.addInfo("Le bot est prêt")
    warns_check.start()
    
    logger.addInfo(f"le bot est connecté au serveur {guild}")

    for member in guild.members:
        try:
            cur.execute(f"SELECT * FROM sanctions WHERE discord_id = {member.id}")
            result = cur.fetchone()
            if not result:
                cur.execute(f"INSERT INTO sanctions(discord_id) VALUES ({member.id})")
        except sqlite3.Error as e:
            print("Error inserting data into database:", e)
    db.commit()
    logger.addInfo("La base de donnée s'est bien chargée")

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            logger.addInfo(f"les commandes {filename[:-3]} ont été chargées")
    
    channel = bot.get_channel(int(1092393670772265010))
    embedCo= discord.Embed(title="⚗️ Y-Guard est connecté  ✅ ", description="Y-Guard est prêt à bosser !", color=0x49FF37)
    embedLoad= discord.Embed(title="⚗️ Y-Guard Commands  ✅ ", description="Y-Guard Loaded commands !", color=0x79b8ff)

    with open('config.json') as file:
        data = json.load(file)
        roles = data['roles']

    await channel.send(embed=embedCo)
    await channel.send(embed=embedLoad)


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
# ================== BOT MAIN =============================
# =========================================================

if __name__ == '__main__':
    args = getArgs()
    logger = Logger("logs.log", args.debug)
    token = os.getenv("TOKEN")
    bot.run(token)
