import discord # импортируем Дискорд
from discord.ext import commands
from discord import Intents
import asyncio
import os
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = "!",intents = intents)    # ! это вызов бота
@bot.event            # Проверка запуска бота
async def on_ready():
    print('4E')
@bot.event # Выдача роли Участник, и приветсвие игроков
async def on_member_join(member:discord.Member):
    role = discord.utils.get(member.guild.roles, name = 'Участник')
    channel = bot.get_channel(815555356662956032)
    embed = discord.Embed(description=f"Привет {member.mention}, добро пожаловать в наш сервер" , color=0x0bf9f9 )
    await member.add_roles(role)
    await channel.send(embed = embed)
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

token = os.environ.get('BOT_TOKEN')








bot.run(token)
