import discord

class Joinmsg:
    """docstring for join message."""
    def __init__(self, bot):
        self.bot = bot

    async def on_server_join(self, server):
        embed=discord.Embed(title="Click here for my support server!", url='https://discord.gg/dVEkSh4 ', description="**Hey there**\n I'm ETLegacy and i got asked to join by an Admin!\n My current prefixes is are * and if you want all the commands do `*commands`!\n Here some of the main features i got!\n **Music**: I can play music if you did `*play` and the song you want, i will connect to your vc.\n **Afk**: Tell the bot when you are AFK, if someone mentions you the bot tells them the person if afk with custom message command for it is `*afk` or `*away`\n **Modlog**: This will logs all kicks and bans\n if you typed `*modset modlog #channelname`\n when you do that i will log all kicks and bans!\n **Mute**: You can mute users for specific of time, it will Re-mute the user if he tries to bypass by leaving and joining again.\n If the bot was given the right permission, all you do is type `*mute @someone 10m test`\n The bot will setup a mute role with the right permissions for mute.\n If you need more commands do `*commands`.\n Have a great day" , color=0x38a33e)
        embed.set_author(name="Thank you for another server!", url='https://discordapp.com/oauth2/authorize?client_id=248032345603571712&scope=bot&permissions=-1', icon_url='https://cdn.discordapp.com/avatars/248032345603571712/7a2203dfab9e800e4f39b34b109b987c.webp?size=1024')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/248032345603571712/7a2203dfab9e800e4f39b34b109b987c.webp?size=1024')
        embed.set_footer(text="Now on {} servers with {} users!".format(len(self.bot.servers), len([e.name for e in self.bot.get_all_members()])))
        await self.bot.send_message(server, embed=embed)

def setup(bot):
    n = Joinmsg(bot)
    bot.add_cog(n)