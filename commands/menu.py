from datetime import datetime
import nextcord
from nextcord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
ip = os.getenv("SERVER_IP")

class OpenTicketButton(nextcord.ui.View):
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Create a Ticket", style=nextcord.ButtonStyle.green)
    async def createticket(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        ctx = interaction.user
        await TicketOptions(ctx)

class CloseTicketButton(nextcord.ui.View):
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Close", style=nextcord.ButtonStyle.red)
    async def closeticket(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id != self.ctx.id:
            await interaction.response.send_message(f"Sorry but this button isn't for you! {interaction.user.mention}", ephemeral=True)
        else:
            self.value = "close"
            self.stop()

class TicketOptionsClass(nextcord.ui.View):
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
        super().__init__(timeout=120)
        self.value = None

    @nextcord.ui.button(label="General", style=nextcord.ButtonStyle.blurple)
    async def generalissues(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "General Issues"
        self.stop()

    @nextcord.ui.button(label="Factions", style=nextcord.ButtonStyle.blurple)
    async def factionsissues(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "Factions Issues"
        self.stop()

    @nextcord.ui.button(label="Buycraft", style=nextcord.ButtonStyle.blurple)
    async def buycraftissues(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "Buycraft Issues"
        self.stop()

    @nextcord.ui.button(label="Player Reports", style=nextcord.ButtonStyle.blurple)
    async def playerreport(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "Player Reports"
        self.stop()

##################################################################################

async def DisplayTicketMenu(ctx):
    view = OpenTicketButton(ctx)
    embed = nextcord.Embed(title="Create a support ticket", description="In need of support? Click the button below to create a ticket.")
    await ctx.reply(embed=embed, view=view)

async def TicketOptions(ctx):
    view = TicketOptionsClass(ctx)
    embed = nextcord.Embed(title="Support", description="Please pick a ticket category from the dropdown below to finish creating your ticket.")
    await ctx.send(embed=embed, view=view)
    await view.wait()

    if view.value == None:
        await ctx.send("You took too long to choose! try again later.")
    
    else:
        issue = view.value
        await MakeATicket(ctx, issue)

async def MakeATicket(ctx, issue):
    try:
        view = CloseTicketButton(ctx)
        channel = await ctx.guild.create_text_channel(f"{issue}-{ctx.display_name}")
        message = await channel.send(ctx.mention)
        await message.delete()
        embed = nextcord.Embed(title=f"{issue}", description=f"Hey {ctx.mention}!\n\nThank you for creating a support ticket.\nWhilst you wait for a staff response, in your following message please answer the format to the best of your ability!")
        embed.add_field(name="Format", value="```IGN:\nIssue:\nAnything Else:```")
        embed.add_field(name="Information", value=f"```Category: {issue}\nOpened by: {ctx}```")
        embed.set_footer(text=f"{ip} | {datetime.datetime.today().day}/{datetime.datetime.today().month}/{datetime.datetime.today().year}")
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False, view_channel=False)
        await channel.set_permissions(ctx, send_messages=True, read_messages=True, view_channel=True)
        await channel.send(embed=embed, view=view)
        await view.wait()

        if view.value == "close":
            await channel.set_permissions(ctx, send_messages=False, read_messages=True, view_channel=True)
            embed = nextcord.Embed(title="Deleting ticket", description="Deleting ticket in 5 seconds!")
            await channel.send(embed=embed)
            await asyncio.sleep(5)
            await channel.delete()

    except Exception as e:
        print(e)