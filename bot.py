import discord
import random
import time
import asyncio
import datetime
import os
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import unquote

load_dotenv()

token = os.getenv('TOKEN')
prefix = '/'

user_agent = 'Mozilla/5.0r'

baseUrl = 'http://air.radiorecord.ru:'

baseHistoryUrl = 'https://history.radiorecord.ru/air/'

current_radio = ''

bitrate = '128'

stations = {
            'record' : baseUrl + '805/rr_' + bitrate,
            'deep' : baseUrl + '805/deep_' + bitrate,
            'rv' : baseUrl + '805/rv_' + bitrate,
            'vesnushka' : baseUrl + '805/deti_' + bitrate,
            'trancehits' : baseUrl + '805/trancehits_' + bitrate,
            '2step' : baseUrl + '805/2step_' + bitrate,
            'tecktonik' : baseUrl + '805/tecktonik_' + bitrate,
            'neurofunk' : baseUrl + '805/neurofunk_' + bitrate,
            'edmhits' : baseUrl + '806/edmhits_' + bitrate,
            'hclassics' : baseUrl + '805/houseclss_' + bitrate,
            'uplifting' : baseUrl + '805/uplift_' + bitrate,
            'darkside' : baseUrl + '805/darkside_' + bitrate,
            'dreamdance' : baseUrl + '805/dream_' + bitrate,
            'bighits' : baseUrl + '805/bighits_' + bitrate,
            'househits' : baseUrl + '805/househits_' + bitrate,
            'progressive' : baseUrl + '805/progr_' + bitrate,
            'synth' : baseUrl + '805/synth_' + bitrate,
            'progressive' : baseUrl + '805/progr_' + bitrate,
            'basshouse' : baseUrl + '805/jackin_' + bitrate,
            'midtempo' : baseUrl + '805/mt_' + bitrate,
            'electro' : baseUrl + '805/elect_' + bitrate,
            'mf' : baseUrl + '805/mf_' + bitrate,
            'innocence' : baseUrl + '805/ibiza_' + bitrate,
            'gold' : baseUrl + '805/gold_' + bitrate,
            'rushits' : baseUrl + '805/russianhits_' + bitrate,
            'groovetribal' : baseUrl + '805/groovetribal_' + bitrate,
            'complextro' : baseUrl + '805/complextro_' + bitrate,
            '1970' : baseUrl + '805/1970_' + bitrate,
            'chillhouse' : baseUrl + '805/chillhouse_' + bitrate,
            '1980' : baseUrl + '805/1980_' + bitrate,
            'cadillac' : baseUrl + '805/cadillac_' + bitrate,
            'rapclassics' : baseUrl + '805/rapclassics_' + bitrate,
            'raphits' : baseUrl + '805/rap_' + bitrate,
            'discofunk' : baseUrl + '805/discofunk_' + bitrate,
            'technopop' : baseUrl + '805/technopop_' + bitrate,
            'eurodance' : baseUrl + '805/eurodance_' + bitrate,
            'rusgold' : baseUrl + '805/russiangold_' + bitrate,
            'drumhits' : baseUrl + '805/drumhits_' + bitrate,
            'liquid' : baseUrl + '805/liquidfunk_' + bitrate,
            'jungle' : baseUrl + '805/jungle_' + bitrate,
            'megamix' : baseUrl + '805/mix_' + bitrate,
            'edm' : baseUrl + '805/club_' + bitrate,
            'tropical' : baseUrl + '805/trop_' + bitrate,
            'goa' : baseUrl + '805/goa_' + bitrate,
            'futureh' : baseUrl + '805/fut_' + bitrate,
            'tm' : baseUrl + '805/tm_' + bitrate,
            'chillout' : baseUrl + '805/chil_' + bitrate,
            'minimal' : baseUrl + '805/mini_' + bitrate,
            'pirate' : baseUrl + '805/ps_' + bitrate,
            'rusmix' : baseUrl + '805/rus_' + bitrate,
            'vip' : baseUrl + '805/vip_' + bitrate,
            'hypno' : baseUrl + '805/hypno_' + bitrate,
            'trancehouse' : baseUrl + '805/trancehouse_' + bitrate,
            'moombahton' : baseUrl + '805/mmbt_' + bitrate,
            'superdisco' : baseUrl + '805/sd90_' + bitrate,
            'breaks' : baseUrl + '805/brks_' + bitrate,
            'dubstep' : baseUrl + '805/dub_' + bitrate,
            'dancecore' : baseUrl + '805/dc_' + bitrate,
            'futureb' : baseUrl + '805/fbass_' + bitrate,
            'remix' : baseUrl + '805/rmx_' + bitrate,
            'techno' : baseUrl + '805/techno_' + bitrate,
            'hardbass' : baseUrl + '805/hbass_' + bitrate,
            'hardstyle' : baseUrl + '805/teo_' + bitrate,
            'trap' : baseUrl + '805/trap_' + bitrate,
            'oschool' : baseUrl + '805/pump_' + bitrate,
            'rock' : baseUrl + '805/rock_' + bitrate,
            'medlyak' : baseUrl + '805/mdl_' + bitrate,
            'symph' : baseUrl + '805/symph_' + bitrate,
            'gop' : baseUrl + '805/gop_' + bitrate,
            'black' : baseUrl + '805/yo_' + bitrate,
            'rave' : baseUrl + '805/rave_' + bitrate,
            'gast' : baseUrl + '805/gast_' + bitrate,
            'ansh' : baseUrl + '805/ansh_' + bitrate,
            'naft' : baseUrl + '805/naft_' + bitrate
            }

