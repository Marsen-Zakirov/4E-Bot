import discord # импортируем Дискорд
from discord.ext import commands
import os
from time import sleep
import requests
from PIL import Image, ImageFont, ImageDraw
import io
import asyncio
import sqlite3
bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
@bot.event            # Проверка запуска бота
async def on_ready():
    print('Бот готов к работе')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT ,
        cash BIGINT,
        lvl INT 
    )''')
    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 1)")
            else:
                pass
    connection.commit()
@bot.event
async def on_raw_reaction_add(playload):
    message_id = playload.message_id
    if message_id == 816300677394595860:
        guild_id = playload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        if playload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles,name = 'Counter-Strike: Global Offensive')
        elif playload.emoji.name == 'dota':
            role = discord.utils.get(guild.roles,name = 'Dota 2')
        elif playload.emoji.name == 'PUBG':
            role = discord.utils.get(guild.roles,name = 'PUBG')
        elif playload.emoji.name == 'GTA':
            role = discord.utils.get(guild.roles,name = 'GTA')
        elif playload.emoji.name == 'rust':
            role = discord.utils.get(guild.roles,name = 'Rust')
        elif playload.emoji.name == 'minecraft':
            role = discord.utils.get(guild.roles,name = 'Minecraft')
        else:
            role = discord.utils.get(guild.roles, name=playload.emoji.name)
        if role is not None:
            member = discord.utils.find(lambda  m : m.id == playload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                print('Пользователь не найден')
        else:
            print('Роль не найден')
@bot.event
async def on_raw_reaction_remove(playload):
    message_id = playload.message_id
    if message_id == 816300677394595860:
        guild_id = playload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        if playload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles,name = 'Counter-Strike: Global Offensive')
        elif playload.emoji.name == 'dota':
            role = discord.utils.get(guild.roles,name = 'Dota 2')
        elif playload.emoji.name == 'PUBG':
            role = discord.utils.get(guild.roles,name = 'PUBG')
        elif playload.emoji.name == 'GTA':
            role = discord.utils.get(guild.roles,name = 'GTA')
        elif playload.emoji.name == 'rust':
            role = discord.utils.get(guild.roles,name = 'Rust')
        elif playload.emoji.name == 'minecraft':
            role = discord.utils.get(guild.roles,name = 'Minecraft')
        else:
            role = discord.utils.get(guild.roles, name=playload.emoji.name)
        if role is not None:
            member = discord.utils.find(lambda  m : m.id == playload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            else:
                print('Пользователь не найден')
        else:
            print('Роль не найден')
@bot.command() # кик игроков
@commands.has_permissions(administrator = True)
async def kick (ctx,member:discord.Member,*,reason = None):
    await member.kick(reason=reason)
@bot.command() # Бан игроков
async def ban(ctx,member:discord.Member,*,reason = None):
    await member.ban(reason=reason)
@bot.command() # mute игроков
@commands.has_permissions(administrator = True)
async def mute(ctx,member:discord.Member):
    await ctx.channel.purge(limit=1)
    mute = discord.utils.get(ctx.message.guild.roles, name = 'mute')
    await member.add_roles(mute)
    await ctx.send(f'{member.mention} Замучен')
    await asyncio.sleep(1800)
    await member.remove_roles(mute)

@bot.command(aliases = ['card','profile','lvl']) #карточка юзера
async def card_user(ctx):
    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar_url)

    response = requests.get(url, stream=True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)

    img.paste(response, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator

    headline = ImageFont.truetype('arial.ttf', size=20)
    undertext = ImageFont.truetype('arial.ttf', size=12)

    idraw.text((145, 15), f'{name}#{tag}', font=headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font=undertext)

    img.save('user_card.png')

    await ctx.send(file=discord.File(fp='user_card.png')) # #      ##
connection = sqlite3.connect('server,db')
cursor = connection.cursor()
@bot.event # дополнение к базам данных
async  def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES('{member}', {member.id},0,1)")
        connection.commit()
    else:
        pass
    role = discord.utils.get(member.guild.roles, name = 'Участник')
    channel = bot.get_channel(815555356662956032)
    embed = discord.Embed(description=f"Привет {member.mention}, добро пожаловать в наш сервер" , color=0x0bf9f9 )
    await member.add_roles(role)
    await channel.send(embed = embed)
    print('Member joined')
@bot.command(aliases = ['balance','cash','money']) # проверка баланса
async def __balance(ctx,member:discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}  :moneybag:**"""
        ))
    else:
        pass
@bot.command(aliases = ['give']) # выдавать деньги
async def __award(ctx,member:discord.Member = None,amount:int=None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, Вы забыли указать, кого желаете наградить")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, Вы забыли указать сумму")
        elif amount < 0:
            await ctx.send(f"**{ctx.author}**, Эмм, вообще то так нельзя")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount,member.id))
            connection.commit()
            await ctx.message.add_reaction('✅')
        await ctx.send(embed=discord.Embed(description=f"""**{member}**, поздравляем, вас наградили, в настоящее время ваш баланс составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}  :moneybag:**"""))
@bot.command(aliases = ['collect']) #отбирать деньги
async def __colect(ctx,member:discord.Member = None, amount = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, Вы забыли указать, у кого желаете отнять деньги")
    else:
        if amount == 'all':
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connection.commit()
            await ctx.send(embed=discord.Embed(
                description=f"""**{member}**, к сожалению у вас забрали все деньги 😭"""))
            await ctx.message.add_reaction('✅')
        elif amount is None:
            await ctx.send(f"**{ctx.author}**, Вы забыли указать сумму")
        elif int(amount) < 0:
            await ctx.send(f"**{ctx.author}**, Эмм, вообще то так нельзя")
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount),member.id))
            connection.commit()
            await ctx.message.add_reaction('✅')
            await ctx.send(embed=discord.Embed(description=f"""**{member}**, к сожалению у вас забрали деньги, в настоящее время ваш баланс составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}  :moneybag:**"""))





token = os.environ.get('BOT_TOKEN')





bot.run(token)