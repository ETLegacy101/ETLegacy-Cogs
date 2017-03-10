
import discord
from discord.ext import commands

a=discord.Embed(title="About ETLegacy", description="""ETLegacy - A fun multipurpose bot for Discord with an interactive Cleverbot, Music, Moderation and many other Utility features.\nFor Help: [ETLegacy Help]( https://discord.io/legacy)\nOAuth Link: [ETLegacy OAuth](https://discordapp.com/oauth2/authorize?client_id=248032345603571712&scope=bot&permissions=-1)""", colour=discord.Colour.blue())
a.set_thumbnail(url="http://i.imgur.com/m4CZ101.png")

au=discord.Embed(title="Audio Commands:", description="""
  **np  :**           Info about the current song.
  **pause  :**        Pauses the current song, `[p]resume` to continue.
  **play  :**         Plays a link / searches and play.
  **queue  :**        Shows the current queue.
  **resume  :**       Resumes a paused song or playlist.
  **shuffle :**       shuffles the current queue.
  **skip  :**         Skips a song, using the set threshold if the requester isn't.
  **stop  :**         Stops a currently playing song or playlist. 
  **volume  :**       Sets the volume (0 - 100).
  **disconnect  :**   Disconnects ETLegacy from the voice channel.""", colour=discord.Colour.red())
au.set_thumbnail(url="https://yt3.ggpht.com/0v8T0CTAv8VPxA5lJtz-tqJe-tR-3VQc0ONhD6Az2RWjNRnwh5QQzPYz5I7wbYljU_tQjZ2ok2W59_v_=s900-nd-c-c0xffffffff-rj-k-no")

mod=discord.Embed(title="Moderation Commands:", description="""
  **addrole  :**      Adds a role to a user, defaults to author
  **ban  :**          Bans a user from the server.
  **botclean  :**     Removes all bot messages.
  **createrole  :**   Creates a role.
  **deleterole  :**   Deletes an existing role.
  **editrole  :**     Edits roles settings.
  **hackban  :**      Bans user by id, user doesn't have to be in server.
  **unban  :**        Unbans a user from the server. Uses user id.
  **kick  :**         Kicks user.
  **massmove  :**     Massmove users to another voice channel.
  **mute  :**         mutes a user serverwide.
  **removerole  :**   Removes a role from user.
  **softban  :**      Kicks user, deleting 1 day of messages.
  **autorole  :**     Change settings for autorole.
  **antilink  :**     Antilink settings for your server.
  **modlogset  :**    Change modlog settings.
  **modlogtoggle  :** toggle which server activity to log.
  **blacklist  :**    bans a user from using the bot.
  **whitelist  :**    Users who will be able to use the bot.
  **welcomeset  :**   Welcome and leave message, with invite link.""", colour=discord.Colour.green())
mod.set_thumbnail(url="https://images-ext-2.discordapp.net/.eJwNwcEOwiAMANB_4V5oJ5ixm4l3P4E0sUOSSRpkclj27_reYfa2mcW8etfFuTGG1X37SoPeuNRSs32Ku6mmO3dOD5XqypuzfJz3M2LgCShcEPwcCSIxwSohMCNSvK5pCpgI_6zWbM4fD7EiMg.E9FwPjfhw-pCKaEMXTvoZ2-ZY-M?width=80&height=80")

info=discord.Embed(title="Infomation Commands: ", description="""
  **names  :**        Show previous names/nicknames of a user
  **admins  :**       Shows mods in the server.
  **inrole  :**       Check members in the role specified.
  **ping  :**         Shows the ping time. 
  **roleinfo  :**     Gives you information about a role.
  **sinfo  :**        Shows servers informations.
  **stats  :**        Shows stats.
  **uinfo  :**        Shows users informations.
  **stats  :**        Retreive statistics.
  **afk  :**          Tell the bot you're away or back.
  **google  :**       Its google, you search with it.
  **permissions  :**  Permissions manager.
  **news  :**         Enables or disables announcement subscription.
  **uptime  :**       Shows how long the bot has been online.""", colour=discord.Colour.blue())
info.set_thumbnail(url="https://images-ext-1.discordapp.net/eyJ1cmwiOiJodHRwczovL3VwbG9hZC53aWtpbWVkaWEub3JnL3dpa2lwZWRpYS9lbi81LzU0L0luZm9ybWF0aW9uLnBuZyJ9.xi-2ZzV_czvJDaudMrqeqOgNZ8E?width=80&height=80")

