import discord
import time
import asyncio
import requests
import praw
import random
import wavelink
import re

from discord import app_commands
from discord.ext import commands
from unidecode import unidecode
from youtubesearchpython import *
from threading import Thread
from datetime import datetime

from help import *

API_TOKEN = 'your token here'
Reddit_client_id = 'your id here'
Reddit_client_secret = 'all of your secrets'
Reddit_app_name = 'My name is... What?'
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 630, 1000, 1600, 2500, 4000, 10000, 16000)


class CustomPlayer(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix = "!", intents = intents, slash_options={"delete_unused": True})

    async def setup_hook(self):
        await self.tree.sync()


client = Bot()
client.remove_command('help')


# HTTPS and websocket operations

@client.event
async def on_ready():
    client.loop.create_task(connect_nodes())


# Helper function
async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,
        host='127.0.0.1',
        port=2333,
        password='youshallnotpass'
    )


## Custom message
@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    await client.change_presence(activity=discord.Game('BZZZZ 🐝'))
    print(f'Node: <{node.identifier}> is ready!')


@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.tracks, reason):
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)


# Get response for this particular question
@client.event
async def on_message(message):
	text = unidecode(message.content).lower()
	if text == "league of legends":
		await message.reply("🤮🤮")
	await client.process_commands(message)


# Yeah fuck this guy in particular
Dywanobot = False
@client.event
async def on_voice_state_update(member, before, after):
	if(member.id == 284580506878869504):
		global Dywanobot
		if before.channel is None and after.channel is not None:
			Dywanobot = False
			thread = Thread(target = IsDywan, args = (after, ))
			thread.start()
		if before.channel is not None and after.channel is None:
			Dywanobot = True


# If this dickhead is in voice channel for an hour now start blasting `legia to chuje`
def IsDywan(after):
	vc = after.channel.guild.voice_client
	global Dywanobot
	while(True):
		time.sleep(1*60*60)
		if(Dywanobot == True):
			break
		if not vc:
			send_fut = asyncio.run_coroutine_threadsafe(join(after), client.loop)
			send_fut.result()
			send_fut = asyncio.run_coroutine_threadsafe(legiatochuje(after), client.loop)
			send_fut.result()
		elif vc:
			if not vc.is_playing():
				send_fut = asyncio.run_coroutine_threadsafe(legiatochuje(after), client.loop)
				send_fut.result()


async def join(after):
	vc = after.channel.guild.voice_client
	custom_player = CustomPlayer()
	vc: CustomPlayer = await after.channel.connect(cls=custom_player)


async def legiatochuje(after):
	vc = after.channel.guild.voice_client
	tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, "https://www.youtube.com/watch?v=ZHuUcaw4Yz4")
	await vc.play(tracks[0])


# Commands

@client.hybrid_command(name = "help", with_app_command = True, description = "Show available commands")
async def help(ctx: commands.Context, cmd: str = None):
	embed = discord.Embed(color=0xFF00FF)
	global Commands_available
	if (cmd != None):
		for i in Commands_available['name']:
			if (cmd.split()[0] == i.split()[0]):
				Com_available = Commands_available.set_index('name')
				embed.add_field(name=cmd.split()[0]+':', value=Com_available.loc[i]['detailed description'] + '.', inline=False)
	else:
		Com_available = Commands_available.sort_values(['name']).set_index('category')
		for cats in Commands_available.sort_values(['category'])['category'].unique():
			cmd_av = ''
			if (cats == 'aHelp'):
				cmd_av += "• !" + Com_available.loc[cats]['name'] + " - " + Com_available.loc[cats]['description'] + '.'
			else:
				for i in range(len(Com_available.loc[cats]['name'])):
					cmd_av += "• !" + Com_available.loc[cats]['name'][i] + " - " + Com_available.loc[cats]['description'][i] + ";\n"
				cmd_av = cmd_av[:-2] + '.'
			embed.add_field(name=cats[1:]+':', value=cmd_av, inline=False)
	await ctx.send(embed=embed)


@client.command()
async def connect(ctx):
    vc = ctx.voice_client # represents a discord voice connection
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        return await ctx.send("Please join a voice channel to connect.")

    if not vc:
        await ctx.author.voice.channel.connect(cls=CustomPlayer())
    else:
        await ctx.send("The bot is already connected to a voice channel")


