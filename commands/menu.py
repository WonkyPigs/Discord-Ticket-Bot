from msilib.schema import File
import nextcord
from nextcord.ext import commands
import asyncio
import json
from datetime import datetime

with open("configuration.json", "r") as config:
    data = json.load(config)
    ticket_role = data["TICKET_ROLE"]
    transcript_channel_id = data["TRANSCRIPTS_CHANNEL_ID"]
    logging_channel_id = data["LOGGING_CHANNEL_ID"]
    guild_id = data["GUILD_ID"]
    category1 = data["TICKET_CATEGORY_1"]
    category2 = data["TICKET_CATEGORY_2"]
    category3 = data["TICKET_CATEGORY_3"]
    category1_desc = data["CATEGORY_1_DESC"]
    category2_desc = data["CATEGORY_2_DESC"]
    category3_desc = data["CATEGORY_3_DESC"]

class CloseTicketButton(nextcord.ui.View):
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Close", style=nextcord.ButtonStyle.red)
    async def closeticket(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = "close"
        self.stop()

class Select(nextcord.ui.Select):
    def __init__(self, ctx:commands.Context, channel, message, bot):
        self.ctx = ctx
        self.channel = channel
        self.message = message
        self.bot = bot
        options=[
            nextcord.SelectOption(label=f"{category1}",description=f"{category1_desc}"),
            nextcord.SelectOption(label=f"{category2}",description=f"{category2_desc}"),
            nextcord.SelectOption(label=f"{category3}",description=f"{category3_desc}")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: nextcord.Interaction):
        await self.message.delete()
        await MakeATicket(interaction, self.channel,self.values[0], self.bot)

class SelectView(nextcord.ui.View):
    def __init__(self, ctx:commands.Context, channel, message, bot):
        super().__init__(timeout=None)
        self.add_item(Select(ctx, channel, message, bot))

class OpenTicketClass(nextcord.ui.View):
    def __init__(self, ctx: commands.Context, bot) -> None:
        self.ctx = ctx
        self.bot = bot
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Open Ticket", style=nextcord.ButtonStyle.blurple, emoji="")
    async def ticket_category_1(self, button:nextcord.ui.Button, interaction: nextcord.Interaction):
        await StartTicket(interaction, self.bot)

##################################################################################

async def DisplayTicketMenu(ctx, bot):
    embed = nextcord.Embed(title="Create a support ticket", description="In need of support? Just open a ticket below", color=0x11ed11)
    await ctx.send(embed=embed, view=OpenTicketClass(ctx, bot))

async def StartTicket(interaction, bot ):
    guild = bot.get_guild(guild_id)
    channel = await guild.create_text_channel(f"{interaction.user.display_name}")
    embed = nextcord.Embed(title="Choose a reason", description="Please select a reason for your ticket", color=0x11ed11)
    await channel.set_permissions(guild.default_role, view_channel=False)   
    await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, view_channel=True)
    await channel.set_permissions(guild.get_role(ticket_role), send_messages=True, read_messages=True, view_channel=True)
    message = await channel.send(f"{interaction.user.mention}")
    await message.edit(content=f"{interaction.user.mention}",embed=embed, view=SelectView(interaction, channel, message, bot))   

async def MakeATicket(interaction, channel, issue, bot):
    try:
        guild = bot.get_guild(guild_id)
        await channel.edit(name=f"{issue}-{interaction.user.display_name}")
        view = CloseTicketButton(interaction)
        await channel.send(interaction.user.mention)
        embed = nextcord.Embed(title=f"{issue}", description=f"Hey {interaction.user.mention}!\n\nThank you for creating a support ticket.\nWhilst you wait for a staff response, in your following message please answer the format to the best of your ability!")
        embed.add_field(name="Format", value="```Issue:\nAny proof if related:\nAny other info:```")
        embed.add_field(name="Information", value=f"```Category: {issue}\nOpened by: {interaction.user.display_name}```")
        embed.set_footer(text=f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}")
        await channel.send(embed=embed, view=view)
        await view.wait()

        if view.value == "close":
            embed = nextcord.Embed(title="Deleting ticket", description="Deleting ticket in 5 seconds!", color=0xed1123)
            await channel.send(embed=embed)
            await asyncio.sleep(5)
            if transcript_channel_id != 0:
                fileName = f"{issue}-{interaction.user.display_name}.txt"
                with open(fileName, "w") as file:
                    async for msg in channel.history(limit=None, oldest_first=True):
                        file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")
                file = nextcord.File(fileName)
                transcript_channel = channel.guild.get_channel(transcript_channel_id)
                await transcript_channel.send(file=file)
            await channel.delete()

    except Exception as e:
        print(e)