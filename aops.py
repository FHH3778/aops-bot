import discord
from discord.ext import commands, tasks
from random import random, randint, choice

client = commands.Bot(command_prefix='aops ', case_insensitive=True, intents=all)
import mysql.connector
import datetime
import asyncio
from discord.ext.commands import has_permissions
users = []

heist_timer = 0
joinmsg = None
heist_channel = None
connection = mysql.connector.connect(
    host="localhost",
    user="discord_dev",
    password="29XpiD$3",
    database="discord"
)


@client.event
async def on_ready():
    mycursor = connection.cursor()
    for guild in client.guilds:
        print(guild.id)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        mycursor.execute("SELECT member_id FROM discord.aops")
        userIds = [*map(lambda x: x[0], mycursor.fetchall())]
        print(userIds)
        print(len(guild.members))
        for member in guild.members:
            insert_sql = "INSERT INTO aops (member_id, member_name, wallet, bank) VALUES (%s, %s, %s, %s)"
            sql = "select * from discord_account where user_id={}".format(member.id)
            print(member.id)
            if int(member.id) not in userIds:
                val = (int(member.id), member.name, 400, 100)
                mycursor.execute(insert_sql, val)
                connection.commit()
        await client.change_presence(
            activity=discord.Game(
                "Watching over {} humans in the Mathematicians of AoPS.".format(int(len(guild.members)) - 10)))
    mycursor.close()

def check(m, n):
    return m == n

"""Join and leave messages"""


@client.event
async def on_member_join(member):
    try:
        a = discord.utils.get(member.guild.channels, id=768221496430428181)
        await member.send(
            f'Welcome to the Mathematicians of AoPS! Make sure to check out {a.mention} to verify yourself!\n**WHAT WE HAVE**\n- :RudolfMewtwobest: Mewbot spawn areas, gyms, and tournaments! :RudolfMewtwobest:\n- :Myuu: Myuu areas! :Myuu:\n- A Pokemon Showdown League!\n- Giveaways!\n- Other fun bots such as Dank Memer!\n- Friendly members and staff!\n- And much, much, more!')
    except:
        pass
    members = 0
    bots = 0
    for member in member.guild.members:
        if not member.bot:
            members += 1
        else:
            bots += 1
    n = int(time.time() - member.created_at.timestamp())
    year = n // (365 * 24 * 3600)
    n = n % (365 * 24 * 3600)
    day = n // (24 * 3600)

    n = n % (24 * 3600)
    hour = n // 3600

    n %= 3600
    minutes = n // 60

    n %= 60
    seconds = n
    if year > 0:
        embed = discord.Embed(title=f"Welcome {member}!",
                              description=f"{member.mention} just joined Pokemon Community. \nWelcome to our server! \nWe now have {members} people and {bots} bots!\n This account is {year} years, {day} days, {hour} hours, {minutes} minutes, and {n} seconds old.")
    elif day > 0:
        embed = discord.Embed(title=f"Welcome {member}!",
                              description=f"{member.mention} just joined Pokemon Community. \nWelcome to our server! \nWe now have {members} people and {bots} bots!\nThis account is {day} days, {hour} hours, {minutes} minutes, and {n} seconds old.")
    elif hour > 0:
        embed = discord.Embed(title=f"Welcome {member}!",
                              description=f"{member.mention} just joined Pokemon Community. \nWelcome to our server! \nWe now have {members} people and {bots} bots!\n:warning: **NEW ACCOUNT** :warning:This account is {hour} hours, {minutes} minutes, and {n} seconds old.")
    elif minutes > 0:
        embed = discord.Embed(title=f"Welcome {member}!",
                              description=f"{member.mention} just joined Pokemon Community. \nWelcome to our server! \nWe now have {members} people and {bots} bots!\n:warning: **NEW ACCOUNT** :warning:This account is {minutes} minutes, and {n} seconds old.")
    else:
        embed = discord.Embed(title=f"Welcome {member}!",
                              description=f"{member.mention} just joined Pokemon Community. \nWelcome to our server! \nWe now have {members} people and {bots} bots!\n:warning: **NEW ACCOUNT** :warning:This account is {n} seconds old.")
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    channel = discord.utils.get(member.guild.channels, id=745752044329107469)

    await channel.send(embed=embed)