@client.command()
async def disconnect(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.hybrid_command(name = "play", with_app_command = True, description = "Searching, URLs, and playlists (YT only)")
async def play(ctx: commands.Context, song: str):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

    # playlist
    if(song.find('&list=') != -1):
        tracks = await wavelink.NodePool.get_node().get_playlist(wavelink.YouTubePlaylist, song)
        await ctx.send('Song added')
        for song in tracks.tracks[1:]:
            vc.queue.put(item=song)
        if not vc.is_playing():
            await vc.play(tracks.tracks[0])

    # single track
    elif(song.find('youtube.com') != -1):
        tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, song)
        await ctx.send('Song added')
        if vc.is_playing():
            vc.queue.put(item=tracks[0])
        else:
            await vc.play(tracks[0])

    # searching
    else:
        search = VideosSearch(song, limit = 1).result()['result'][0]['link']
        tracks = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, search)
        await ctx.send('Song added')
        if vc.is_playing():
            vc.queue.put(item=tracks[0])
        else:
            await vc.play(tracks[0])


@client.hybrid_command(name = "skip", with_app_command = True, description = "Skips")
async def skip(ctx):
    vc = ctx.voice_client
    if vc:
        if not vc.is_playing():
            return await ctx.send("Nothing is playing.")
        ctx.send('Song skipped')
        if vc.queue.is_empty:
            return await vc.stop()

        await vc.seek(vc.track.length * 1000)
        if vc.is_paused():
            await vc.resume()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.hybrid_command(name = "pause", with_app_command = True, description = "Pauses")
