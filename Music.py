import asyncio

import discord
from discord.ext import commands
from UrlSource import UrlSource

class Music(commands.Cog):
    """
    collection of commands for music.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play', help="play song from url")
    async def play(self, ctx, *, url):
        """
        Streams audio from url.
        :param ctx:
        :param url:
        :return:
        """
        async with ctx.typing():
            player = await UrlSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @play.before_invoke
    async def auto_connect(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Music(bot))