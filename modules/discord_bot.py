import discord
from discord.ext import tasks
import json
import modules.spotify as spotify
import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    await check_insta.start()

@tasks.loop(seconds=5)
async def check_insta():

    if datetime.now().minute == 44:
        log = json.loads(open(f'{os.getenv('INSTA_TARGET')}-data/log.json').read())
        if log['hourly log'] != "":
            await bot.get_channel(int(os.getenv('DISCORD_CHANNEL'))).send(log['hourly log'])
            log['hourly log'] = ""
            with open(f'{os.getenv('INSTA_TARGET')}-data/log.json', 'w') as f:
                f.write(json.dumps(log, indent=4))

    if not os.path.exists(f'{os.getenv("INSTA_TARGET")}-data/log.json'):
        return
    
    data = json.loads(open(f'{os.getenv("INSTA_TARGET")}-data/log.json').read())

    if data['read'] == False:
        if data['log'] == "":
            return

        print("[+] New insta data found, sending to discord...")
        await bot.get_channel(int(os.getenv('DISCORD_CHANNEL'))).send("Activity in the past hour:", data['log'])
        data['read'] = True
        data['log'] = ""
        with open(f'{os.getenv('INSTA_TARGET')}-data/log.json', 'w') as f:
            f.write(json.dumps(data, indent=4))

    if os.path.exists('stories'):
        print("[+] New insta story found, sending to discord...")
        
        for story in os.listdir('stories'):
            splitext = os.path.splitext(story)
            if '.jpg' in splitext or '.mp4' in splitext:
                await bot.get_channel(int(os.getenv('DISCORD_CHANNEL'))).send(file=discord.File(f'stories/{story}'))
            
            os.remove(f'stories/{story}')

        os.rmdir('stories')


def run():
    bot.run(TOKEN)