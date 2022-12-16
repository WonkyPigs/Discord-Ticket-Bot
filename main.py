import nextcord
from nextcord.ext import commands
import json

# importing command files
from commands.menu import *

with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["BOT_TOKEN"]
	prefix = data["PREFIX"]
	owner_id = data["OWNER_ID"]

bot = commands.AutoShardedBot(command_prefix=prefix)
bot.remove_command('help')

#### READY UP AND BOT EVENTS ####

@bot.event  
async def on_ready():
    print("-----------------------------------------")
    print(f"{bot.user} has connected to discord!")
    print(f"Prefix set to '{prefix}'")
    print("-----------------------------------------")
    await bot.change_presence(status=nextcord.Status.online)

#### COMMANDS ####

@bot.command(name="menu")
async def TicketMenu(ctx):
    if ctx.author.id != owner_id:
        await ctx.reply("how about no?")
        return
    await DisplayTicketMenu(ctx, bot)

#### MAKE THE BOT COME TO LIFE ####
bot.run(token)