fun=discord.Embed(title="Fun Commands:", description="""
  **bank  :**         Bank operations
  **economyset  :**   Changes economy module settings
  **leaderboard  :**  Server / global leaderboard
  **payday  :**       Get some free credits
  **payouts  :**      Shows slot machine payouts
  **slot  :**         Play the slot machine.
  **buyrole  :**      You buy a role from a server 
  **buyroleset  :**   Manage buyrole.
  **weather  :**      Gets the weather.
  **membercount  :**  Gets the how many members in the server.
  **uid  :**          Gets your id.
  **sid  :**          Gets your server id.
  **reaction  :**     fucker, lmao, rekt, sotru, noscope, litaf.
  **reminder  :**     forgetme: Removes all your upcoming notifications\n remindme: Sends you <text> when the time is up.
  **seen  :**         seen <@username>.
  **trivia  :**       Start a trivia session with the specified list.
  **triviaset  :**    Change trivia settings.
  **penis  :**        Detects user's penis length.
  **shop  :**         Shop Commands.""", colour=discord.Colour.yellow())
fun.set_thumbnail(url="http://www.niagarafallsfunzone.com/images/layout/tickets.png")

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def audio(self, ctx):
        """Sends Audio help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=au)
                
    @commands.command(pass_context=True)
    async def mod(self, ctx):
        """Sends Mod help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=mod)
                
    @commands.command(pass_context=True)
    async def information(self, ctx):
        """Sends Info help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=info)
		
	@commands.command(pass_context=True)
    async def fun(self, ctx):
        """Sends fun help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=fun)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        """Channel help message."""
        try:
            e=discord.Embed(title="ETLegacy Help", 
			description=
			"Here is a little bit of help with ETLegacy!\n\n"
			"**1)** To get all of ETLegacy's commands you may type `*commands`.\n"
			"**2)** For changelog and more type `*info`.\n"
			"**3)** You may type the module as a command and all the commands in that module will be pasted out in a message. Example: `*mod`\n"
			"**4)** And for any comments or concerns please use the `*contact` commands.\n\n"
			"For Support or updates with ETLegacy bot please join our discord.\n"
			"[ETLegacy Discord](https://discord.io/legacy)\n"
			"[Invite ETLegacy](https://discordapp.com/oauth2/authorize?client_id=248032345603571712&scope=bot&permissions=-1)\n\n"
			"Thank you for reading this and have a great day!", 
			colour=discord.Colour.blue())
            e.set_thumbnail(url="https://images-ext-1.discordapp.net/.eJwFwQsOwiAMANC7cABa2k5gifEs5bO4RB0B1ETj3X3va579ZlZznbONFSCXhy37yEcv2prNxx30pVP7AJKATCzLCXnxzjsCr0TIZdMUa0CssnFMLMlhTDH4bN81tcvYP_XskMT8_qcxIYk._YrCsmQnelUli8Exk3yukS5BDcc?width=80&height=80")
            await self.bot.say(embed=e)
        except:
            msg = "__**ETlegacy Help**__\n\n"
            msg += "**1)** To get all of ETLegacy's commands you may type `*commands`.\n"
            msg += "**2)** For changelog and more type `*info`.\n"
            msg += "**3)** You may type the module as a command. Example: `*mod`\n"
            msg += "**4)** And for any comments or concerns please use the *contact commands.\n\n"
            msg += "__**Thank you for reading this and have a great day!**__\n\n"
            msg += "`Disclaimer:` This is the old embed, you're only seeing this because I do not have embed perms. If you want to see the new help message please give me embed perms."
            await self.bot.say(msg)
            
    @commands.command(pass_context=True, no_pm=True)
    async def help2(self, ctx):
        await self.bot.say(":warning: | Some menu items may not work for certain users due to permission requirements.")
        author = ctx.message.author
        menu = self.bot.get_cog("Menu")
        cmds = ["Roles", "Send modules", "List modules", "Permissions", "Invite", "Disclaimer", "Cancel"]

        result = await menu.number_menu(ctx, "Utilities menu", cmds, autodelete=True)
        cmd = cmds[result-1]

        if cmd == "Roles":
            await ctx.invoke(self.roles)
                
        if cmd == "Send modules":
            await ctx.invoke(self.sendmod)
        
        if cmd == "List modules":
            await ctx.invoke(self.listmods)
            
        if cmd == "Permissions":
            await ctx.invoke(self.permissions)
            
        if cmd == "Invite":
            await ctx.invoke(self.invite)
                
        if cmd == "Disclaimer":
            await ctx.invoke(self.disclaimer)    
                
        if cmd == "Cancel":
            return await self.bot.say("Menu cancelled.")

        if cmd is None:
            return await self.bot.say("Menu has expired.")

    @commands.command(pass_context=True)
    async def commands(self, ctx):
        """Shows all commands."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = author
        await self.bot.send_message(destination, embed=a)
        await self.bot.send_message(destination, embed=au)
        await self.bot.send_message(destination, embed=mod)
        await self.bot.send_message(destination, embed=info)

    async def on_message(self, message):
        if message.content == "*commands":
            await self.bot.send_message(message.channel, message.author.mention+", I have pm'd you my commands!")        

def setup(bot):
    n = Help(bot)
    bot.remove_command('help')
    bot.add_cog(n)