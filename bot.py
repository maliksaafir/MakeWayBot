# bot.py
import aiohttp
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')


@bot.command(name='post', help='Creates a new post!')
async def post(ctx, user_name: str, title: str, caption: str = None, ):
    await ctx.send(f'received data: {user_name}, {title}, {caption}')
    data = {
        'creator': user_name,
        'caption': caption,
        'title': title
        }

    async with aiohttp.ClientSession() as session:
        await ctx.send('sending post...')
        async with session.post('https://makeway.herokuapp.com/posts/',
                                json=data) as r:
            if r.status == 201:
                print('got a 201 code!')
                await ctx.send('posted successfully!!')
            elif r.status == 409:
                print('got a 409 code :(')
                await ctx.send(f'failed :(\nerror message: {await r.text()}')


bot.run(TOKEN)
