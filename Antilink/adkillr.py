import discord
from discord.ext import commands
from .utils import checks
from __main__ import send_cmd_help, settings
from cogs.utils.dataIO import dataIO
import os
import logging

class Adkillr:
    """Adkillr"""

    def __init__(self, bot):
        self.bot = bot
        self.adkillr = dataIO.load_json("data/adkillr/adkillr.json")
        self.counter = 0
        
    async def antiadv(self, message):
        """Kill them ads!"""
        if message.server is not None:
            self.counter += 1
            if self.counter % 10 == 0:
                self.adkillr = dataIO.load_json("data/adkillr/adkillr.json")
            try:
                temp = message.author.roles
            except AttributeError:
                return
            serverid = message.server.id
            ad = message
            if ad.server is None:
                pass
            try:
                temp = self.adkillr[serverid]['toggle']
            except:
                self.adkillr[serverid] = {'toggle': True, 'message': "{0.mention} don't send links!"}
                dataIO.save_json("data/adkillr/adkillr.json", self.adkillr)
            if ad.author.id == settings.owner:
                return
            elif ad.author.permissions_in(ad.channel).manage_messages:
                return
            if self.adkillr[serverid]['toggle']:
                if not message.author.id == self.bot.user.id:
                    try:
                        if ("discord.gg" in ad.content.lower()) or ("discord.com" in ad.content.lower()) and ("." in ad.content.lower()):
                            for filter in self.adkillr[ad.server.id]['filters']:
                                if filter in ad.content:
                                    pass
                                else:
                                    if message.server.me.permissions_in(ad.channel).manage_messages:
                                        try:
                                            await self.bot.delete_message(ad)
                                            await self.bot.send_message(ad.channel, self.adkillr[ad.server.id]['message'].format(ad.author))
                                        except:
                                            pass
                    except KeyError:
                        if message.server.me.permissions_in(ad.channel).manage_messages:
                            await self.bot.delete_message(ad)
                            await self.bot.send_message(ad.channel, self.adkillr[ad.server.id]['message'].format(ad.author))


    @commands.group(name="antiadv", pass_context=True, no_pm=True)
    async def _antiadv(self, ctx):
        """Manages the settings for antiadv."""
        serverid = ctx.message.server.id
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
        if serverid not in self.adkillr:
            self.adkillr[serverid] = {'toggle': False, 'message': '{0.mention} don\'t send links!', 'filters': []}
            dataIO.save_json("data/adkillr/adkillr.json", self.adkillr)

    @_antiadv.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def toggle(self, ctx):
        """Enable/disables antiadv in the server."""
        serverid = ctx.message.server.id
        if self.adkillr[serverid]['toggle'] is True:
            self.adkillr[serverid]['toggle'] = False
            e = discord.Embed(description='**AntiAdv is now disabled.**')
            await self.bot.say(embed=e)
        elif self.adkillr[serverid]['toggle'] is False:
            self.adkillr[serverid]['toggle'] = True
            e = discord.Embed(description='**AntiAdv is now enabled.**')
            await self.bot.say(embed=e)
        dataIO.save_json("data/adkillr/adkillr.json", self.adkillr)
        
    @_antiadv.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def message(self, ctx, *, message:str):
        """Set the custom message for when a link gets deleted
        {0} will turn into the authors name, you can use {0.name}, {0.mention} or {0.id}.
        Default is {0.mention} don't send links!"""
        serverid = ctx.message.server.id
        self.adkillr[serverid]['message'] = message
        dataIO.save_json("data/adkillr/adkillr.json", self.adkillr)
        await self.bot.say("Message set!")
    
    @_antiadv.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def add(self, ctx, *, link):
        """Add a link or word that shouldn't get deleted, 
        example: https://www.youtube.com, youtube.com, youtube.
        
        If you put 'discord' anything with the word discord in it won't be deleted."""
        try: # compatability with older versions
            self.adkillr[ctx.message.server.id]['filters'].append(link)
        except KeyError:
            self.adkillr[ctx.message.server.id]['filters'] = [link]
        dataIO.save_json("data/adkillr/adkillr.json", self.adkillr)
        await self.bot.say("Filter added.")
        
    @_antiadv.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions()
    async def remove(self, ctx, *, link):
        """Remove a word or link that shouldn't get deleted."""
        try:
            if link not in self.adkillr[ctx.message.server.id]['filters']:
                await self.bot.say("That link is not in the current filters.")
            else:
                self.adkillr[ctx.message.server.id]['filters'].remove(link)
                await self.bot.say("Filter removed.")
        except KeyError:
            await self.bot.say("There are no filters set.")
            
    @_antiadv.command(pass_context=True, no_pm=True)
    async def list(self, ctx):
        """Lists the filters that the bot doesn't delete."""
        try:
            if ctx.message.server.id not in self.adkillr:
                await self.bot.say("There are no filters set for this server.")
            else:
                await self.bot.say("The current filters are\n{}.".format(", ".join(self.adkillr[ctx.message.server.id]['filters'])))
        except KeyError:
            await self.bot.say("There are no filters set for this server.")
        
def check_folders():
    if not os.path.exists("data/adkillr"):
        print("Creating data/adkillr folder...")
        os.makedirs("data/adkillr")
        
def check_files():
    if not os.path.exists("data/adkillr/adkillr.json"):
        print("Creating data/adkillr/adkillr.json file...")
        dataIO.save_json("data/adkillr/adkillr.json", {})
        
def setup(bot):
    check_folders()
    check_files()
    n = Adkillr(bot)
    bot.add_listener(n.antiadv, "on_message")
    bot.add_cog(Adkillr(bot))
