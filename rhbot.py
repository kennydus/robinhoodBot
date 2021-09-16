import discord
import requests
import bs4
from discord.ext import commands
from discord.ext import tasks

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('!rhhelp'))
    #doge_reminder.start()
    print('Robinhood Bot is ready.')

@client.command()
async def rhhelp(ctx):
    embed = discord.Embed(
        title = 'Robinhood Bot Commands',
        description = "Here's a list of the available commands for the Robinhood Bot.",
        colour = discord.Colour.green()
    )
    embed.add_field(name='!rhhelp', value="Displays all commands for the Robinhood Bot.", inline=False)
    embed.add_field(name='!fall [stock] [price]', value="Sends an alert when the given stock falls to the given price.", inline=False)
    embed.add_field(name='!rise [stock] [price]', value="Sends an alert when the given stock rises to the given price.", inline=False)
    embed.add_field(name='!price [stock]', value="Gives the current price of a stock.", inline=False)
    embed.add_field(name='!doge', value='Gives the current price of Dogecoin.', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def fall(ctx, stock, price):
    url = "https://finance.yahoo.com/quote/"
    full_url = url + stock
    response = requests.get(full_url).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    stock_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    await ctx.send(f"Limit notification set! The current price of **{stock.upper()}** is **${stock_price}**. You'll be notified when **{stock.upper()}** falls below **${price}**.")
    while True:
        response = requests.get(full_url).content
        soup = bs4.BeautifulSoup(response, 'html.parser')
        stock_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
        if stock_price < price:
            await ctx.send(f":exclamation: ALERT :exclamation: **{stock.upper()}** has dropped below **${price}**! {ctx.message.author.mention}")
            await ctx.send(f"**{stock.upper()}** is now at **${stock_price}**.")
            break

@client.command()
async def rise(ctx, stock, price):
    url = "https://finance.yahoo.com/quote/"
    full_url = url + stock
    response = requests.get(full_url).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    stock_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    await ctx.send(f"Limit notification set! The current price of **{stock.upper()}** is **${stock_price}**. You'll be notified when **{stock.upper()}** rises above **${price}**.")
    while True:
        response = requests.get(full_url).content
        soup = bs4.BeautifulSoup(response, 'html.parser')
        stock_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
        if stock_price > price:
            await ctx.send(f":exclamation: ALERT :exclamation: **{stock.upper()}** has risen above **${price}**! {ctx.message.author.mention}")
            await ctx.send(f"**{stock.upper()}** is now at **${stock_price}**.")
            break

@client.command()
async def price(ctx, *, stock):
    url = "https://finance.yahoo.com/quote/"
    full_url = url + stock
    response = requests.get(full_url).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    stock_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    await ctx.send(f"The current price of **{stock.upper()}** is **${stock_price}**.")

@client.command()
async def doge(ctx):
    doge_coin_url = 'https://finance.yahoo.com/quote/DOGE-USD/'
    response = requests.get(doge_coin_url).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    doge_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    await ctx.send(f"The current price of **DOGECOIN** is **${doge_price}**.")

#@tasks.loop(hours=6)
#async def doge_reminder():
#    doge_coin_url = 'https://finance.yahoo.com/quote/DOGE-USD/'
#    response = requests.get(doge_coin_url).content
#    soup = bs4.BeautifulSoup(response, 'html.parser')
#    doge_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
#    channel = client.get_channel(804319842836152360)
#    await channel.send(f"The current price of **DOGECOIN** is **${doge_price}**.")

@client.command()
async def dogedown(ctx, price):
    doge_coin_url = 'https://finance.yahoo.com/quote/DOGE-USD/'
    response = requests.get(doge_coin_url).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    doge_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    if doge_price <= price:
        await ctx.send('**Error**: The current price of **DOGECOIN** is already lower than the price you input.')
    else:
        await ctx.send(f"Limit notification set! **DOGECOIN** is currently **${doge_price}**. You'll be notified when **DOGECOIN** falls below **${price}**.")
        while True:
            response = requests.get(doge_coin_url).content
            soup = bs4.BeautifulSoup(response, 'html.parser')
            doge_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
            if doge_price < price:
                await ctx.send(f"**:exclamation: ALERT :exclamation: DOGECOIN has dropped below ${price}! {ctx.message.author.mention}**")
                await ctx.send(f"**:exclamation: ALERT :exclamation: DOGECOIN has dropped below ${price}! {ctx.message.author.mention}**")
                await ctx.send(f"**:exclamation: ALERT :exclamation: DOGECOIN has dropped below ${price}! {ctx.message.author.mention}**")
                await ctx.send(f"**DOGECOIN** is **${doge_price}**!")
                break

@client.command()
async def dogeup(ctx, price):
    doge_coin_url = 'https://finance.yahoo.com/quote/DOGE-USD/'
    response = requests.get(doge_coin_url).content
    soup = bs4.BeautifulSoup(response, 'html.parser')
    doge_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    if doge_price >= price:
        await ctx.send('**Error**: The current price of **DOGECOIN** is already higher than the price you input.')
    else:
        await ctx.send(f"Limit notification set! **DOGECOIN** is currently **${doge_price}**. You'll be notified when **DOGECOIN** rises above **${price}**.")
        while True:
            response = requests.get(doge_coin_url).content
            soup = bs4.BeautifulSoup(response, 'html.parser')
            doge_price = soup.find("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
            if doge_price > price:
                await ctx.send(f"**:exclamation: ALERT :exclamation: DOGECOIN has risen above ${price}! {ctx.message.author.mention}**")
                await ctx.send(f"**:exclamation: ALERT :exclamation: DOGECOIN has risen above ${price}! {ctx.message.author.mention}**")
                await ctx.send(f"**:exclamation: ALERT :exclamation: DOGECOIN has risen above ${price}! {ctx.message.author.mention}**")
                await ctx.send(f"**DOGECOIN** is **${doge_price}**!")
                break
    
