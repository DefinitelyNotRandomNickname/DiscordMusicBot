# Dicord music and miscellaneous bot <span style="color:red;">(NSFW)</span>

## Note
Wavelink fucked some shit up and playing audio doesn't work for now. I've used older version of it, if you want to make it work you can try to migrate it to 2.0 or higher version.
I'm too lazy and have more shit to do so I won't work on it for now. If your solution works feel free to share it.

## About
Discord bot that is able to play audio from youtube videos, edit it, talk premade shit, stalks one's guy in the server if you have their ID (just copy it from dc), and sends some NSFW stuff.

Type /help or !help for some info in discord. For app commands you need to set them up on discord dev site, otherwise only set prefix (`!`) is available.

To start bot you need to get your API_TOKEN from discord dev site, and set up your bot in there.
To play music you need to configure and start Lavalink, set up your java and `application.yml file` and start it with `java -jar Lavalink`. After it started you can start bot with `python bot.py`.

For one certain command you need to get your reddit client id and create app in there.

## Audio
Bot is able to connect, disconnect from your actual voice channel automatically and manually.

`connect` and `disconnect` do exactly what you might think.

You can use `play` and send some string as an argument.

With `playlist` you can check actual song and playlist.

`skip`, `pause`, `resume` is kinda obious.

`stop` stop audio from playing and clear playlist.

`volume` sets volume, `bassboost` sets bass boost, `nightcore` sets 30% higher pitch and 20% higher pace.

## Pics & gifs
This is <span style="color:red;">(NSFW)</span> part, and sometimes has lags. They depend on API and reddit.

`pls` sends tag selected image/gif from `https://nekobot.xyz` API. Tags are listed in `/help pls` and in `help.py` file.
My favorite is tag `food`.

`dicpic` this shit is fire to send on your friend's server. Dic pic is precesilly selected randomly from TOP 100 hot of `r/MassiveCock` subreddit.

## Miscellaneous
There's also `on_voice_state_update` function that detects if that guy with `284580506878869504` ID has connected to the voice channel. If he's in there for
like 60 minutes bot is join him and play some good ass music. This function is kinda buggy, but w/e.

With `on_message` function you can set up bot responses to certain sentences, and there was also plan for doing laundry alarm that would go WEE WOO WEE WOO, but finally I had no time for it.
