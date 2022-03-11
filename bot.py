# bot.py

import os, random, discord, pandas as pd, numpy as np, matplotlib.pyplot as plt
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

flag : int = 0
counter : int = 0
word_counter = [''][0]
toggle_c : bool = False
toggle_r : bool = False
text_log : str = ""

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Welcome To Python Project Server!'
    )



@bot.command(name = 'chat', help='- Toggles Chat Bot')
async def toggle_chat(ctx):
    global toggle_c
    if toggle_c == False:
        toggle_c = True
        response ='Chat Mode Turned On'
    else:
        toggle_c = False
        response = 'Chat Mode Turned Off'
    await ctx.send(response)
    
@bot.command(name = 'reader', help='- Toggles Bot To Read & Save Texts')
async def toggle_read(ctx):
    global toggle_r
    if toggle_r == False:
        toggle_r = True
        response ='Read Mode Turned On'
    else:
        toggle_r = False
        response = 'Read Mode Turned Off'
    await ctx.send(response)
    
@bot.command(name = 'list', help='- Provides List of Members')
async def member_list(ctx):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
        
    members = '\n - '.join([member.name for member in guild.members])
    response = f'Server Members:\n - {members}'
    await ctx.send(response)

@bot.command(name = 'plotWords', help="- Shows Server's Used Words Graph")
async def plot_graph(ctx):
    df = pd.read_csv('words.csv')
    x = df['Word'].values
    y = df['Count'].values
    image = discord.File("words.png")
    f = plt.figure()
    f.set_figwidth(12)
    f.set_figheight(10)
    plt.xlabel('Word Count')
    plt.ylabel('Words')
    plt.bar(x,y)
    plt.xticks(rotation=90)
    plt.savefig("words.png")
    plt.close()
    await ctx.send(file=image)

@bot.event
async def on_message(message):
    global toggle_c, toggle_r, text_log, counter, flag
    
#Chat Logger
    time = datetime.now()
    c_time = time.strftime("[%H:%M]")
    text_log = message.content    
    logger = open("chatLog.txt", "a")
    logger.write(f'{message.author.name}'+ c_time +' - ' + text_log)
    logger.write("\n")
    logger.close()



#User Checker
    if message.author == bot.user:
        return

#Word Listing
    if toggle_r == True:
        for item in message.content.lower().split():
            if not os.path.isfile('words.csv'):
                listing = pd.DataFrame([[item,1]], columns=['Word','Count'])
                listing.to_csv('words.csv',mode='a', index=False)
            else:
                df = pd.read_csv('words.csv', usecols=['Word','Count'])
                for word in df["Word"]:
                    if item == word:
                        count = df.iloc[counter,1]
                        df.at[counter,'Count'] = count+1
                        df.to_csv('words.csv',mode='w',index=False)
                        flag=1
                    counter = counter+1
                        
                counter = 0   
                if flag==0:
                    listing = pd.DataFrame([[item,1]])
                    listing.to_csv('words.csv',mode='a',index=False,header=False)
                flag=0
                    
#Chat Service
    if toggle_c == True:
        if message.author.nick == None:
            welcome_quotes = [
                f'Hello {message.author.name}, why are you wandering without a nickname',
                f'Hi {message.author.name}, where is your nickname?',
                f"What's Up {message.author.name}! get yourself a nickname"
            ]
        else:
            welcome_quotes = [
                f'Hello {message.author.nick}',
                f'Hi {message.author.nick}',
                f"What's Up {message.author.nick}"
            ]
    
        if message.content.lower() in ['hello','hi']:
            response = random.choice(welcome_quotes)
            await message.channel.send(response)
    
    
    
    await bot.process_commands(message)

bot.run(TOKEN)