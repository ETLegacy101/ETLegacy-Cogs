import os
import discord
import glob
import re
import os
import aiohttp
import asyncio
import random
import requests
import json
import datetime

from discord.ext import commands
from .utils import checks
from __main__ import settings
from cogs.utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box
from time import perf_counter
from random import choice
from subprocess import check_output

try:
    import ffmpy
    ffmpyinstalled = True
except:
    print("You don't have ffmpy installed, installing it now...")
    try:
        check_output("pip3 install ffmpy", shell=True)
        print("FFMpy installed succesfully!")
        import ffmpy
        ffmpyinstalled = True
    except:
        print("FFMpy didn't install succesfully.")
        ffmpyinstalled = False
try:
    from pyshorteners import Shortener
    pyshortenersinstalled = True
except:
    print("You don't have pyshorteners installed, installing it now...")
    try:
        check_output("pip3 install pyshorteners", shell=True)
        print("Pyshorteners installed succesfully!")
        import pyshorteners
        pyshortenersinstalled = True
    except:
        print("Pyshorteners didn't install succesfully.")
        pyshortenersinstalled = False

class Useful:
    """Useful stuffz!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/useful/settings.json")

    @commands.command()
    async def mstats(self):
        """Shows you in how many servers the bot is."""
        stats = await self.bot.say("Getting stats, this may take a while.")
        edit_message = self.bot.edit_message
        uniquemembers = []
        servercount = len(self.bot.servers)
        channelcount = len(list(self.bot.get_all_channels()))
        membercount = len(list(self.bot.get_all_members()))
        for member in list(self.bot.get_all_members()):
            if member.name not in uniquemembers:
                uniquemembers.append(member.name)
        uniquemembercount = len(uniquemembers)
        statsmsg = "I am currently in **{}** servers with **{}** channels, **{}** members of which **{}** unique.".format(servercount, channelcount, membercount, uniquemembercount)
        await self.bot.edit_message(stats, statsmsg)
        # start of servercount milestones
        await asyncio.sleep(0.3)
        if servercount >= 10:
            statsmsg = statsmsg + "\n\n:white_check_mark: Reach 10 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10 servers."
        if servercount >= 50:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50 servers."
        if servercount >= 100:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 100 servers."
        if servercount >= 500:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 500 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 500 servers."
        if servercount >= 1000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 1000 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 servers."
        await self.bot.edit_message(stats, statsmsg)
        # start of channelcount milestones
        await asyncio.sleep(0.3)
        if channelcount >= 10:
            statsmsg = statsmsg + "\n\n:white_check_mark: Reach 10 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10 channels."
        if channelcount >= 50:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50 channels."
        if channelcount >= 100:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 100 channels."
        if channelcount >= 500:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 500 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 500 channels."
        if channelcount >= 1000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 1000 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 channels."
        await self.bot.edit_message(stats, statsmsg)
        # start of membercount milestones
        await asyncio.sleep(0.3)
        if membercount >= 1000:
            statsmsg = statsmsg + "\n\n:white_check_mark: Reach 1000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 members."
        if membercount >= 5000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 5000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 5000 members."
        if membercount >= 10000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 10000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10000 members."
        if membercount >= 50000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50000 members."
        if membercount >= 100000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 100000 members.\n"
        await self.bot.edit_message(stats, statsmsg)
        # start of uniquemembercount milestones
        await asyncio.sleep(0.3)
        if uniquemembercount >= 1000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 1000 unique members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 unique members."
        if uniquemembercount >= 5000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 5000 unique members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 5000 unique members."
        if uniquemembercount >= 10000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 10000 unique members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10000 unique members."
        if uniquemembercount >= 50000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50000 unique members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50000 unique members."
        if uniquemembercount >= 100000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100000 unique members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 100000 unique members."
        await self.bot.edit_message(stats, statsmsg)
            
    @commands.command(pass_context=True)
    @checks.is_owner()
    async def announce(self, ctx, *, msg):
        """Sends a message in every server."""
        statusMsg = "Sending message to all servers {}..."
        sent = 0
        status = str(sent) + "/" + str(len(self.bot.servers))
        sending = await self.bot.say(statusMsg.format(status))
        servers = []
        for server in self.bot.servers:
            servers.append(server)
        for server in servers:
            if not "bots" in server.name.lower():
                try:
                    await self.bot.send_message(server.default_channel, "{} ~ {}.".format(msg, str(ctx.message.author)))
                except:
                    pass
                sent += 1
                status = str(sent) + "/" + str(len(self.bot.servers))
                if sent % 5 == 0:
                    await self.bot.edit_message(sending, statusMsg.format(status))
        await self.bot.edit_message(sending, "Done!")

    @commands.command(name="autopost")
    @checks.mod_or_permissions()
    async def _autopost(self, times:int, interval:float, *, msg):
        """Posts a message every set amount of minutes.
        The interval is in minutes."""
        time = 0
        while time < times:
            await self.bot.say(msg)
            time = time + 1
            await asyncio.sleep(interval * 60)
        
    @commands.command()
    @checks.is_owner()
    async def setclientid(self, id:str):
        """Sets the client id of this bot."""
        self.settings['client_id'] = id
        self.save_settings()
        await self.bot.say("Client id set, now set the authorization header with [p]setauth.")
        
    @commands.command()
    @checks.is_owner()
    async def setauth(self, auth):
        """Sets the authorization header key for bots.discord.pw to update the amount of servers your bot is in, yw."""
        if self.settings['client_id'] == "client_id_here":
            await self.bot.say("You first have to set the client id with [p]setclientid <id>.")
        data = {'server_count': int(len(self.bot.servers))}
        try:
            post = requests.post("https://bots.discord.pw/api/bots/" + self.settings['client_id'] + "/stats", headers={'Authorization': auth, 'Content-Type' : 'application/json'}, data=json.dumps(data))
            print(post.content.decode("utf-8"))
        except Exception as e:
            await self.bot.say("Auth key is not working or an error occured.\n")
            await self.bot.say(e)
            return
        self.settings['auth_key'] = auth
        self.save_settings()
        await self.bot.say("Auth key set and servercount updated.")
        
    @commands.command()
    @checks.is_owner()
    async def setdlauth(self, auth):
        """Sets the authorization header key for bots.discordlist.net to update the amount of servers your bot is in, yw."""
        data = {"token": auth, "servers": len(self.bot.servers)}
        try:
            post = requests.post("https://bots.discordlist.net/api.php", data=json.dumps(data))
            print(post.content.decode("utf-8"))
        except Exception as e:
            await self.bot.say("Auth key is not working or an error occured.\n")
            await self.bot.say(e)
            return
        self.settings['auth_key_dl'] = auth
        self.save_settings()
        await self.bot.say("Auth key set and servercount updated.")
        
    @commands.command()
    async def servercount(self):
        """Counts all the servers the bot is currently in."""
        await self.bot.say("I am currently in **{} servers** with **{} members**.".format(len(self.bot.servers), len(list(self.bot.get_all_members()))))
        
    def save_settings(self):
        return dataIO.save_json("data/useful/settings.json", self.settings)
        
    async def on_server_join(self, server):
        if not self.settings['auth_key'] == "key_here":
            data = {'server_count': int(len(self.bot.servers))}
            post = requests.post("https://bots.discord.pw/api/bots/" + self.settings['client_id'] + "/stats", headers={'Authorization': self.settings['auth_key'], 'Content-Type' : 'application/json'}, data=json.dumps(data))
            print("Joined a server, updated stats on bots.discord.pw. " + post.content.decode("utf-8"))
        if not self.settings['auth_key_dl'] == "dl_key_here":
            data = {"token": self.settings['auth_key_dl'], "servers": len(bot.servers)}
            post = requests.post("https://bots.discordlist.net/api.php", data=json.dumps(data))
            print("Left a server, updated stats on bots.discordlist.net. " + post.content.decode("utf-8"))
        
    async def on_server_remove(self, server):
        if not self.settings['auth_key'] == "key_here":
            data = {'server_count': int(len(self.bot.servers))}
            post = requests.post("https://bots.discord.pw/api/bots/" + self.settings['client_id'] + "/stats", headers={'Authorization': self.settings['auth_key'], 'Content-Type' : 'application/json'}, data=json.dumps(data))
            print("Left a server, updated stats on bots.discord.pw. " + post.content.decode("utf-8"))
        if not self.settings['auth_key_dl'] == "dl_key_here":
            data = {"token": self.settings['auth_key_dl'], "servers": len(bot.servers)}
            post = await requests.post("https://bots.discordlist.net/api.php", data=json.dumps(data))
            print("Left a server, updated stats on bots.discordlist.net. " + post.content.decode("utf-8"))
        
def check_folders():
    if not os.path.exists("data/useful"):
        print("Creating data/useful folder...")
        os.makedirs("data/useful")
        
def check_files():
    if not os.path.exists("data/useful/settings.json"):
        print("Creating data/useful/settings.json file...")
        dataIO.save_json("data/useful/settings.json", {'auth_key': 'key_here', 'client_id': 'client_id_here', 'geocodingkey': 'key_here', 'timezonekey': 'key_here'})
        
class ModuleNotFound(Exception):
    pass
        
def setup(bot):
    if not ffmpyinstalled:
        raise ModuleNotFound("FFmpy is not installed, install it with pip3 install ffmpy.")
    if not pyshortenersinstalled:
        raise ModuleNotFound("Pyshorteners is not installed, install it with pip3 install pyshorteners.")
    check_folders()
    check_files()
    bot.add_cog(Useful(bot))
