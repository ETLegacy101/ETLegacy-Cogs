import time
import discord
from discord.ext import commands
from .utils.chat_formatting import *
from random import randint
from random import choice as randchoice
import asyncio

class ETLegacy:
	def __init__(self, bot):
		self.bot = bot

	async def on_server_join(self, server):
		channel = server.default_channel
		donate = "https://www.patreon.com/ETLegacy"
		sinv = "https://discord.gg/MqQsmF7"
		inv ="https://bot.discord.io/trinityv4"
		em = discord.Embed(description="**Hey there**\n I'm Trinity and i got asked to join by an Admin!\n My current prefixes is are `*` and if you want all the commands do `*help`!\n Here some of the main features i got!\n **Music**: I can play music if you did `*play` and the song you want, i will connect to your vc.\n **Afk**: Tell the bot when you are AFK, if someone mentions you the bot tells them the person if afk with custom message command for it is `*afk` or `*away`\n **Modlog**: This will logs all kicks and bans\n if you typed `*modset modlog #channelname`\n when you do that i will log all kicks and bans!\n **Mute**: You can mute users for specific of time, it will Re-mute the user if he tries to bypass by leaving and joining again.\n If the bot was given the right permission, all you do is type `*mute @someone 10m test`\n The bot will setup a mute role with the right permissions for mute.\nDo `*roleset` it will set my roles for this server!\nIf you need more commands do `*help`.\n Have a great day", colour=discord.Colour.blue())
		if self.bot.user.avatar_url:
			em.set_author(name="", url=self.bot.user.avatar_url)
			em.set_footer(text="Currently in {} Servers".format(len(self.bot.servers)), icon_url=self.bot.user.avatar_url)
			em.add_field(name="Invite", value="[Click Here]({})".format(inv))
			em.add_field(name="Support Server", value="[Click Here]({})".format(sinv))
			em.add_field(name="Donate", value="[Click Here]({})".format(donate))
			em.add_field(name="Owner", value="<@153286414212005888>")
			em.set_thumbnail(url=self.bot.user.avatar_url)
		await self.bot.send_message(server, embed=em)

def setup(bot):
	n = ETLegacy(bot)
	bot.add_cog(n)
