# point system
# like everything else in the api

from discord.utils import get, find
from jsonfunc import JF
from discord.ext import commands, tasks
from datetime import datetime
import discord
from humanize import intcomma
import io
import os
import parse_api

PREFIX = "!"
POINTS_FILE = os.getcwd()  + "/points.json"
ROLES_LIST = {"What's Star Wars?": 100, "Star Wars Noob": 500, "Star Wars Rookie": 1000, "Intermidiate Star Wars Enthusiast": 2000, "Star Wars Fanboy": 3000, "Star Wars Sweat": 4500, "Star Wars Master": 6000, "Star Wars Legend": 8000, "Star Wars Jedi": 10000, "Ultimate Star Wars God": 0}
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_guild_join(guild):
    for role in ROLES_LIST.keys():
        await guild.create_role(name=role)
    embd = discord.Embed(title="Server Ready", description="Star Wars Bot has successfully been added to your server!", color=discord.Color.green())
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(embed=embd)

@bot.command()
async def help(ctx, help_page=None):
    if help_page == None:
        embd = discord.Embed(title="Help is on the Way!", color=discord.Color.gold())
        embd.add_field(name=f"`{PREFIX}quiz movies`", value="Get a movie quiz question", inline=False)
        embd.add_field(name=f"`{PREFIX}quiz people`", value="Get a quiz question about a Star Wars character", inline=False)
        embd.add_field(name=f"`{PREFIX}quiz vehicles`", value="Get a vehicle quiz question", inline=False)
        embd.add_field(name=f"`{PREFIX}quiz ships`", value="Get a ship quiz question", inline=False)
        embd.add_field(name=f"`{PREFIX}points`", value="Tells you your current amount of points", inline=False)
        embd.add_field(name=f"`{PREFIX}leaderboard`", value="Shows top 10 players ranked by points and your rank", inline=False)
        embd.add_field(name=f"`{PREFIX}rank`", value="View Star Wars rank levels", inline=False)
        embd.add_field(name=f"`{PREFIX}rank (rank number)`", value=f"Enter `{PREFIX}rank` followed by the number of the rank you want to buy", inline=False)
        embd.set_footer(text="Made by BaconLover, and iLikeCTFs")
        await ctx.channel.send(embed=embd)

@bot.command()
async def quiz(ctx, quiz_type):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me and message.author == ctx.author
    if quiz_type.lower() == "movies":
        data = parse_api.ParseAPI().random_movie()
        point = (1, -2)
        answer = data["title"]
        embd = discord.Embed(title="What movie is this?", description=data["desc"], color=discord.Color.gold())
        await ctx.channel.send(embed=embd)

    elif quiz_type.lower() == "people":
        data = parse_api.ParseAPI().random_person()
        point = (30, -1)
        answer = data["name"]
        embd = discord.Embed(title="Who is this Star Wars character?", color=discord.Color.gold())
        await ctx.channel.send(embed=embd)
        image_file = discord.File(io.BytesIO(data['image_bytes']), filename="guess.png")
        await ctx.send(file=image_file)

    elif quiz_type.lower() == "vehicles":
        data = parse_api.ParseAPI().random_vehicle()
        point = (20, -1)
        answer = data["name"]
        embd = discord.Embed(title="What Star Wars vehicle is this?", color=discord.Color.gold())
        await ctx.channel.send(embed=embd)
        image_file = discord.File(io.BytesIO(data['image_bytes']), filename="guess.png")
        await ctx.send(file=image_file) 

    elif quiz_type.lower() == "ships":
        data = parse_api.ParseAPI().random_ship()
        point = (20, -1)
        answer = data["name"]
        embd = discord.Embed(title="What Star Wars ship is this?", color=discord.Color.gold())
        await ctx.channel.send(embed=embd)
        image_file = discord.File(io.BytesIO(data['image_bytes']), filename="guess.png")
        await ctx.send(file=image_file)

    else:
        embd = discord.Embed(title="Uh-Oh!", description=f"The phrase you entered does not appear to be a command. Use the `{PREFIX}help` command.", color=discord.Color.red())
        await ctx.channel.send(embed=embd)
        return 0
    
    msg = await bot.wait_for('message', check=check)
    if msg.content.lower() == answer.lower():
        embd = discord.Embed(title="Correct!", description=f"Nice one! You got it correct and won `{point[0]}` points.", color=discord.Color.green())
        JF(POINTS_FILE).change_points(str(ctx.author.id), point[0])
        await ctx.channel.send(embed=embd)
    else:
        embd = discord.Embed(title="Close One!", description=f"The correct answer is `{answer}`. You lost `{abs(point[1])}` points.", color=discord.Color.red())
        JF(POINTS_FILE).change_points(str(ctx.author.id), point[1])
        await ctx.channel.send(embed=embd)

