import discord
import os
import requests
import datetime

from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# can be done with API call
roles = ['','Caster','Fighter','Protector']

minionTypes = requests.get(f'https://us.api.blizzard.com/hearthstone/metadata/minionTypes?locale=en_US&access_token={os.getenv("BLIZZTOKEN")}').json()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    ct = f'[{datetime.datetime.now()}] - '

    if message.content.startswith('!help'):
      embed=discord.Embed(title="Bot Documentation", url="https://github.com/EdwardHeath/HSMercsBot/blob/9e7ea68a2418289259f1c8f6489f6fa70a4f6790/README.md", color=0xFF5733)
      embed.add_field(name='\u200B', value='Contact - https://discord.gg/y5gE3KXp')
      await message.channel.send(embed=embed)
      print(f'{ct}Help requested')
      return


    if message.content.startswith('!'):
      merc = message.content[1:]
      res = requests.get(f'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&gameMode=mercenaries&textFilter={merc}&access_token={os.getenv("BLIZZTOKEN")}')
      
      try:
        data = res.json()['cards'][0]
      except:
        await message.channel.send(f'Could not find {merc}')
        print(f'{ct}invalid merc name: {merc}')
        return

      for t in minionTypes:
        if t['id'] == data['minionTypeId']:
          type = t['name']

      embed=discord.Embed(title=data['name'], color=0xFF5733)
      embed.add_field(name=type, value=roles[data['mercenaryHero']['roleId']])
      embed.set_image(url=data['image'])
      embed.set_footer(text='Get more help [here].(https://discord.gg/y5gE3KXp)')
      await message.channel.send(embed=embed)
      print(f'{ct}{data["name"]} served')

keep_alive()

client.run(os.getenv('TOKEN'))
