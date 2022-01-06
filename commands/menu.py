from datetime import datetime
import nextcord
from nextcord.ext import commands
import asyncio
import json

with open("configuration.json", "r") as config: 
	data = json.load(config)
	category1 = data["TICKET_CATEGORY_1"]
	category2 = data["TICKET_CATEGORY_2"]
	category3 = data["TICKET_CATEGORY_3"]

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

    @nextcord.ui.button(label=f"{category1}", style=nextcord.ButtonStyle.blurple)
    async def ticket_category_1(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = f"{category1}"
        self.stop()

    @nextcord.ui.button(label=f"{category2}", style=nextcord.ButtonStyle.blurple)
    async def ticket_category_2(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = f"{category2}"
        self.stop()

    @nextcord.ui.button(label=f"{category3}", style=nextcord.ButtonStyle.blurple)
    async def ticket_category_3(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = f"{category3}"
        self.stop()

##################################################################################

async def DisplayTicketMenu(ctx):
    view = OpenTicketButton(ctx)
    embed = nextcord.Embed(title="Create a support ticket", description="In need of support? Click the button below to create a ticket.")
    await ctx.reply(embed=embed, view=view)

async def TicketOptions(ctx):
    view = TicketOptionsClass(ctx)
    embed = nextcord.Embed(title="Support", description="Please pick a ticket category from the options below to finish creating your ticket.")
    await ctx.send(embed=embed, view=view)
    await view.wait()

    if view.value == None:
        await ctx.send("You took too long to choose! Try again later.")
    
    else:
        await MakeATicket(ctx, view.value)

async def MakeATicket(ctx, issue):
    try:
        view = CloseTicketButton(ctx)
        channel = await ctx.guild.create_text_channel(f"{issue}-{ctx.display_name}")
        message = await channel.send(ctx.mention)
        await message.delete()
        embed = nextcord.Embed(title=f"{issue}", description=f"Hey {ctx.mention}!\n\nThank you for creating a support ticket.\nWhilst you wait for a staff response, in your following message please answer the format to the best of your ability!")
        embed.add_field(name="Format", value="```IGN:\nIssue:\nAnything Else:```")
        embed.add_field(name="Information", value=f"```Category: {issue}\nOpened by: {ctx}```")
        embed.set_footer(text=f"{datetime.datetime.today().day}/{datetime.datetime.today().month}/{datetime.datetime.today().year}")
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