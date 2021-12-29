from disnake.ext import commands, ipc


class IpcRoutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def get_stats(self, data):
        channels_list = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                channels_list.append(channel)
        return {
            "status": "200",
            "message": "all is ok",
            "guilds": str(len(self.bot.guilds)),
            "users": str(len(self.bot.users)),
            "channels": len(channels_list),
        }

    @ipc.server.route()
    async def get_invite_url(self, data):
        return f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot+applications.commands&permissions=473197655"

    @ipc.server.route()
    async def get_mutual_guilds(self, data):
        guild_ids = []
        for guild in self.bot.guilds:
            guild_ids.append(guild.id)
        return guild_ids


def setup(bot):
    bot.add_cog(IpcRoutes(bot))