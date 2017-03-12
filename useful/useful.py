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