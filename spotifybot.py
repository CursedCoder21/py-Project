import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import spotify_dl

# Configure intents with specific permissions
intents = discord.Intents.all()
intents.voice_states = True
intents.guild_messages = True


# Define Spotify access details
client_id = "f7167bad4c154bdd88556072d12f7b86"
client_secret = "b79b70ed68b24be39332170a7b105aa9"

# Create Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create Discord bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Voice client dictionary
voice_clients = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def join(ctx):
    """Join the voice channel the author is in."""

    voice_client = voice_clients.get(ctx.guild.id)

    # If already connected, inform the user
    if voice_client and voice_client.is_connected():
        await ctx.send('Bot is already connected to the voice channel.')
        return

    # Get the author's voice channel
    channel = ctx.author.voice.channel

    # Attempt to connect to the voice channel
    try:
        voice_client = await channel.connect()
        voice_clients[ctx.guild.id] = voice_client
        await ctx.send(f'Joined voice channel: {channel.name}')
    except discord.errors.ClientException:
        await ctx.send('Failed to join voice channel.')
        return


@bot.command()
async def play(ctx, query):
    # Get the voice client
    voice_client = voice_clients.get(ctx.guild.id)

    # Check if voice client exists and is connected
    if not voice_client or not voice_client.is_connected():
        await ctx.send('Bot is not connected to a voice channel. Please join a voice channel and try again.')
        return

    # Search for the song using Spotipy
    results = sp.search(q=query, type="track")
    track = results["tracks"]["items"][0]

    # Download the song
    try:
        downloader = spotify_dl.SpotifyDL()
        downloaded_song = await downloader.download(track["uri"])
    except Exception as e:
        await ctx.send(f'Failed to download song: {e}')
        return

    # Check if download successful
    if not downloaded_song:
        await ctx.send(f'Failed to download song: {track["name"]}')
        return

    # Play the downloaded song
    source = discord.FFmpegOpusAudio(downloaded_song)
    voice_client.play(source)

    # Confirm song playback
    await ctx.send(f'Playing: {track["name"]}')


@bot.command()
async def leave(ctx):
    voice_client = voice_clients.get(ctx.guild.id)

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        del voice_clients[ctx.guild.id]
        await ctx.send('Disconnected from voice channel.')
    else:
        await ctx.send('Bot is not connected to any voice channel.')

# Run the bot
bot.run('MTE4MTMyMTIxNjIxMzEzOTYzOQ.GNMUnz.FJQB_a7eruc4J4PxBI1vPpqYh2zoE0F-2n7Wec')
