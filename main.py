import discord
import os
import requests

from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# can be done with API call
roles = ['','Caster','Fighter','Protector']

minionTypes = requests.get(f'https://us.api.blizzard.com/hearthstone/metadata/sets?locale=en_US&access_token={os.getenv("BLIZZTOKEN")}').json()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
      merc = message.content[1:]
      res = requests.get(f'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&gameMode=mercenaries&textFilter={merc}&access_token={os.getenv("BLIZZTOKEN")}')
      
      print(res.json())
      
      try:
        data = res.json()['cards'][0]
      except:
        await message.channel.send(f'Could not find {merc}')
        print('invalid merc name')
        return

      for t in minionTypes:
        if t['id'] == data['minionTypeId']:
          type = t['name']

      embed=discord.Embed(title=data['name'], color=0xFF5733)
      embed.add_field(name=type, value=roles[data['mercenaryHero']['roleId']])
      embed.set_image(url=data['image'])
      # embed.add_field(name='',value='I am a work in progress.')
      await message.channel.send(embed=embed)

keep_alive()

client.run(os.getenv('TOKEN'))
