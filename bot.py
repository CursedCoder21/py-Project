import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Configure intents with specific permissions
intents = discord.Intents.default()
intents.voice_states = True
intents.guild_messages = True

# Define Spotify access details
client_id = "f7167bad4c154bdd88556072d12f7b86"
client_secret = "b79b70ed68b24be39332170a7b105aa9"

# Create Spotify and Discord clients
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
bot = commands.Bot(command_prefix="!", intents=intents)

# Voice client dictionary
voice_clients = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def join(ctx):
    voice_client = voice_clients.get(ctx.guild.id)

    # Check if already connected
    if voice_client and voice_client.is_connected():
        await ctx.send('Bot is already connected to the voice channel.')
        return

    try:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        voice_clients[ctx.guild.id] = voice_client
        print(f'Joined voice channel: {channel.name}')
    except discord.errors.ClientException:
        await ctx.send('Failed to join voice channel.')
        return

@bot.command()
async def play(ctx, query):
    # Get the voice client
    voice_client = voice_clients.get(ctx.guild.id)

    # Check if voice client exists and is connected
    if not voice_client or not voice_client.is_connected():
        await ctx.send('Bot is not connected to a voice channel.')
        return

    # Search for the song using Spotipy
    results = sp.search(q=query, type="track")
    track = results["tracks"]["items"][0]

    # Download the song
    # ... (implement song download logic here) ...

    # Play the song
    # ... (implement song playback logic here) ...

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