hints = 	{
			'record' : 'Radio Record',
			'deep' : 'Deep',
			'rv' : 'Руки Вверх!',
			'vesnushka' : 'Веснушка FM',
			'trancehits' : 'Trance Hits',
			'2step' : '2-step',
			'tecktonik' : 'Tecktonik',
			'neurofunk' : 'Neurofunk',
			'edmhits' : 'EDM Hits',
			'hclassics' : 'House Classics',
			'uplifting' : 'Uplifting',
			'darkside' : 'Darkside',
			'dreamdance' : 'Dream Dance',
			'bighits' : 'Big Hits',
			'househits' : 'House Hits',
			'synth' : 'Synthwave',
			'progressive' : 'Progressive',
			'basshouse' : 'Bass House',
			'midtempo' : 'Midtempo',
			'electro' : 'Electro',
			'mf' : 'Маятник Фуко',
			'innocence' : 'Innocence',
			'gold' : 'Gold',
			'rushits' : 'Russian Hits',
			'groovetribal' : 'Groove/Tribal',
			'complextro' : 'Complextro',
			'1970' : '1970-е',
			'chillhouse' : 'Chill House',
			'1980' : '1980-е',
			'cadillac' : 'Cadillac FM',
			'rapclassics' : 'Rap Classics',
			'raphits' : 'Rap Hits',
			'discofunk' : 'Disco/Funk',
			'technopop' : 'Technopop',
			'eurodance' : 'Eurodance',
			'rusgold' : 'Russian Gold',
			'drumhits' : 'Drum\'n\'Bass Hits',
			'liquid' : 'Liquid Funk',
			'jungle' : 'Jungle',
			'megamix' : 'Megamix',
			'edm' : 'EDM',
			'tropical' : 'Tropical',
			'goa' : 'GOA/PSY',
			'futureh' : 'Future House',
			'tm' : 'Trancemission',
			'chillout' : 'Chill-Out',
			'minimal' : 'Minimal/Tech',
			'pirate' : 'Pirate Station',
			'rusmix' : 'Russian Mix',
			'vip' : 'Vip House',
			'hypno' : 'Hypnotic',
			'trancehouse' : 'Trancehouse',
			'moombahton' : 'Moombahton',
			'superdisco' : 'Супердискотека 90-х',
			'breaks' : 'Breaks',
			'dubstep' : 'Dubstep',
			'dancecore' : 'Dancecore',
			'futureb' : 'Future Bass',
			'remix' : 'Remix',
			'techno' : 'Techno',
			'hardbass' : 'Hard Bass',
			'hardstyle' : 'Hard Style',
			'trap' : 'Trap',
			'oschool' : 'Old School',
			'rock' : 'Rock',
			'medlyak' : 'Медляк FM',
			'symph' : 'Симфония FM',
			'gop' : 'Гоп ФМ',
			'black' : 'Black',
			'rave': 'Rave FM',
			'gast' : 'Гастарбайтер FM',
			'ansh' : 'Аншлаг FM',
			'naft' : 'Нафталин FM'
 			}

