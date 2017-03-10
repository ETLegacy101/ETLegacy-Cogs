import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import set_cog
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box
import random
from random import randint
from random import choice as randchoice
from .utils.chat_formatting import *

import importlib
import traceback
import logging
import asyncio
from copy import deepcopy
import threading
import datetime
import time
import glob
import os
import aiohttp

log = logging.getLogger("red.owner")
colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
colour = int(colour, 16)

class CogNotFoundError(Exception):
    pass


class CogLoadError(Exception):
    pass


class NoSetupError(CogLoadError):
    pass


class CogUnloadError(Exception):
    pass


class OwnerUnloadWithoutReloadError(CogUnloadError):
    pass


class Owner:
    """All owner-only commands that relate to debug bot operations.
    """

    def __init__(self, bot):
        self.bot = bot
        self.setowner_lock = False
        self._settings = dataIO.load_json('data/admin/settings.json')
        self._settable_roles = self._settings.get("ROLES", {})
        self.file_path = "data/red/disabled_commands.json"
        self.disabled_commands = dataIO.load_json(self.file_path)
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    async def _confirm_invite(self, server, owner, ctx):
        answers = ("yes", "y")
        invite = await self.bot.create_invite(server)
        if ctx.message.channel.is_private:
            await self.bot.say(invite)
        else:
            await self.bot.say("Are you sure you want to post an invite to {} "
                               "here? (yes/no)".format(server.name))
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg is None:
                await self.bot.say("I guess not.")
            elif msg.content.lower().strip() in answers:
                await self.bot.say(invite)
            else:
                await self.bot.say("Alright then.")

    def _is_server_locked(self):
        return self._settings.get("SERVER_LOCK", False)


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def serverlock(self, ctx):
        """Toggles locking the current server list, will not join others"""
        if self._is_server_locked():
            self._set_serverlock(False)
            await self.bot.say("Server list unlocked")
        else:
            self._set_serverlock()
            await self.bot.say("Server list locked.")

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def partycrash(self, ctx, idnum=None):
        """Lists servers and generates invites for them"""
        owner = ctx.message.author
        if idnum:
            server = discord.utils.get(self.bot.servers, id=idnum)
            if server:
                await self._confirm_invite(server, owner, ctx)
            else:
                await self.bot.say("I'm not in that server")
        else:
            msg = ""
            servers = sorted(self.bot.servers, key=lambda s: s.name)
            for i, server in enumerate(servers, 1):
                msg += "{}: {}\n".format(i, server.name)
            msg += "\nTo post an invite for a server just type its number."
            for page in pagify(msg, delims=["\n"]):
                await self.bot.say(box(page))
                await asyncio.sleep(1.5)  # Just in case for rate limits
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg is not None:
                try:
                    msg = int(msg.content.strip())
                    server = servers[msg - 1]
                except ValueError:
                    await self.bot.say("You must enter a number.")
                except IndexError:
                    await self.bot.say("Index out of range.")
                else:
                    try:
                        await self._confirm_invite(server, owner, ctx)
                    except discord.Forbidden:
                        await self.bot.say("I'm not allowed to make an invite"
                                           " for {}".format(server.name))
            else:
                await self.bot.say("Response timed out.")

    @commands.group(invoke_without_command=True, aliases=["l"])
    @checks.is_owner()
    async def load(self, *, module: str):
        """Loads a module

        Example: load mod"""
        colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        module = module.strip()
        if "cogs." not in module:
            module = "cogs." + module
        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say(":bangbang: **That module could not be found.** :x:")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say(embed=discord.Embed(description="There was an issue loading the module.```py\n{}```".format(e), colour=discord.Colour(value=colour)))
        except Exception as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say(embed=discord.Embed(description='Module was found and possibly loaded but '
                               'something went wrong.```py\n{}```'.format(e), colour=discord.Colour(value=colour)))
        else:
            set_cog(module, True)
            await self.disable_commands()
            em = discord.Embed(description="Module Loaded.", colour=discord.Colour(value=colour))    
            await self.bot.say(embed=em)

    @commands.group(invoke_without_command=True, aliases=["ul"])
    @checks.is_owner()
    async def unload(self, *, module: str):
        """Unloads a module

        Example: unload mod"""
        module = module.strip()
        if "cogs." not in module:
            module = "cogs." + module
        if not self._does_cogfile_exist(module):
            await self.bot.say("That module file doesn't exist. I will not"
                               " turn off autoloading at start just in case"
                               " this isn't supposed to happen.")
        else:
            set_cog(module, False)
        try:  # No matter what we should try to unload it
            self._unload_cog(module)
        except OwnerUnloadWithoutReloadError:
            await self.bot.say("I cannot allow you to unload the Owner plugin"
                               " unless you are in the process of reloading.")
        except CogUnloadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say('Unable to safely disable that module.')
        else:
            await self.bot.say("Module Unloaded.")

    @unload.command(name="all", aliases=["ula"])
    @checks.is_owner()
    async def unload_all(self):
        """Unloads all modules"""
        cogs = self._list_cogs()
        still_loaded = []
        for cog in cogs:
            set_cog(cog, False)
            try:
                self._unload_cog(cog)
            except OwnerUnloadWithoutReloadError:
                pass
            except CogUnloadError as e:
                log.exception(e)
                traceback.print_exc()
                still_loaded.append(cog)
        if still_loaded:
            still_loaded = ", ".join(still_loaded)
            await self.bot.say("I was unable to unload some cogs: "
                "{}".format(still_loaded))
        else:
            await self.bot.say(":ballot_box_with_check: ***All cogs are now unloaded.*** :ballot_box_with_check:")

    @load.command(name="all")
    @checks.is_owner()
    async def load_all(self):
        """loads all modules"""
        cogs = self._list_cogs()
        still_unloaded = []
        for cog in cogs:
            set_cog(cog, True)
            try:
                self._load_cog(cog)
            except OwnerUnloadWithoutReloadError:
                pass
            except CogUnloadError as e:
                log.exception(e)
                traceback.print_exc()
                still_loaded.append(cog)
        if still_unloaded:
            still_unloaded = ", ".join(still_unloaded)
            await self.bot.say(":bangbang: **I was unable to load some cogs:**\n"
                "***{}***".format(still_unloaded))
        else:
            await self.bot.say(":ballot_box_with_check: ***All cogs are now loaded.*** :ballot_box_with_check:")


    @checks.is_owner()
    @commands.command(name="reload", hidden=True, pass_context=True, aliases=["r"])
    async def _reload(self, ctx, module):
        """Reloads a module

        Example: reload audio"""
        if "cogs." not in module:
            module = "cogs." + module

        try:
            self._unload_cog(module, reloading=True)
        except:
            pass

        try:
            self._load_cog(module)
        except CogNotFoundError:
            em = discord.Embed(description="That module cannot be found.", colour=discord.Colour(value=colour))
            await self.bot.say(embed=em)
        except NoSetupError:
            em = discord.Embed(description="That module does not have a setup function.", colour=discord.Colour(value=colour))
            await self.bot.say(embed=em)
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            em = discord.Embed(title="**Error:**", description="```py\n{}```".format(e), colour=discord.Colour.red())
            await self.bot.say(ctx.message.author.mention+", Something went wrong!")
            await self.bot.say(embed=em)
        else:
            set_cog(module, True)
            await self.disable_commands()
            em = discord.Embed(description="Module Reloaded.", colour=discord.Colour(value=colour))
            await self.bot.say(embed=em)

    @commands.command(name="cogs")
    @checks.is_owner()
    async def _show_cogs(self):
        """Shows loaded/unloaded cogs"""
        # This function assumes that all cogs are in the cogs folder,
        # which is currently true.

        # Extracting filename from __module__ Example: cogs.owner
        loaded = [c.__module__.split(".")[1] for c in self.bot.cogs.values()]
        # What's in the folder but not loaded is unloaded
        unloaded = [c.split(".")[1] for c in self._list_cogs()
                    if c.split(".")[1] not in loaded]

        if not unloaded:
            unloaded = ["None"]

        msg = ("+ Loaded\n"
               "{}\n\n"
               "- Unloaded\n"
               "{}"
               "".format(", ".join(sorted(loaded)),
                         ", ".join(sorted(unloaded)))
               )
        for page in pagify(msg, [" "], shorten_by=16):
            await self.bot.say(box(page.lstrip(" "), lang="diff"))

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def debug(self, ctx, *, code):
        """Evaluates code"""
        def check(m):
            if m.content.strip().lower() == "more":
                return True

        author = ctx.message.author
        channel = ctx.message.channel

        code = code.strip('` ')
        result = None

        global_vars = globals().copy()
        global_vars['bot'] = self.bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.server

        try:
            result = eval(code, global_vars, locals())
        except Exception as e:
            await self.bot.say(box('{}: {}'.format(type(e).__name__, str(e)),
                                   lang="py"))
            return

        if asyncio.iscoroutine(result):
            result = await result

        result = str(result)

        if not ctx.message.channel.is_private:
            censor = (self.bot.settings.email, self.bot.settings.password)
            r = "[EXPUNGED]"
            for w in censor:
                if w != "":
                    result = result.replace(w, r)
                    result = result.replace(w.lower(), r)
                    result = result.replace(w.upper(), r)

        result = list(pagify(result, shorten_by=16))

        for i, page in enumerate(result):
            if i != 0 and i % 4 == 0:
                last = await self.bot.say("There are still {} messages. "
                                          "Type `more` to continue."
                                          "".format(len(result) - (i+1)))
                msg = await self.bot.wait_for_message(author=author,
                                                      channel=channel,
                                                      check=check,
                                                      timeout=10)
                if msg is None:
                    try:
                        await self.bot.delete_message(last)
                    except:
                        pass
                    finally:
                        break
            await self.bot.say(box(page, lang="py"))

    @commands.group(name="set", pass_context=True)
    async def _set(self, ctx):
        """Changes ETLegacy's Bot global settings."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            return

    @_set.command(pass_context=True)
    async def owner(self, ctx):
        """Sets owner"""
        if self.setowner_lock:
            await self.bot.say("A set owner command is already pending.")
            return

        if self.bot.settings.owner != "id_here":
            await self.bot.say(
            "The owner is already set. Remember that setting the owner "
            "to someone else other than who hosts the bot has security "
            "repercussions and is *NOT recommended*. Proceed at your own risk."
            )
            await asyncio.sleep(3)

        await self.bot.say("Confirm in the console that you're the owner.")
        self.setowner_lock = True
        t = threading.Thread(target=self._wait_for_answer,
                             args=(ctx.message.author,))
        t.start()

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def prefix(self, ctx, *prefixes):
        """Sets ETLegacy global prefixes

        Accepts multiple prefixes separated by a space. Enclose in double
        quotes if a prefix contains spaces.
        Example: set prefix ! $ ? "two words" """
        if prefixes == ():
            await self.bot.send_cmd_help(ctx)
            return

        self.bot.settings.prefixes = sorted(prefixes, reverse=True)
        log.debug("Setting global prefixes to:\n\t{}"
                  "".format(self.bot.settings.prefixes))

        p = "prefixes" if len(prefixes) > 1 else "prefix"
        await self.bot.say("**Global** `{}` ***set***".format(p))

    @_set.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def serverprefix(self, ctx, *prefixes):
        """Sets ETLegacy prefixes for this server

        Accepts multiple prefixes separated by a space. Enclose in double
        quotes if a prefix contains spaces.
        Example: set serverprefix ! $ ? "two words"

        Issuing this command with no parameters will reset the server
        prefixes and the global ones will be used instead."""
        server = ctx.message.server

        if prefixes == ():
            self.bot.settings.set_server_prefixes(server, [])
            current_p = ", ".join(self.bot.settings.prefixes)
            await self.bot.say("Server prefixes reset. Current prefixes: "
                               "`{}`".format(current_p))
            return

        prefixes = sorted(prefixes, reverse=True)
        self.bot.settings.set_server_prefixes(server, prefixes)
        log.debug("Setting server's {} prefixes to:\n\t{}"
                  "".format(server.id, self.bot.settings.prefixes))

        p = "Prefixes" if len(prefixes) > 1 else "**Prefix**"
        await self.bot.say("`{}` **set for this server.\n"
                           "To go back to the global prefixes, do**"
                           " `{}set serverprefix` "
                           "".format(p, prefixes[0]))

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def name(self, ctx, *, name):
        """Sets ETLegacy's Bot name"""
        name = name.strip()
        if name != "":
            try:
                await self.bot.edit_profile(self.bot.settings.password,
                                            username=name)
            except:
                await self.bot.say("Failed to change name. Remember that you"
                                   " can only do it up to 2 times an hour."
                                   "Use nicknames if you need frequent "
                                   "changes. {}set nickname"
                                   "".format(ctx.prefix))
            else:
                await self.bot.say("Name set to `{}`".format(name))
        else:
            await self.bot.send_cmd_help(ctx)

    @_set.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def nickname(self, ctx, *, nickname=""):
        """Sets ETLegacy's Bot nickname

        Leaving this empty will remove it."""
        nickname = nickname.strip()
        if nickname == "":
            nickname = None
        try:
            await self.bot.change_nickname(ctx.message.server.me, nickname)
            await self.bot.say(":thumbsup: Nickname changed to `{}`".format(nickname))
        except discord.Forbidden:
            await self.bot.say("I cannot do that, I lack the "
                "\"Change Nickname\" permission.")

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def game(self, ctx, *, game=None):
        """Sets ETLegacy's playing status

        Leaving this empty will clear it."""

        server = ctx.message.server

        current_status = server.me.status if server is not None else None

        if game:
            game = game.strip()
            await self.bot.change_presence(game=discord.Game(name=game),
                                           status=current_status)
            log.debug('Status set to "{}" by owner'.format(game))
        else:
            await self.bot.change_presence(game=None, status=current_status)
            log.debug('status cleared by owner')
        await self.bot.say(":thumbsup: Game changed to `{}`".format(game))

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def status(self, ctx, *, status=None):
        """Sets ETLegacy's Bot status

        Statuses:
            online
            idle
            dnd
            invisible"""

        statuses = {
                    "online"    : discord.Status.online,
                    "idle"      : discord.Status.idle,
                    "dnd"       : discord.Status.dnd,
                    "invisible" : discord.Status.invisible
                   }

        server = ctx.message.server

        current_game = server.me.game if server is not None else None

        if status is None:
            await self.bot.change_presence(status=discord.Status.online,
                                           game=current_game)
            await self.bot.say(":no_good: Status reset.")
        else:
            status = statuses.get(status.lower(), None)
            if status:
                await self.bot.change_presence(status=status,
                                               game=current_game)
                await self.bot.say(":thumbsup: Status changed to `{}`".format(status))
            else:
                await self.bot.send_cmd_help(ctx)

    @_set.command(pass_context=True)
    @checks.is_owner()
    async def stream(self, ctx, streamer=None, *, stream_title=None):
        """Sets ETLegacy's streaming status

        Leaving both streamer and stream_title empty will clear it."""

        server = ctx.message.server

        current_status = server.me.status if server is not None else None

        if stream_title:
            stream_title = stream_title.strip()
            if "twitch.tv/" not in streamer:
                streamer = "https://www.twitch.tv/" + streamer
            game = discord.Game(type=1, url=streamer, name=stream_title)
            await self.bot.change_presence(game=game, status=current_status)
            log.debug('Owner has set streaming status and url to "{}" and {}'.format(stream_title, streamer))
        elif streamer is not None:
            await self.bot.send_cmd_help(ctx)
            return
        else:
            await self.bot.change_presence(game=None, status=current_status)
            log.debug('stream cleared by owner')
        await self.bot.say("***Done.***")

    @_set.command()
    @checks.is_owner()
    async def avatar(self, url):
        """Sets ETLegacy's Bot avatar"""
        try:
            async with self.session.get(url) as r:
                data = await r.read()
            await self.bot.edit_profile(self.bot.settings.password, avatar=data)
            await self.bot.say("Am i sexy with my new avatar :D ?")
            log.debug("changed avatar")
        except Exception as e:
            await self.bot.say("Error, check your console or logs for "
                               "more information.")
            log.exception(e)
            traceback.print_exc()

    @_set.command(name="token")
    @checks.is_owner()
    async def _token(self, token):
        """Sets ETLegacy's Bot login token"""
        if len(token) < 50:
            await self.bot.say("Invalid token.")
        else:
            self.bot.settings.login_type = "token"
            self.bot.settings.email = token
            self.bot.settings.password = ""
            await self.bot.say("Token set. Restart me.")
            log.debug("Token changed.")

    @checks.is_owner()
    @commands.command(pass_context=True, no_pm=True)
    async def sendcog(self, ctx, filepath: str):
        fp = "cogs/{0}.py".format(filepath)
        if os.path.exists(fp):
            await self.bot.send_file(ctx.message.channel, fp)
        else:
            await self.bot.say(":x: **Cog** ***not found!***")

    @checks.is_owner()
    @commands.command(pass_context=True, no_pm=True)
    async def listcogs(self, ctx):
        """Shows the status of cogs.
        + means the cog is loaded
        - means the cog is unloaded
        ? means the cog couldn't be found(it was probably removed manually)"""

        all_cogs = dataIO.load_json("data/red/cogs.json")
        loaded, unloaded, other = ("",)*3
        cogs = self.bot.cogs['Owner']._list_cogs()

        for x in all_cogs:
            if all_cogs.get(x):
                if x in cogs:
                    loaded += "+\t{0}\n".format(x.split('.')[1])
                else:
                    other += "?\t{0}\n".format(x.split('.')[1])
            elif x in cogs:
                unloaded += "-\t{0}\n".format(x.split('.')[1])
        await self.bot.say("```diff\n{0}{1}{2}```".format(loaded, unloaded, other))

    @checks.is_owner()
    @commands.command(pass_context=True, no_pm=True)
    async def perms(self, ctx, user: discord.Member):
        perms = iter(ctx.message.channel.permissions_for(user))
        perms_we_have = "```diff\n"
        perms_we_dont = ""
        for x in perms:
            if "True" in str(x):
                perms_we_have += "+\t{0}\n".format(str(x).split('\'')[1])
            else:
                perms_we_dont += ("-\t{0}\n".format(str(x).split('\'')[1]))
        await self.bot.say("{0}{1}```".format(perms_we_have, perms_we_dont))

    @commands.command(aliases=["sd"])
    @checks.is_owner()
    async def shutdown(self):
        """Shuts down ETLegacy"""
        now = datetime.datetime.now()
        uptime = (now - self.bot.uptime).seconds
        uptime = datetime.timedelta(seconds=uptime)
        await self.bot.say("Successfully, Shut Down at `{}`".format(uptime))
        await self.bot.logout()

    @commands.group(name="command", pass_context=True)
    @checks.is_owner()
    async def command_disabler(self, ctx):
        """Disables/enables commands

        With no subcommands returns the disabled commands list"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            if self.disabled_commands:
                msg = "Disabled commands:\n```xl\n"
                for cmd in self.disabled_commands:
                    msg += "{}, ".format(cmd)
                msg = msg.strip(", ")
                await self.bot.whisper("{}```".format(msg))

    @command_disabler.command()
    async def disable(self, *, command):
        """Disables commands/subcommands"""
        comm_obj = await self.get_command(command)
        if comm_obj is KeyError:
            await self.bot.say("That command Is inexistent you fuck !")
        elif comm_obj is False:
            await self.bot.say("You cannot disable owner restricted commands.")
        else:
            comm_obj.enabled = False
            comm_obj.hidden = True
            self.disabled_commands.append(command)
            dataIO.save_json(self.file_path, self.disabled_commands)
            await self.bot.say("Command disabled :ok_hand: ")

    @command_disabler.command()
    async def enable(self, *, command):
        """Enables commands/subcommands"""
        if command in self.disabled_commands:
            self.disabled_commands.remove(command)
            dataIO.save_json(self.file_path, self.disabled_commands)
            await self.bot.say(":ok_hand: ***Command enabled!!*** :ok_hand:")
        else:
            await self.bot.say(" **That command is not disabled.** :face_palm:  ")
            return
        try:
            comm_obj = await self.get_command(command)
            comm_obj.enabled = True
            comm_obj.hidden = False
        except:  # In case it was in the disabled list but not currently loaded
            pass # No point in even checking what returns

    async def get_command(self, command):
        command = command.split()
        try:
            comm_obj = self.bot.commands[command[0]]
            if len(command) > 1:
                command.pop(0)
                for cmd in command:
                    comm_obj = comm_obj.commands[cmd]
        except KeyError:
            return KeyError
        for check in comm_obj.checks:
            if hasattr(check, "__name__") and check.__name__ == "is_owner_check":
                return False
        return comm_obj

    async def disable_commands(self): # runs at boot
        for cmd in self.disabled_commands:
            cmd_obj = await self.get_command(cmd)
            try:
                cmd_obj.enabled = False
                cmd_obj.hidden = True
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def leave(self, ctx):
        """Leaves server"""
        message = ctx.message
        await self.bot.say("Are you **SURE** you want me to leave this server?"
                           " Type `yes` to confirm.")
        response = await self.bot.wait_for_message(author=message.author)

        if response.content.lower().strip() == "yes":
            await self.bot.say("Peace im leaving this server! Bye! :wave: ")
            log.debug('Leaving "{}"'.format(message.server.name))
            await self.bot.leave_server(message.server)
        else:
            await self.bot.say("Guess im staying in **{}** then ¯\_(ツ)_/¯.".format(server.name))

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def servers(self, ctx):
        """Lists and allows to leave servers"""
        owner = ctx.message.author
        servers = sorted(list(self.bot.servers),
                         key=lambda s: s.name.lower())
        msg = ""
        for i, server in enumerate(servers):
            msg += "{}: {}\n".format(i, server.name)
        msg += "\nType The server # and im out of that server."

        for page in pagify(msg, ['\n']):
            await self.bot.say(page)

        while msg is not None:
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            try:
                msg = int(msg.content)
                await self.leave_confirmation(servers[msg], owner, ctx)
                break
            except (IndexError, ValueError, AttributeError):
                pass

    async def leave_confirmation(self, server, owner, ctx):
        await self.bot.say("Are you sure you want me "
                    "to leave {}? (yes/no)".format(server.name))

        msg = await self.bot.wait_for_message(author=owner, timeout=15)

        if msg is None:
            await self.bot.say("I guess not.")
        elif msg.content.lower().strip() in ("yes", "y"):
            await self.bot.leave_server(server)
            if server != ctx.message.server:
                await self.bot.say("I've Left.")
        else:
            await self.bot.say(":thinking: ")

    @commands.command()
    @checks.is_owner()
    async def inv(self, *, server: str):
        """ 
        gets an invite link for the server that the bot is in.
        """
        invite = await self.bot.create_invite(discord.utils.find(lambda m: m.name == server, self.bot.servers))
        await self.bot.say(str(invite))

    @commands.command()
    async def servercount(self):
        '''General global server information'''
        servers = sorted([server.name for server in self.bot.servers])
        ret = "I am currently in "
        ret += bold(len(servers))
        ret += " servers with "
        ret += bold(len(set(self.bot.get_all_members())))
        ret += " members.\n"
        await self.bot.say(ret)

    @commands.command()
    async def support(self):
        """Support continued bot and cog development.
        """
        await self.bot.say("If you'd like to support continued bot and cog "
                           "development, I'd greatly appreciate that.\n\n"
                           "Patreon: https://www.patreon.com/bePatron?u=4862715")
    @commands.command()
    async def github(self):
        """Support continued bot and cog development.
        """
        await self.bot.say("If you like Legacy's Bot And his cogs this is the github "
                           "Cogs are indevelopment, Thanks for choosing Legacy's Bot\n\n"
                           "Git Hub ==> I don't have one xD")

    @commands.command()
    async def invite(self):
        """Invite me to a new server"""
        await self.bot.whisper("You must have manage server permissions in order"
                           " to add me to a new server. If you do, just click"
                           " the link below and select the server you wish for"
                           " me to join.\n\n"
                           "https://discordapp.com/oauth2/authorize?client_id=248032345603571712&scope=bot&permissions=-1\n\n"                
                           "Join My support server here.\n\n"
                           "https://discord.gg/dVEkSh4"
						   " Donate so the bot stays alive"
						   " https://www.patreon.com/bePatron?u=4862715")
    @commands.command(pass_context=True)
    async def contact(self, ctx, *, message : str):
        """Sends message to the owner"""
        if self.bot.settings.owner is None:
            await self.bot.say("I have no owner set.")
            return
        owner = discord.utils.get(self.bot.get_all_members(),
                                  id=self.bot.settings.owner)
        author = ctx.message.author
        if ctx.message.channel.is_private is False:
            server = ctx.message.server
            source = ", server **{}** ({})".format(server.name, server.id)
        else:
            source = ", direct message"
        sender = "From **{}** ({}){}:\n\n".format(author, author.id, source)
        message = sender + message
        try:
            await self.bot.send_message(owner, message)
        except discord.errors.InvalidArgument:
            await self.bot.say("I cannot send your message, I'm unable to find"
                               " my owner... *sigh*")
        except discord.errors.HTTPException:
            await self.bot.say("The message you wrote is way too long.")
        except:
            await self.bot.say("I'm unable to deliver your message. Sorry.")
        else:
            await self.bot.say("**Your message has been sent.** :ok_hand:")

    async def leave_confirmation(self, server, owner, ctx):
        if not ctx.message.channel.is_private:
            current_server = ctx.message.server
        else:
            current_server = None
        answers = ("yes", "y")
        await self.bot.say("Are you sure you want me "
                    "to leave ***{}?**** (yes/no)".format(server.name))
        msg = await self.bot.wait_for_message(author=owner, timeout=15)
        if msg is None:
            await self.bot.say("Aint Reply Yes so ¯\_(ツ)_/¯")
        elif msg.content.lower().strip() in answers:
            await self.bot.leave_server(server)
            if server != current_server:
                await self.bot.say("I have succesfully left that server!")
        else:
            await self.bot.say("`Alright then.`")

    @commands.command()
    async def info(self):
        """Shows info about ETLegacy"""  
        author_repo = "https://discordapp.com/oauth2/authorize?client_id=248032345603571712&scope=bot&permissions=-1"
        red_repo = "None"
        server_url = "https://discord.gg/dVEkSh4"
        discordpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2016, 1, 2, 0, 0)
        days_since = (datetime.datetime.now() - since).days
        python_url = "https://www.python.org/"
        dpy_version = "[{}]({})".format(discord.__version__, discordpy_repo)
        py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3],
                                             python_url)

        name = self.bot.user.name

        avatar = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url

        owner_set = self.bot.settings.owner != "id_here"
        owner = self.bot.settings.owner if owner_set else None
        if owner:
            owner = discord.utils.get(self.bot.get_all_members(), id=owner)
            if not owner:
                try:
                    owner = await self.bot.get_user_info(self.bot.settings.owner)
                except:
                    owner = None
        if not owner:
            owner = "Unknown"

        about = (
            "This is a heavily edited instance of Red By TwentySix : [ETLegacy- A fun Moderative utility bot for all your needs]({}) "
            "edited by [{}]({}) With teddy and Dangerous Help!.\n\n"
            "ETLegacy Is Just a Fun Moderative Utility bot Any command invoked is automatically fun with ETLegacy "
            "fun content for everyone to enjoy. [Join us today]({}) "
            "and help us improve!\n\n"
            "Written in [Python]({}), powered by [discord.py]({})"
            "".format(author_repo, owner, red_repo, server_url, python_url,
                      discordpy_repo))

        embed = discord.Embed(colour=discord.Colour.purple())
        embed.add_field(name="Owner", value=str(owner))
        embed.add_field(name="Python", value=py_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="ETLegacy", value=about)
        embed.set_footer(text="Hosted by Nemu Technology.".format(name), icon_url=avatar)

        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")
    @commands.command()
    async def python(self):
        """Shows info about Legacy"""  
        author_repo = "http://www.learnpython.org/"
        red_repo = "http://aiohttp.readthedocs.io/en/stable/"
        server_url = "http://discordpy.readthedocs.io/en/latest/api.html"
        owner = "https://docs.python.org/3/"
        discordpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2016, 1, 2, 0, 0)
        days_since = (datetime.datetime.now() - since).days
        python_url = "https://github.com/Rapptz/discord.py/tree/master/discord/ext/commands"
        dpy_version = "[{}]({})".format(discord.__version__, discordpy_repo)
        py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3],
                                             python_url)

        name = self.bot.user.name

        avatar = self.bot.user.avatar_url if self.bot.user.avatar else self.bot.user.default_avatar_url

        about = (
            "**Python is a coding language** [Learn Python]({})\n"
            "Python docs [Documentation]({})\n"
            "AioHttp Docs [Learn AioHttp]({})\n"
            "Discord.py is Discords version of python :P Have fun coding\n"
            "Discord.py Docs [Learn today]({})"
            "\n"
            "Commands Ext Docstrings: [Python]({}), powered by [discord.py]({})\n\n"
            "".format(author_repo, owner, red_repo, server_url, python_url,
                      discordpy_repo))

        embed = discord.Embed(colour=discord.Colour.purple())
        embed.add_field(name="Python", value=py_version)
        embed.add_field(name="Brought to you by", value="Alan")
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="Python&D.py Help", value=about)
        embed.set_footer(text="This is useless to uses on phone move along. :P".format(name), icon_url=avatar)

        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    @commands.command()
    async def uptime(self):
        """Shows ETLegacy uptime"""
        try:
            uptime = abs(self.bot.uptime - int(time.perf_counter()))
        except TypeError:
            uptime = time.time() - time.mktime(self.bot.uptime.timetuple())
        up = datetime.timedelta(seconds=uptime)
        days = up.days
        hours = int(up.seconds/3600)
        minutes = int(up.seconds % 3600/60)
        colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        em = discord.Embed(description='I have Been up for: {} Days {} Hours And {} Minutes'.format(str(days), str(hours), str(minutes)), colour=discord.Colour(value=colour))
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def sudo(self, ctx, user: discord.Member, *, command):
        """Runs the [command] as if [user] had run it. DON'T ADD A PREFIX
        """
        new_msg = deepcopy(ctx.message)
        new_msg.author = user
        new_msg.content = self.bot.settings.get_prefixes(new_msg.server)[0] \
            + command
        await self.bot.process_commands(new_msg)

    def _load_cog(self, cogname):
        if not self._does_cogfile_exist(cogname):
            raise CogNotFoundError(cogname)
        try:
            mod_obj = importlib.import_module(cogname)
            importlib.reload(mod_obj)
            self.bot.load_extension(mod_obj.__name__)
        except SyntaxError as e:
            raise CogLoadError(*e.args)
        except:
            raise

    def _unload_cog(self, cogname, reloading=False):
        if not reloading and cogname == "cogs.owner":
            raise OwnerUnloadWithoutReloadError(
                "Can't unload the owner plugin :P")
        try:
            self.bot.unload_extension(cogname)
        except:
            raise CogUnloadError

    def _list_cogs(self):
        cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
        return ["cogs." + os.path.splitext(f)[0] for f in cogs]

    def _does_cogfile_exist(self, module):
        if "cogs." not in module:
            module = "cogs." + module
        if module not in self._list_cogs():
            return False
        return True

    def _wait_for_answer(self, author):
        print(author.name + " requested to be set as owner. If this is you, "
              "type 'yes'. Otherwise press enter.")
        print()
        print("*DO NOT* set anyone else as owner. This has security "
              "repercussions.")

        choice = "None"
        while choice.lower() != "yes" and choice == "None":
            choice = input("> ")

        if choice == "yes":
            self.bot.settings.owner = author.id
            self.bot.settings.save_settings()
            print(author.name + " has been set as owner.")
            self.setowner_lock = False
            self.owner.hidden = True
        else:
            print("The set owner request has been ignored.")
            self.setowner_lock = False

    async def server_locker(self, server):
        if self._is_server_locked():
            await self.bot.leave_server(server)


    def _list_cogs(self):
        cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
        return ["cogs." + os.path.splitext(f)[0] for f in cogs]

def check_files():
    if not os.path.isfile("data/red/disabled_commands.json"):
        print("Creating empty disabled_commands.json...")
        dataIO.save_json("data/red/disabled_commands.json", [])

    if not os.path.exists('data/admin/settings.json'):
        try:
            os.mkdir('data/admin')
        except FileExistsError:
            pass
        else:
            dataIO.save_json('data/admin/settings.json', {})


def setup(bot):
    check_files()
    n = Owner(bot)
    bot.add_cog(n)
    bot.add_listener(n.server_locker, "on_server_join")