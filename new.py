import discord
from discord.ext import commands
from ytmusicapi import YTMusic
import pydub
import ffmpeg

# Install PyNaCl if not already installed
try:
    import nacl.secret
except ImportError:
    print("Installing PyNaCl...")
    subprocess.run(["pip", "install", "PyNaCl"])
    print("PyNaCl installed!")

# Create a new bot instance
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Adjust ffmpeg path if needed
ffmpeg_path = "ffmpeg.exe"  # Update path to your ffmpeg executable

# Command to search and play a song
@bot.command()
async def play(ctx, *, query):
    # Check if user is in a voice channel
    if not ctx.author.voice:
        await ctx.send('You need to be in a voice channel to use this command.')
        return

    # Get the voice channel and connect
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()

    # Initialize YTMusic client and search for song
    ytmusic = YTMusic()
    search_results = ytmusic.search(query, filter='songs', limit=1)

    # Handle song search results
    if search_results:
        song = search_results[0]
        title = song['title']
        artist = song['artists'][0]['name']
        duration = song['duration']

        # Download audio and convert to Opus
        audio_stream = ytmusic.get_stream(song['videoId'])
        downloaded_audio = await audio_stream.read()
        audio_data = pydub.AudioSegment.from_file(downloaded_audio, format="mp3")

        # Convert to Opus using FFmpeg
        ffmpeg = discord.FFmpeg(executable=ffmpeg_path)
        source = ffmpeg.input(audio_data, format="s16le", samplerate=audio_data.frame_rate).output(
            "pipe", format="opus", audio_bitrate="64k"
        )
        process = await source.run_async()

        # Play audio in voice channel
        player = voice_channel.create_stream(process, format="opus")
        await ctx.send(f'Playing: {title} by {artist} ({duration} seconds)')
        await player.start()
        await process.wait()

    else:
        await ctx.send('No results found.')

    # Disconnect after playback
    await voice_channel.disconnect()

# Run the bot
bot.run('MTE4MTMyMTIxNjIxMzEzOTYzOQ.GNMUnz.FJQB_a7eruc4J4PxBI1vPpqYh2zoE0F-2n7Wec')

