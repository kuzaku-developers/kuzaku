def init_dashboard(bot):
    @bot.dashboard.route
    async def get_stats(data):
        channels_list = []
        for guild in bot.guilds:
            for channel in guild.channels:
                channels_list.append(channel)
        return {
            "status": "200",
            "message": "all is ok",
            "guilds": str(len(bot.guilds)),
            "users": str(len(bot.users)),
            "channels": len(channels_list),
        }

    @bot.dashboard.route
    async def get_invite_url(data):
        return f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands&permissions=473197655"

    @bot.dashboard.route
    async def get_mutual_guilds(data):
        guild_ids = []
        for guild in bot.guilds:
            guild_ids.append(guild.id)
        return guild_ids