# @client.event
# async def on_member_join(member):
#     channel = await member.create_dm()
#     await channel.send(f"{member.mention}, welcome to the biggest AoPS Discord server of them all! We currently have {len(member.guild.members)} members!")
#     await channel.send("**THINGS TO DO!**")
#     a = discord.utils.get(member.guild.channels, 749347092325072997)
#     await channel.send(f"Check {a.mention} for the rules and to get access to the rest of this server!")
# @client.event
# async def on_member_join(member):
#     embed = discord.Embed(title="Welcome",
#                           description=f"{member.mention} Just Joined \nWelcome to our server :partying_face: \nYou are member number {len(list(member.guild.members))}!")
#     embed.timestamp = datetime.datetime.utcnow()
#     embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
#     embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
#     embed.set_thumbnail(url=f"{member.avatar_url}")
#     channel = client.get_channel(id=749349890118778962)
#     await channel.send(embed=embed)
@client.event
async def on_message(message):
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM aops WHERE member_id={}".format(int(message.author.id)))
    myres = mycursor.fetchone()
    mycursor.execute("SELECT * FROM potd order by problem_id desc limit 1".format(int(message.author.id)))
    myres2 = mycursor.fetchone()
    print(message.channel.id, heist_channel)
    print(message.content)

    print(message.content, joinmsg)
    try:
        if int(message.channel.id) == int(heist_channel) and message.content.upper() == joinmsg.upper():
            print('oof')
            if message.author not in users:
                users.append(message.author)
                await message.channel.send(f"**{message.author.name}** has joined the heist! You still have **{heist_timer}** seconds left to join!")
            else:
                await message.channel.send(
                    f"**{message.author.name}** has already joined the heist!! You still have **{heist_timer}** seconds left to join!")
            print(users)
    except:
        pass
    if message.guild == None and not message.author.bot:
        channel = client.get_channel(819704671639830538)
        await message.channel.send("%s, your message has been received! We will respond ASAP!" % message.author)
        embed = discord.Embed(title="Modmail by {}".format(message.author),
                              description="{}".format(message.content))
        await channel.send(embed=embed)
    else:
        # if int(myres[4]) == 1:
        #     if str(message.content) == str(myres2[0]):
        #         await message.channel.send(f"{message.author.mention}, congratulations, you solved the POTD!")
        #         await message.delete()
        #     else:
        #         await message.channel.send(f"{message.author.mention}, that is the wrong answer! Try again!")
        # mycursor.execute("UPDATE aops SET wallet={} WHERE member_id={}".format(int(myres[2]) + 2, int(message.author.id)))
        # connection.commit()
        await client.process_commands(message)


@client.command(help='Request a random AMC8 problem!')
async def amc8(ctx):
    link = "https://artofproblemsolving.com/wiki/index.php/" + str(
        randint(1999, 2020)) + "_AMC_8_Problems/Problem_" + str(randint(1, 26))
    await ctx.channel.send(link)


@client.command(help='Request a random AMC10 problem!')
async def amc10(ctx):
    if randint(1, 3) == 1:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(
            randint(2002, 2020)) + "_AMC_10A_Problems/Problem_" + str(randint(1, 26))
    else:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(
            randint(2002, 2020)) + "_AMC_10B_Problems/Problem_" + str(randint(1, 26))
    await ctx.channel.send(link)


@client.command(help='Request a random AMC12 problem!')
async def amc12(ctx):
    if randint(1, 3) == 1:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(
            randint(2002, 2020)) + "_AMC_12A_Problems/Problem_" + str(randint(1, 26))
    else:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(
            randint(2002, 2020)) + "_AMC_12B_Problems/Problem_" + str(randint(1, 26))
    await ctx.channel.send(link)


@client.command(help='Request a random AIME problem!')
async def aime(ctx):
    a = randint(1983, 2021)
    if a < 2000:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(a) + "_AIME_Problems/Problem_" + str(
            randint(1, 15))
    else:
        if randint(1, 3) == 1:
            link = "https://artofproblemsolving.com/wiki/index.php/" + str(a) + "_AIME_I_Problems/Problem_" + str(
                randint(1, 15))
        else:
            link = "https://artofproblemsolving.com/wiki/index.php/" + str(a) + "_AIME_II_Problems/Problem_" + str(
                randint(1, 15))
    await ctx.channel.send(link)