async def pause(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await ctx.send("Song paused")
            await vc.pause()
        else:
            await ctx.send("Nothing is playing.")
    else:
        await ctx.send("The bot is not connected to a voice channel")


@client.hybrid_command(name = "resume", with_app_command = True, description = "Resumes")
async def resume(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_paused():
            await ctx.send("Song is now playing")
            await vc.resume()
        else:
            await ctx.send("Nothing is paused.")
    else:
        await ctx.send("The bot is not connected to a voice channel")


@client.hybrid_command(name = "stop", with_app_command = True, description = "Stop playing and clear playlist")
async def stop(ctx):
    vc = ctx.voice_client
    if vc:
        if not vc.queue.is_empty:
            vc.queue.clear()
        if vc.is_playing() and not vc.is_paused():
            await vc.stop()
            await ctx.send("Song stopped")
        else:
            await ctx.send("Nothing is playing.")
    else:
        await ctx.send("The bot is not connected to a voice channel")


@client.hybrid_command(name = "volume", with_app_command = True, description = "Sets volume from 0 to 1000, 1000 is kinda earrape")
async def volume(ctx: commands.Context, volume: str):
	vc = ctx.voice_client
	volume = int(volume)
	if(volume < 1):
		volume = 1
	elif(volume > 1000):
		volume = 1000

	await ctx.send("Volume is now at " + str(volume) + "%")
	await vc.set_volume(volume)


switch = False
@client.hybrid_command(name = "nightcore", with_app_command = True, description = "~( ˘▾˘~)♡♫♩♬")
async def nightcore(ctx):
	vc = ctx.voice_client
	global switch
	if(switch == False):
		switch = True
		await ctx.send("Nightcore on")
		await vc.set_filter(wavelink.Filter(timescale = wavelink.Timescale(speed = 1.2, pitch = 1.3)))
	else:
		switch = False
		await ctx.send("Nightcore off")
		await vc.set_filter(wavelink.Filter(timescale = wavelink.Timescale(speed = 1.0, pitch = 1.0)))


@client.hybrid_command(name = "bassboost", with_app_command = True, description = "Boosting basses, from 0 to 100, to 15 is ok")
async def bassboost(ctx: commands.Context, boost: str):
	vc = ctx.voice_client
	boost = int(boost)
	if boost < 0:
		boost = 0
	elif boost > 100:
		boost = 100
	boost = boost / 100
	HZ = []
	cnt = 0
	for i in HZ_BANDS:
		if (HZ_BANDS[cnt] >= 60 and HZ_BANDS[cnt] <= 150):
			HZ.append([cnt, boost])
		else:
			HZ.append([cnt, 0.0])
		cnt += 1

	await ctx.send("Bassboost is now at " + str(boost*100) + "%")
	await vc.set_filter(wavelink.Filter(equalizer = wavelink.Equalizer(bands = HZ)))


@client.hybrid_command(name = "playlist", with_app_command = True, description = "Spits out actual playlist")
async def playlist(ctx):
	vc = ctx.voice_client
	if(vc.queue.is_empty and vc.track == None):
		await ctx.send("Playlista ist empty")
	else:
		embed = discord.Embed(color=0xFF00FF)
		playlist =  'Now: ' + str(vc.track) + '\n'
		i = 1
		for track in vc.queue:
			playlist += str(i) + '. ' + str(track) + '\n'
			i += 1
			if i >= 15:
				playlist += '...\n'
				break
		embed.add_field(name="Commands:", value=playlist, inline=False)
		await ctx.send(embed=embed)


# gifs & pics

@client.hybrid_command(name = "pls", with_app_command = True, description = "Sends pic or gif or selected tag, /help pls for more info")
@app_commands.choices(choices=[
	app_commands.Choice(name="4k", value="4k"),
	app_commands.Choice(name="ass", value="ass"),
	app_commands.Choice(name="pussy", value="pussy"),
	app_commands.Choice(name="boobs", value="boobs"),
	app_commands.Choice(name="neko", value="neko"),
	app_commands.Choice(name="hentai", value="hentai"),
	app_commands.Choice(name="hentai neko", value="hneko"),
	app_commands.Choice(name="hentai kitsune", value="hkitsune"),
	app_commands.Choice(name="anal", value="anal"),
	app_commands.Choice(name="hentai anal", value="hanal"),
	app_commands.Choice(name="food", value="food"),
	app_commands.Choice(name="tentacle", value="tentacle"),
	app_commands.Choice(name="hboobs", value="hboobs"),
	app_commands.Choice(name="pgif", value="pgif"),
	])
async def pls(ctx: discord.Interaction, choices: app_commands.Choice[str]):
	global tags
	if choices.value in tags:
		ret = requests.get("https://nekobot.xyz/api//image?type=" + choices.value).json()
		url=ret["message"]
		await sendpic(ctx, url)
	else:
		embed = discord.Embed(color=0xFF00FF)
		tags_av = ''
		for i in tags:
			tags_av += i + ', '
		tags_av = tags_av[:-2] + '.'
		embed.add_field(name="Tags available:", value=tags_av, inline=False)
		await ctx.send(embed=embed)


@client.hybrid_command(name = "dicpic", with_app_command = True, description = "Sends dic pic")
async def dicpic(ctx):
	reddit = praw.Reddit(client_id=Reddit_client_id,
					client_secret=Reddit_client_secret,
					user_agent=Reddit_app_name, check_for_async=False)

	posts = reddit.subreddit('MassiveCock').hot()
	while True:
		nmb = random.randint(1, 100)
		for i in range(0, nmb):
			post = next(x for x in posts if not x.stickied)
		if "i.redd.it" in post.url:
			break

	await sendpic(ctx, post.url)


async def sendpic(ctx, url):
	embed = discord.Embed()
	embed.set_image(url=url)
	await ctx.send(embed=embed)


# Misc

# Should set timer for laundry, but I had no time to do it
@client.hybrid_command(name = "laundry", with_app_command = True, description = "Laundry timer")
async def laundry(ctx: commands.Context, timer: str):
	now = datetime.now()

	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	dates = dt_string.split('/')
	tmp = dates[2].split(' ')
	dates[2] = tmp[0]
	times = tmp[1].split(':')

	or_date = [18, 1, 2023]
	or_time = ['00', '00', '00']

	minutes = ((int(dates[2]) - or_date[2])*365*24*60) + ((int(dates[1]) - or_date[1])*30*24*60) + ((int(dates[0]) - or_date[0])*24*60) + (int(times[0])*60) + int(times[1])

	await ctx.send('Command is in TODO phase: -' + str(minutes))

client.run(API_TOKEN)