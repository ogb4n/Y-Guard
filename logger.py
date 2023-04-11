from unicodedata import category
from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View
from discord import app_commands
from dotenv import load_dotenv
import os, sys, discord, json, dotenv, datetime, asyncio, argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    return args

class Logger:
    def __init__(self, fileName,debugMode):
        self.fileName = fileName
        self.debugMode = debugMode

    def addInfo(self, info):
        strInfo = f"[{self.getTime()} - INFO] {info}"
        print(strInfo)
        with open(self.fileName, "a") as f:
            f.write(strInfo + "\n")

    def addError(self, error):
        strError = f"[{self.getTime()} - ERROR] {error}"
        print(strError)
        with open(self.fileName, "a") as f:
            f.write(strError + "\n")

    def addDebug(self, debug):
        if self.debugMode:
            strDebug = f"[{self.getTime()} - DEBUG] {debug}"
            print(strDebug)
            with open(self.fileName, "a") as f:
                f.write(strDebug + "\n")

    def addWarning(self, warning):
        strWarning = f"[{self.getTime()} - WARNING] {warning}"
        print(strWarning)
        with open(self.fileName, "a") as f:
            f.write(strWarning + "\n")

    def getTime(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

args = getArgs()
logger = Logger("logs.log", args.debug)