commands = {
			'/radiohelp, /rh' : 'Вывод списка команд для радио и текущий битрейт',
			'/play, /p' : 'Играть радио (параметр - название радио)',
			'/radio, /r' : 'Показать текущее радио',
			'/stop, /s' : 'Остановить радио',
			'/song' : 'Показать текущую песню'
			}

client = Bot(command_prefix=prefix)

def parse_song_href(s):
	s = s.__str__()
	i = s.find('<')
	j = s.find('>')
	s = unquote(s[i+1:j])
	i = s.find('"')
	j = s.rfind('"')
	s = s[i+1:j]
	return (s[:s.find('-')].strip(), s[s.find('-')+1:s.find('.mp3')].strip())

def get_radio_url_name(s):
	i = [pos for pos, char in enumerate(s) if char == '/'][-1]
	j = [pos for pos, char in enumerate(s) if char == '_'][-1]
	return s[i+1:j]

def get_air_url(s):
	uname = get_radio_url_name(stations[s])
	return baseHistoryUrl + uname + '/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'

def get_url(x):
    if x == 'random':
    	return random.choice(list(stations.values()))
    elif x == '':
        return stations['record']
    else:
        return stations.get(x)

@client.event
async def on_ready():
    print('Bot Ready')

@client.command(aliases=['rh', 'rhelp'])
async def radiohelp(ctx):
	help = 'Список доступных радио:\n'
	for i, key in enumerate(stations):
		help += f'{i+1}. {key} ({hints[key]})\n'
	help += f'\nБитрейт: {bitrate}'
	await ctx.send(help)

@client.command(aliases=['cmd'])
async def command(ctx):
	cmd = ''
	for key, value in commands.items():
		cmd += f'{key} - {value}\n'
	await ctx.send(cmd)

@client.command(aliases=['p'])
async def play(ctx, arg = ''):
    channel = ctx.message.author.voice.channel
    radio = get_url(arg)

    if not radio:
    	await ctx.send(f'Нет такого радио :(')
    	return

    global player
    try:
    	player = await channel.connect()
    except:
    	pass
    player.play(FFmpegPCMAudio(radio))
    for key, value in stations.items():
	    if value == radio:
	    	global current_radio
	    	current_radio = key
    await ctx.send(f'Radio: {hints[current_radio]}')

@client.command(aliases=['s'])
async def stop(ctx):
    player.stop()

@client.command(aliases=['r'])
async def radio(ctx):
	await ctx.send(hints[current_radio])

@client.command(aliases=['currentsong', 'song', 'cs'])
async def cursong(ctx, parse = ''):
	url = get_air_url(current_radio) 
	req = Request(url, headers={'User-Agent' : user_agent})
	page = urlopen(req).read()
	soup = BeautifulSoup(page, 'lxml')
	hrefs = soup.find_all('a', href=True)
	if parse == 'noparse':
		song = hrefs[-1]
		await ctx.send(song)
	else:
		song = parse_song_href(hrefs[-1])
		await ctx.send(f'Время начала песни: {song[0]}\nНазвание песни: {song[1]}')
client.run(token)