@bot.command()
async def points(ctx):
    points = JF(POINTS_FILE).get_points(str(ctx.author.id))
    embd = discord.Embed(title="Your points are...", description=f"`{str(ctx.author)}` currently has `{intcomma(points)}` points", color=discord.Color.gold())
    await ctx.channel.send(embed=embd)

@bot.command()
async def leaderboard(ctx):
    embd = discord.Embed(title="Leaderboard", color=discord.Color.gold())
    file = JF(POINTS_FILE)
    top = file.order()
    places = [":first_place:", ":second_place:", ":third_place:"]
    for person in top[0:10]:
        userid = int(person[0])
        points = file.get_points(userid)
        user = await bot.fetch_user(userid)
        pos = top.index(person)
        if pos in [0, 1, 2]:
            embd.add_field(name=f"{places[pos]}  *{str(user)}*", value=f"Total Points:  {intcomma(points)}", inline=False)
        else:
            embd.add_field(name=f"**#{pos + 1}**  *{str(user)}*", value=f"Total Points:  {intcomma(points)}", inline=False)
    userpos = top.index((str(ctx.author.id), file.get_points(str(ctx.author.id)))) + 1
    embd.set_footer(text=f"{str(ctx.author)} is in #{userpos} place")
    await ctx.channel.send(embed=embd)

@bot.command()
async def rank(ctx, ranknum=None):
    userrank = []
    for role in ctx.author.roles:
        userrank.append(role.name.lower())
    if ranknum == None:
        embd = discord.Embed(title="Star Wars Ranks", color=discord.Color.gold())
        pos = 0
        for key in ROLES_LIST:
            if key == list(ROLES_LIST.keys())[-1]:
                value = "Reserved for #1 Star Wars Fan"
            elif key == list(ROLES_LIST.keys())[-2]:
                value = f"{intcomma(ROLES_LIST.get(key))} points monthly"
            elif key.lower() in userrank:
                value = f"~~{intcomma(ROLES_LIST.get(key))} points~~ *Already purchased*"
            else:
                value = intcomma(ROLES_LIST.get(key)) + " points"
            pos += 1
            embd.add_field(name=f"Rank #{pos}:  **{key}**", value=value, inline=False)
        await ctx.channel.send(embed=embd)
    else:
        if ranknum not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            embd = discord.Embed(title="Uh-Oh!", description="You entered an invalid rank number. Use !rank to see a list of the ranks and their numbers.", color=discord.Color.red())
            await ctx.channel.send(embed=embd)
            return 0
        role = list(ROLES_LIST.keys())[int(ranknum) - 1]
        new = get(ctx.guild.roles, name=role)
        jf = JF(POINTS_FILE)
        if jf.get_points(str(ctx.author.id)) >= abs(ROLES_LIST.get(role)) and role.lower() not in userrank:
            if int(ranknum) in [1, 2, 3, 4, 5, 6, 7, 8]:
                jf.change_points(str(ctx.author.id), -1 * abs(ROLES_LIST.get(role)))
                embd = discord.Embed(title="Success!", description=f"You successfully purchased the `{role}` rank", color=discord.Color.green())
                await ctx.author.add_roles(new)
            elif int(ranknum) == 9:
                embd = discord.Embed(title="Success!", description=f"You successfully purchased the `{role}` rank", color=discord.Color.green())
                jf.change_points(str(ctx.author.id), -1 * ROLES_LIST.get(role))
                await ctx.author.add_roles(new)
            elif int(ranknum) == 10:
                userpos = jf.order().index((str(ctx.author.id), jf.get_points(str(ctx.author.id))))
                if userpos == 0:
                    embd = discord.Embed(title="Success!", description=f"You successfully redeemed the `{role}` rank", color=discord.Color.green())
                    await ctx.author.add_roles(new)
                else:
                    embd = discord.Embed(title="Uh-Oh!", description="To redeem this rank you must be the user with the most points", color=discord.Color.red())
            else:
                pass
            
        else:
            
            embd = discord.Embed(title="Uh-Oh!", description="You either don't have enough points to purchase that rank or have already purchased it", color=discord.Color.red())
        await ctx.channel.send(embed=embd)



if __name__ == '__main__':
    bot.run("")


