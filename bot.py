import pandas as pd
import requests
import tracemalloc
import json

from khl import Bot, Message
from khl.card import CardMessage, Card, Module, Element, Types

tracemalloc.start()

# setup bot and tokens
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

bot = Bot(token=config['token'])


async def getRecent(playerid: str, type: str):
    if type == 'song':
        tableIndex = 3
    elif type == 'course':
        tableIndex = 4
    url = "http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=mypage&playerid=" + playerid
    html = requests.get(url).text
    tables = pd.read_html(html)
    recents = tables[tableIndex]
    recent = recents.loc[0]
    
    song = recent[1]
    status = recent[2]
    playcount = recent[3]
    ranking = recent[4]

    if type == 'song':
        return f"**Song:** {song} \n**Clear Status:** {status} \n**Playcount:** {playcount} \n**Ranking:** {ranking}"
    elif type == 'course':
        return f"**Course:** {song} \n**Clear Status:** {status} \n**Playcount:** {playcount} \n**Ranking:** {ranking}"


@bot.command(name='r')
async def recentSong(msg: Message, playerid: str):
    resmsg = await getRecent(playerid, 'song')

    cm = CardMessage()
    c1 = Card(Module.Header(f"Recent Play for {playerid}"))
    c1.append(Module.Divider())
    c1.append(Module.Section(Element.Text(resmsg)))
    cm.append(c1)
    await msg.reply(cm)


@bot.command(name='c')
async def recentCourse(msg: Message, playerid: str):
    
    resmsg = await getRecent(playerid, 'course')

    cm = CardMessage()
    c1 = Card(Module.Header(f"Recent Course for {playerid}"))
    c1.append(Module.Divider())
    c1.append(Module.Section(Element.Text(resmsg)))
    cm.append(c1)
    await msg.reply(cm)


#ping
@bot.command(name='ping')
async def ping(msg: Message):
    await msg.reply('pong')

bot.run()
