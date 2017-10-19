import discord
from discord.ext import commands
from cogs.utils import checks
import os
import asyncio

class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """Trinity's info!"""
        prefix = ctx.prefix
        owner = "<@153286414212005888>"
        servers = len(self.bot.servers)
        members = len([e.name for e in self.bot.get_all_members()])
        invite = "https://bot.discord.io/trinityv4"
        donate = "https://www.patreon.com/ETLegacy"
        server = "https://discord.io/trinityhome"
        library = "Discord.py"
        channels = len([e.name for e in self.bot.get_all_channels()])
        commands = len(self.bot.commands)
        cogs = len(self.bot.cogs)
        e = discord.Embed(description="Trinity is a multi-functional bot written in python,\n It can do Music, Moderation, Utility and Fun commands.\n[Based on Red - Discord Bot](https://github.com/Twentysix26/Red-DiscordBot)\nJoin my support server: [Click here]({})\nInvite link: [Click here]({})\nPatreon: [Donate]({})".format(server, invite, donate), colour=discord.Colour.blue())
        e.add_field(name="Info:", value="Developer: {}\nServers: {} servers.\nPrefix: {}\nTotal Users: {}\nTotal Channels: {}\nTotal Commands: {}\nTotal Modules: {}\nLibrary: {}\nAPI Version: {}".format(owner, servers, ctx.prefix, members, channels, commands, cogs, library, discord.__version__))
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        e.set_thumbnail(url="https://i.imgur.com/7E0vIcO.png")
        try:
            await self.bot.say(embed=e)
        except discord.HTTPException:
            prefix = ctx.prefix
            owner = "<@153286414212005888>"
            servers = len(self.bot.servers)
            users = len([e.name for e in self.bot.get_all_members()])
            channels = len([e.name for e in self.bot.get_all_channels()])
            data = "Trinity is a multi-functional bot written in python,\n It can do Moderation, Utility and Fun commands.\n\n"
            data += "**Information:**\n"
            data += "Owner: {}\n".format(owner)
            data += "Prefix: {}\n".format(prefix)
            data += "Servers: {}\n".format(servers)
            data += "Total Users: {}\n".format(users)
            data += "Total Channels: {}\n".format(channels)
            data += "Total Commands: {}\n".format(len(self.bot.commands))
            data += "Total Modules: {}\n\n".format(len(self.bot.cogs))
            data += "**Links:** :link:\n"
            data += "Official Server: <https://discord.gg/MqQsmF7>\n"
            data += "Invite Url: <https://discordapp.com/oauth2/authorize?client_id=331609909823012875&scope=bot&permissions=-1>\n"
            data += "Patreon: <https://www.patreon.com/ETLegacy>\n\n"
            await self.bot.say(data)
			
    #@commands.command()
    #async def shard(self):
        #"""Your server shard."""

        #em=discord.Embed(colour=0x0082c0, timestamp=__import__('datetime').datetime.utcnow())
        #em.add_field(name="Shard:", value="This is shard {} out of {} shards.".format(self.bot.shard_id + 1, self.bot.shard_count))
        #em.set_author(name="Trinity", icon_url="http://i.imgur.com/4JCHIRS.png")
        #await self.bot.say(embed=em) 
		
    @commands.command(pass_context=True, no_pm=False, hidden=True)
    @checks.is_owner()
    async def sendcog(self, ctx, filepath: str):
        fp = "cogs/{0}.py".format(filepath)
        if os.path.exists(fp):
            await self.bot.send_file(ctx.message.channel, fp)
        else:
            await self.bot.say("Module not found!")
			
    @commands.command(pass_context=True)
    async def prefix(self, ctx):
       """Shows the bot's prefixs"""
       prefix = ctx.prefix
       author = ctx.message.author
       server = ctx.message.server
       user = author
	   
       lel = discord.Embed(description="{} Prefix on **{}** is `{}`".format(user.mention, server.name, prefix), colour=discord.Colour.blue())
       await self.bot.say(embed=lel)
	   
    @commands.command(pass_context=True)
    @checks.is_owner()
    async def changelog(self, ctx):
       """Shows the bot's changelog"""
       author = ctx.message.author
       server = ctx.message.server
	   
       await self.bot.delete_message(ctx.message)
       msg = "<@&317100780760858624>"
       o=discord.Embed(description="<:stafftools:335722528582402048>Changelog for Trinity! **__[/09/2017]__**", colour=discord.Colour.blue())
       o.add_field(name="CHANGED", value="• Changed `*modlogset` now you can make embed!\n• Changed the warning commands.")
       o.add_field(name="ADDED", value="• Added `*autorole fixroles` it gives the role to every user that didn't get the role.")
       o.add_field(name="FIXED", value="• Fixed `*antiadv` it used to block every link, but now should block only discord. You can block other links if you add them.")
       o.add_field(name="DISABLED", value="• Nothing to disable.", inline=False)
       o.add_field(name="Coming Soon", value="• AFK: It will add `[AFK]` right next of your name.")
       o.set_author(name="Trinity™#1306", icon_url="https://i.imgur.com/7E0vIcO.png")
       o.set_thumbnail(url="https://i.imgur.com/7E0vIcO.png")
       await self.bot.say(msg, embed=o)
 
		
def setup(bot):
    n = Info(bot)
    bot.add_cog(n)
