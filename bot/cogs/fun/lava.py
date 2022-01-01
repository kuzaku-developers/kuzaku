import asyncio
import async_timeout
import copy
import datetime
import disnake
import math
import random
import re
import typing
import wavelink
from disnake.ext import commands

# URL matching REGEX...
URL_REG = re.compile(r"https?://(?:www\.)?.+")


class NoChannelProvided(commands.CommandError):
    """Error raised when no suitable voice channel was supplied."""

    pass


class IncorrectChannelError(commands.CommandError):
    """Error raised when commands are issued outside of the players session channel."""

    pass


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ("requester",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")


class Player(wavelink.Player):
    """Custom wavelink Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = kwargs.get("context", None)
        if self.context:
            self.dj: disnake.Member = self.context.author

        self.queue = asyncio.Queue()
        self.controller = None

        self.waiting = False
        self.updating = False

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.stop_votes = set()

    async def do_next(self) -> None:
        if self.is_playing or self.waiting:
            return

        # Clear the votes for a new song...
        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.stop_votes.clear()

        try:
            self.waiting = True
            with async_timeout.timeout(300):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            # No music has been played for 5 minutes, cleanup and disconnect...
            return await self.teardown()

        await self.play(track)
        self.waiting = False

        # Invoke our players controller...
        # await self.invoke_controller()

    async def invoke_controller(self) -> None:
        """Method which updates or sends a new player controller."""
        if self.updating:
            return

        self.updating = True

        if not self.controller:
            self.controller = InteractiveController(
                embed=self.build_embed(), player=self
            )
            await self.controller.start(self.context)

        elif not await self.is_position_fresh():
            try:
                await self.controller.message.delete()
            except disnake.HTTPException:
                pass

            self.controller.stop()

            self.controller = InteractiveController(
                embed=self.build_embed(), player=self
            )
            await self.controller.start(self.context)

        else:
            embed = self.build_embed()

            await self.channel.send(embed=self.embed)

        self.updating = False

    def build_embed(self) -> typing.Optional[disnake.Embed]:
        """Method which builds our players controller embed."""
        track = self.current
        if not track:
            return

        channel = self.bot.get_channel(int(self.channel_id))
        qsize = self.queue.qsize()

        embed = disnake.Embed(
            title=f"Music Controller | {channel.name}", colour=0xEBB145
        )
        embed.description = f"Now Playing:\n**`{track.title}`**\n\n"
        embed.set_thumbnail(url=track.thumb)

        embed.add_field(
            name="Duration",
            value=str(datetime.timedelta(milliseconds=int(track.length))),
        )
        embed.add_field(name="Queue Length", value=str(qsize))
        embed.add_field(name="Volume", value=f"**`{self.volume}%`**")
        embed.add_field(name="Requested By", value=track.requester.mention)
        embed.add_field(name="DJ", value=self.dj.mention)
        embed.add_field(name="Video URL", value=f"[Click Here!]({track.uri})")

        return embed

    async def is_position_fresh(self) -> bool:
        """Method which checks whether the player controller should be remade or updated."""
        try:
            async for message in self.context.channel.history(limit=5):
                if message.id == self.controller.message.id:
                    return True
        except (disnake.HTTPException, AttributeError):
            return False

        return False

    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""


        try:
            await self.destroy()
        except KeyError:
            pass


class InteractiveController:
    def __init__(self, *, embed: disnake.Embed, player: Player):
        super().__init__()

        self.embed = embed
        self.player = player

    def update_context(self, payload: disnake.RawReactionActionEvent):
        """Update our context with the user who reacted."""
        ctx = copy.copy(self.ctx)
        ctx.author = payload.member

        return ctx

    def reaction_check(self, payload: disnake.RawReactionActionEvent):
        if payload.event_type == "REACTION_REMOVE":
            return False

        if not payload.member:
            return False
        if payload.member.bot:
            return False
        if payload.message_id != self.message.id:
            return False
        if (
            payload.member
            not in self.bot.get_channel(int(self.player.channel_id)).members
        ):
            return False

        return payload.emoji in self.buttons

    async def send_initial_message(
        self, ctx, channel: disnake.TextChannel
    ) -> disnake.Message:
        return await channel.send(embed=self.embed)


class Musicc(commands.Cog, wavelink.WavelinkMixin):
    """Music Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if not hasattr(bot, "wavelink"):
            bot.wavelink = wavelink.Client(bot=bot)

        bot.loop.create_task(self.start_nodes())
    async def getRadio(self, radio):
        if radio=="Ретро FM":
            return "http://retroserver.streamr.ru:8043/retro256.mp3"
        elif radio=="Дорожное радио":
            return "http://dorognoe.hostingradio.ru:8000/radio"
    async def start_nodes(self) -> None:
        """Connect and intiate nodes."""
        await self.bot.wait_until_ready()

        if self.bot.wavelink.nodes:
            self.bot.log.warn("Lavalink :: Initializing nodes")
            previous = self.bot.wavelink.nodes.copy()

            for node in previous.values():
                await node.destroy()

        nodes = {'MAIN': {'host': 'node01.lavalink.eu',
                          'port': 2333,
                          'rest_uri': 'http://node01.lavalink.eu:2333',
                          'password': 'Raccoon',
                          'identifier': 'MAIN',
                          'region': 'us_central'
                          }}
        for n in nodes.values():
            await self.bot.wavelink.initiate_node(**n)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        self.bot.log.info(f"Lavalink :: node {node.identifier} is ready")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node: wavelink.Node, payload):
        await payload.player.do_next()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState,
    ):
        if member.bot:
            return

        player: Player = self.bot.wavelink.get_player(member.guild.id, cls=Player)

        if not player.channel_id or not player.context:
            player.node.players.pop(member.guild.id)
            return

        channel = self.bot.get_channel(int(player.channel_id))

        if member == player.dj and after.channel is None:
            for m in channel.members:
                if m.bot:
                    continue
                else:
                    player.dj = m
                    return

        elif after.channel == channel and player.dj not in channel.members:
            player.dj = member

    async def cog_command_error(self, ctx, error: Exception):
        """Cog wide error handler."""
        if isinstance(error, IncorrectChannelError):
            return

        if isinstance(error, NoChannelProvided):
            return await ctx.send(":warning: Вы должны быть в канале или указать его!")

    async def cog_check(self, ctx):
        """Cog wide check, which disallows commands in DMs."""
        if not ctx.guild:
            await ctx.send(":warning: Музыкальные команды недоступны в лс.")
            return False

        return True

    async def cog_before_invoke(self, ctx):
        """Coroutine called before command invocation.

        We mainly just want to check whether the user is in the players controller channel.
        """
        player: Player = self.bot.wavelink.get_player(
            ctx.guild.id, cls=Player, context=ctx
        )

        if ctx.command.name == "connect" and not player.context:
            return
        elif self.is_privileged(ctx):
            return

        if not player.channel_id:
            return

        channel = self.bot.get_channel(int(player.channel_id))
        if not channel:
            return

        if player.is_connected:
            if ctx.author not in channel.members:
                await ctx.send(
                    f"{ctx.author.mention}, you must be in `{channel.name}` to use voice commands."
                )
                raise IncorrectChannelError

    def required(self, ctx):
        """Method which returns required votes based on amount of members in a channel."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        channel = self.bot.get_channel(int(player.channel_id))
        required = math.ceil((len(channel.members) - 1) / 2.5)

        if ctx.command.name == "stop":
            if len(channel.members) == 3:
                required = 2

        return required

    def is_privileged(self, ctx):
        """Check whether the user is an Admin or DJ."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        return player.dj == ctx.author or ctx.author.guild_permissions.kick_members

    @commands.slash_command(
        name="connect",
        description="Connect to a voice channel.",
    )
    async def connect(self, ctx, channel: disnake.VoiceChannel = None):
        """Connect to a voice channel."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if player.is_connected:
            return

        channel = getattr(ctx.author.voice, "channel", channel)
        if channel is None:
            raise NoChannelProvided

        await player.connect(channel.id)

    @commands.slash_command(
        name="play",
        description="Play some music!",
    )
    async def play(self, ctx, query: str):
        """Play or queue a song with the given query."""
        await ctx.response.defer()
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            try:
                await player.connect(ctx.author.voice.channel.id)
            except:
                return await ctx.send(
                    content="Сначала войдите в голосовой канал!"
                )
        query = query.strip("<>")
        if not URL_REG.match(query):
            query = f"ytsearch:{query}"

        tracks = await self.bot.wavelink.get_tracks(query)
        if not tracks:
            return await ctx.send(
                content="<a:no_anim:796454160283074611> Увы, треков не найдено. Повторите попытку."
            )

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                track = Track(track.id, track.info, requester=ctx.author)
                await player.queue.put(track)

            await ctx.send(
                content=f'```ini\nПлейлист {tracks.data["playlistInfo"]["name"]}'
                f" с {len(tracks.tracks)} треками добавлен в очередь.\n```"
            )
        else:
            track = Track(tracks[0].id, tracks[0].info, requester=ctx.author)
            await ctx.send(
                content=f"```ini\nТрек {track.title} добавлен в очередь\n```"
            )
            await player.queue.put(track)

        if not player.is_playing:
            await player.do_next()


    @commands.slash_command(name="radio", description="Radio, yes!")
    async def radio_(self, ctx, radio: str =commands.Param(
            choices=[
                "Ретро FM",
                "Дорожное радио",
            ]
        ),):
        query=await self.getRadio(radio)
        """Play or queue a song with the given query."""
        await ctx.response.defer()
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            try:
                await player.connect(ctx.author.voice.channel.id)
            except:
                return await ctx.send(
                    content="Сначала войдите в голосовой канал!"
                )
        query = query.strip("<>")
        if not URL_REG.match(query):
            query = f"scsearch:{query}"

        tracks = await self.bot.wavelink.get_tracks(query)
        if not tracks:
            return await ctx.send(
                content="<a:no_anim:796454160283074611> Увы, треков не найдено. Повторите попытку."
            )

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                track = Track(track.id, track.info, requester=ctx.author)
                await player.queue.put(track)

            await ctx.send(
                content=f'```ini\nПлейлист {tracks.data["playlistInfo"]["name"]}'
                f" с {len(tracks.tracks)} треками добавлен в очередь.\n```"
            )
        else:
            track = Track(tracks[0].id, tracks[0].info, requester=ctx.author)
            await ctx.send(
                content=f"```ini\nРадио {radio} добавлено в очередь\n```"
            )
            await player.queue.put(track)

        if not player.is_playing:
            await player.do_next()

    @commands.slash_command(
        name="pause",
        description="Pause the currently playing song.",
    )
    async def pause(self, ctx):
        """Pause the currently playing song."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if player.is_paused or not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send("Админ или DJ поставил проигрыватель на паузу.")
            player.pause_votes.clear()

            return await player.set_pause(True)

        required = self.required(ctx)
        player.pause_votes.add(ctx.author)

        if len(player.pause_votes) >= required:
            await ctx.send("Голосование за остановку пройдено. Останавливаю.")
            player.pause_votes.clear()
            await player.set_pause(True)
        else:
            await ctx.send(f"{ctx.author.mention} Проголосовал за остановку.")

    @commands.slash_command(
        name="resume",
        description="Resume a currently paused player.",
    )
    async def resume(self, ctx):
        """Resume a currently paused player."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_paused or not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send("An admin or DJ has resumed the player.")
            player.resume_votes.clear()

            return await player.set_pause(False)

        required = self.required(ctx)
        player.resume_votes.add(ctx.author)

        if len(player.resume_votes) >= required:
            await ctx.send("Vote to resume passed. Resuming player.")
            player.resume_votes.clear()
            await player.set_pause(False)
        else:
            await ctx.send(f"{ctx.author.mention} has voted to resume the player.")

    @commands.slash_command(
        name="skip",
        description="Skip the currently playing song.",
    )
    async def skip(self, ctx):
        """Skip the currently playing song."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send("An admin or DJ has skipped the song.")
            player.skip_votes.clear()

            return await player.stop()

        if ctx.author == player.current.requester:
            await ctx.send("The song requester has skipped the song.")
            player.skip_votes.clear()

            return await player.stop()

        required = self.required(ctx)
        player.skip_votes.add(ctx.author)

        if len(player.skip_votes) >= required:
            await ctx.send("Vote to skip passed. Skipping song.")
            player.skip_votes.clear()
            await player.stop()
        else:
            await ctx.send(f"{ctx.author.mention} has voted to skip the song.")

    @commands.command(name="stop", description="Stop the song.")
    async def stop(self, ctx):
        await ctx.defer()
        """Stop the player and clear all internal states."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send("An admin or DJ has stopped the player.")
            return await player.teardown()

        required = self.required(ctx)
        player.stop_votes.add(ctx.author)

        if len(player.stop_votes) >= required:
            await ctx.send("Vote to stop passed. Stopping the player.")
            await player.teardown()
        else:
            await ctx.send(f"{ctx.author.mention} has voted to stop the player.")

    @commands.slash_command(
        name="volume",
        description="change the players volume, between 1 and 100.",
    )
    async def volume(self, ctx, vol: int):
        """Change the players volume, between 1 and 100."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send("Only the DJ or admins may change the volume.")

        if not 0 < vol < 101:
            return await ctx.send("Please enter a value between 1 and 100.")

        await player.set_volume(vol)
        await ctx.send(f"Set the volume to **{vol}**%")

    @commands.slash_command(
        name="shuffle",
        description="Shuffle the players queue.",
    )
    async def shuffle(self, ctx):
        """Shuffle the players queue."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if player.queue.qsize() < 3:
            return await ctx.send("Add more songs to the queue before shuffling.")

        if self.is_privileged(ctx):
            await ctx.send("An admin or DJ has shuffled the playlist.")
            player.shuffle_votes.clear()
            return random.shuffle(player.queue._queue)

        required = self.required(ctx)
        player.shuffle_votes.add(ctx.author)

        if len(player.shuffle_votes) >= required:
            await ctx.send("Vote to shuffle passed. Shuffling the playlist.")
            player.shuffle_votes.clear()
            random.shuffle(player.queue._queue)
        else:
            await ctx.send(f"{ctx.author.mention} has voted to shuffle the playlist.")

    @commands.command(hidden=True)
    async def vol_up(self, ctx):
        """Command used for volume up button."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected or not self.is_privileged(ctx):
            return

        vol = int(math.ceil((player.volume + 10) / 10)) * 10

        if vol > 100:
            vol = 100
            await ctx.send("Maximum volume reached")

        await player.set_volume(vol)

    @commands.command(hidden=True)
    async def vol_down(self, ctx):
        """Command used for volume down button."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected or not self.is_privileged(ctx):
            return

        vol = int(math.ceil((player.volume - 10) / 10)) * 10

        if vol < 0:
            vol = 0
            await ctx.send("Player is currently muted")

        await player.set_volume(vol)

    @commands.slash_command(
        name="equalizer",
        description="Change the playwr equalizer.",
    )
    async def equalizer(self, ctx, equalizer: str):
        """Change the players equalizer."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send("Only the DJ or admins may change the equalizer.")

        eqs = {
            "flat": wavelink.Equalizer.flat(),
            "boost": wavelink.Equalizer.boost(),
            "metal": wavelink.Equalizer.metal(),
            "piano": wavelink.Equalizer.piano(),
        }

        eq = eqs.get(equalizer.lower(), None)

        if not eq:
            joined = "\n".join(eqs.keys())
            return await ctx.send(f"Invalid EQ provided. Valid EQs:\n\n{joined}")

        await ctx.send(f"Successfully changed equalizer to {equalizer}")
        await player.set_eq(eq)

    @commands.slash_command(
        name="queue",
        description="Display the players queued songs.",
    )
    async def queue(self, ctx):
        """Display the players queued songs."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if player.queue.qsize() == 0:
            return await ctx.send("Очередь пустая.")

        entries = [track.title for track in player.queue._queue]
        embed = disnake.Embed(title="Включаю...", colour=0x4F0321)
        embed.description = "\n".join(
            f"`{index}. {title}`" for index, title in track in player.queue._queue
        )

        await ctx.send(embed=embed)

   

    @commands.slash_command(
        name="swap",
        description="Swap the current DJ to another member in the voice channel.",
    )
    async def swap_dj(self, ctx, member: disnake.Member = None):
        """Swap the current DJ to another member in the voice channel."""
        await ctx.response.defer()
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send("Only admins and the DJ may use this command.")

        members = self.bot.get_channel(int(player.channel_id)).members

        if member and member not in members:
            return await ctx.send(
                f"{member} is not currently in voice, so can not be a DJ."
            )

        if member and member == player.dj:
            return await ctx.send("Cannot swap DJ to the current DJ... :)")

        if len(members) <= 2:
            return await ctx.send("No more members to swap to.")

        if member:
            player.dj = member
            return await ctx.send(f"{member.mention} is now the DJ.")

        for m in members:
            if m == player.dj or m.bot:
                await ctx.send("Вы уже DJ.")
                continue
            else:
                player.dj = m
                return await ctx.send(f"{member.mention} is now the DJ.")


def setup(bot: commands.Bot):
    bot.add_cog(Musicc(bot))