@client.command(help='Request a random USAJMO problem! Good luck...')
async def usajmo(ctx):
    link = "https://artofproblemsolving.com/wiki/index.php/" + str(
        randint(2010, 2019)) + "_USAJMO_Problems/Problem_" + str(randint(1, 6))
    await ctx.channel.send(link)


@client.command(help='Request a random USAMO problem! Good luck...')
async def usamo(ctx):
    a = randint(1983, 2019)
    if a < 1996:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(a) + "_USAMO_Problems/Problem_" + str(
            randint(1, 5))
    else:
        link = "https://artofproblemsolving.com/wiki/index.php/" + str(a) + "_USAMO_Problems/Problem_" + str(
            randint(1, 6))
    await ctx.channel.send(link)


@client.command(aliases=['bal'], help='Check your balance!')
async def balance(ctx, *, member: discord.Member = None):
    mycursor = connection.cursor()
    if member:
        mycursor.execute("SELECT * FROM aops WHERE member_id={}".format(int(member.id)))
        myresult = mycursor.fetchone()
        l = []
        l.append("Cash: %d" % myresult[2])
        l.append("Bank: %d" % myresult[3])
        l.append("Total: %d" % int(int(myresult[2]) + int(myresult[3])))
        user = member

        embed = discord.Embed(title="{}'s balance".format(user.name),
                              description="{}".format('\n'.join(l)))
        await ctx.channel.send(embed=embed)
    else:
        mycursor.execute("SELECT * FROM aops WHERE member_id={}".format(int(ctx.message.author.id)))
        myresult = mycursor.fetchone()
        l = []
        l.append("Cash: %d" % myresult[2])
        l.append("Bank: %d" % myresult[3])
        l.append("Total: %d" % int(int(myresult[2]) + int(myresult[3])))
        user = ctx.message.author

        embed = discord.Embed(title="{}'s balance".format(user.name),
                              description="{}".format('\n'.join(l)))
        await ctx.channel.send(embed=embed)
    mycursor.close()


@client.command(aliases=['heist', 'bankheist'],
                help="Heist someone's bank with a team! There is a greater chance of success with more people!")
async def bankrob(ctx, *, member: discord.Member):
    global heist_timer
    mycursor = connection.cursor()
    mycursor.execute('SELECT wallet FROM aops WHERE member_id={}'.format(ctx.message.author.id))
    robber = mycursor.fetchone()
    print(robber)
    if member.id != ctx.message.author.id:
        if int(robber[0]) >= 2500:
            mycursor.execute('SELECT bank FROM aops WHERE member_id={}'.format(member.id))
            victim = int(mycursor.fetchone()[0])
            print(victim)
            if int(victim) >= 2500:
                global heist_channel
                global users
                global joinmsg
                heist_channel = ctx.channel.id
                heist_timer = 60
                users = [ctx.message.author]
                joinmsg = choice(['GIMME THOSE CUBES', 'JOIN HEIST', 'ROB THE BANK'])
                await ctx.channel.send(embed=discord.Embed(title=':moneybag: Bankrob time!',
                                                           description=f'**{ctx.author.name}** is trying to bankrob **{member.name}**!\n\nType `{joinmsg.upper()}` to join them!'))
                await ubankrob()
                while heist_timer > 0:
                    pass
            else:
                await ctx.channel.send(
                    f"{ctx.message.author.mention}, the bank you are trying to heist has less than 2500 cubes in it! It's not worth it!")
        else:
            await ctx.channel.send(f"{ctx.message.author.mention}, you need 2500 cubes to bankrob!")
    else:
        await ctx.channel.send(f"{ctx.message.author.mention}, wny do you want to bankrob yourself???")

async def ubankrob():
    global heist_timer
    if heist_timer > 0:
        heist_timer -= 1
        await asyncio.sleep(1)
    else:
         heist_timer = 0


