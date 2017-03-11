    @commands.command(pass_context=True, no_pm=True)
    async def avatar(self, ctx, *, user: discord.Member=None):
        """Retrieves a users avatar."""
        author = ctx.message.author
        if not user:
            user = author
        data = discord.Embed(colour=user.colour)
        data.set_image(url=user.avatar_url)
        data.set_author(name="Avatar for "+user.name, icon_url=user.avatar_url)
        data.set_footer(text=datetime.datetime.now().strftime("%A, %B %-d %Y at %-I:%M%p").replace("PM", "pm").replace("AM", "am"))
        await self.bot.say(embed=data)