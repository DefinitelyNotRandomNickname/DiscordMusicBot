import pandas as pd

tags = ['4k', 'hentai', 'hass', 'ass', 'neko', 'hneko', 'hkitsune', 'anal', 'hanal', 'pussy', 'food', 'tentacle', 'boobs', 'hboobs', 'pgif']

Commands_available = pd.DataFrame({
		(
		'aHelp',
		'help [Optional argument]',
		'Show available commands',
		'Show available commands'
		),

		(
		'bVoice',
		'connect',
		'Yeah, guess what this shit can do',
		'Yeah, guess what this shit can do'
		),

		(
		'bVoice',
		'disconnect',
		'🤔',
		'🤔'
		),

		(
		'bVoice',
		'play [url/name]',
		'Playing yt audio from searching, URLs, and playlist',
		'Playing yt audio from searching, URLs, and playlist'
		),

		(
		'bVoice',
		'playlist',
		'Spits out actual playlist',
		'Spits out actual playlist'
		),

		(
		'bVoice',
		'skip',
		'Skips actual song',
		'Skips actual song'
		),

		(
		'bVoice',
		'pause',
		'Pause audio',
		'Pause audio'
		),

		(
		'bVoice',
		'resume',
		'Resumes audio',
		'Resumes audio'
		),

		(
		'bVoice',
		'stop',
		'Stop and clear playlist',
		'Stop and clear playlist'
		),

		(
		'cDJ',
		'volume [0-1000]',
		'Sets audio volume from 0 to 1000',
		'Sets audio volume from 0 to 1000'
		),

		(
		'cDJ',
		'bassboost [0-100]',
		'Sets audio bassboost, from 0 to 100',
		'Sets audio bassboost, from 0 to 100'
		),

		(
		'cDJ',
		'nightcore',
		'~( ˘▾˘~)♡♫♩♬',
		'~( ˘▾˘~)♡♫♩♬'
		),

		(
		'dMisc',
		'dicpic',
		'Sends dic pic',
		'Hot dic pic is beeing selected randomly from top 100 of r/MassiveCock'
		),

		(
		'dMisc',
		'pls [tag]',
		'Sends pic or gif based on selected tag',
		'Available tags: ' + ', '.join(tags) 
		),
}, columns=['category', 'name', 'description', 'detailed description'])