# @client.command(help="Get today's problem!")
# async def daily(ctx):
#     mycursor = connection.cursor()
#     mycursor.execute("SELECT * from aops WHERE member_id={}".format(int(ctx.message.author.id)))
#     myres = mycursor.fetchone()
#     mycursor.execute("SELE
#     CT * from potd order by problem_id desc")
#     myres2 = mycursor.fetchall()
#     print(myres2[0])
#     if int(myres[5]) == 0:   # means that POTD was not solved yet
#         await ctx.channel.send(f"{ctx.message.author.mention}, today's problem is: **{myres2[0][1]}**")
#         mycursor.execute("UPDATE aops SET solving={} WHERE member_id={}".format(1, int(ctx.message.author.id)))
#     else:
#         await ctx.channel.send(f"{ctx.message.author.mention}, you already solved today's Problem of the day! Come back tomorrow! In the meantime, run aops help for more ways to get more math problems!")

# @client.command(help="Check out the AoPS shop!")
# async def shop(ctx):
@client.command()
@has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member = None, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send('You cannot mute yourself. The Everything Bot! does not allow self-harm.')
    elif member is None:
        await ctx.channel.send('You cannot mute nobody you stupid!')
    else:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        print(ctx.message.content)
        if not member:
            await ctx.channel.send('I can\'t mute a fellow bot.')
            return
        await member.add_roles(role)
        await ctx.channel.send('%s has been successfully muted by %s' % (member, ctx.message.author))
        channel = await member.create_dm()
        await channel.send(
            f'{member.name}, you were muted in {guild.name} by {ctx.message.author}.'
            f' | Reason: %s. You may contact them to appeal the mute.' % reason
        )


@client.command()
@has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    print(ctx.message.content)
    if not member:
        await ctx.channel.send('I couldn\'t mute a bot. HOW CAN I UNMUTE ONE U IMBECILE.')
        return
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.channel.send('%s has been successfully unmuted by %s' % (member, ctx.message.author))
        channel = await member.create_dm()
        await channel.send(
            f'{member.name}, you were unmuted in the server by {ctx.message.author}.  Great!'
        )
    else:
        await ctx.channel.send('%s was never muted in the first place, %s!' % (member, ctx.message.author))


@client.command()
@has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if member:
        embed = discord.Embed(title="{} has been warned by {}".format(member, ctx.message.author),
                              description="{}".format(
                                  '%s, you have been warned by %s.  Reason: %s' % (member, ctx.message.author, reason)))
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send('%s, please specify a member to warn' % (ctx.message.author))
    channel = await member.create_dm()
    await channel.send(
        f'{member.name}, you were warned in the server by {ctx.message.author}.'
        f' | Reason: %s.' % reason
    )


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title="{} has been kicked by {}".format(member, ctx.message.author), description="{}".format(
        '%s, you have been kicked by %s.  Reason: %s' % (member, ctx.message.author, reason)))
    await ctx.channel.send(embed=embed)
    channel = await member.create_dm()
    await channel.send(
        f'{member.name}, you were kicked in the server by {ctx.message.author}.'
        f' | Reason: %s.' % reason
    )


@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(title="{} has been banned by {}".format(member, ctx.message.author),
                          description="{}".format(
                              '%s, you have been banned by %s.  Reason: %s' % (member, ctx.message.author, reason)))
    await ctx.channel.send(embed=embed)
    channel = await member.create_dm()
    await channel.send(
        f'{member.name}, you were banned in the server by {ctx.message.author}.'
        f' | Reason: %s.' % reason
    )


@client.command()
@has_permissions(ban_members=True)
async def banid(ctx, member, *, reason=None):
    toban = await client.fetch_user(int(member))
    await ctx.guild.ban(toban, reason=reason)


@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title="{} has been unbanned by {}".format(member, ctx.message.author),
                                  description="{}".format(
                                      '%s, you have been unbanned by %s' % (member, ctx.message.author)))
            await ctx.channel.send(embed=embed)
            channel = await member.create_dm()
            await channel.send(
                f'{member.name}, you were unbanned in the server by {ctx.message.author}!'
            )
            return


@client.command()
async def checklist(ctx):
    await ctx.channel.send("**CHECKLIST**\n**1**: Currency\n**2**: POTD")

client.run("ODE2ODAyNTQ4MzU0NTE0OTQ0.YEAQpg.oPAh3pga8D-sqwqo9I6uFlny5-c")
