import discord
from discord.ext import commands

TOKEN = "OTgzODU4MDQxOTc3OTcwNzI4.GqLk2U.lOVlJrdYY6rHWu3VUujTgywz6IyzPquhE-V7RI"

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    user_message = str(message.content)
    if message.author == client.user:
        return

    if message.channel.name == "moderator-only":
        #if str(message.author) == "Juanzin#6760":
        if str(message.author) == "InviteLogger#5780":
            tagged_user = user_message.split(" ")[0]
            member_id = message.author.mention
            split_memberid_1 = member_id.split("@")[1]
            split_memberid_2 = split_memberid_1.split(">")[0]
            member = await message.guild.fetch_member(member_id=int(split_memberid_2))
            total_invites = user_message.lower().split("now has ")[1].split(" invites")[0]
            if int(total_invites) == 5:
                bot_channel = client.get_channel(966774320804290640)
                await bot_channel.send(f"{tagged_user} now have 5 invites! {tagged_user} was assign to early supporters role and is now eligible for giveaways!")
                await member.add_roles(discord.utils.get(message.guild.roles, name="Early Supporters"))
    
    #if message.content.startswith('!hello'):
    #    await message.channel.send('Hello!')

client.run(TOKEN)