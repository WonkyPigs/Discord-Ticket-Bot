import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os

# importing command files
from commands.menu import *

load_dotenv()

prefix = os.getenv("PREFIX")
bot = commands.AutoShardedBot(command_prefix=prefix)
bot.remove_command('help')

OWNER_ID = int(os.getenv("OWNER_ID"))

#### READY UP AND BOT EVENTS ####

@bot.event  
async def on_ready():
    print("-----------------------------------------")
    print(f"{bot.user} has connected to discord!")
    print(f"Prefix set to '{prefix}'")
    print(f"Help command - '{prefix}help'")
    print("-----------------------------------------")
    await bot.change_presence(status=nextcord.Status.online)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name='https://github.com/WonkyPigs/Discord-Ticket-Bot'))

#### COMMANDS ####

@bot.command(name="menu")
async def TicketMenu(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.reply("no")
        return
    await DisplayTicketMenu(ctx)

#### MAKE THE BOT COME TO LIFE ####
bot.run(os.getenv("BOT_TOKEN"))