#works on replit with its own db and pings session only for 1 hr if inactive for an hour


import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

sad_words = ['unhappy','sad','depressed', 'miserable', 'depressing','angry', 'upset',]
encouragement_words = ['Cheer up!', 'Hang in there!', 'You are a great person!', 'You are amazing!']

if 'responding' not in db.keys():
  db['responding'] = True


#client = discord.Client()

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_encoragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements


  else:
    db['encouragements'] = [encouraging_message]
    
def delete_ecouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements



@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
    
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db['responding']:
    options = encouragement_words
    if 'encouragements' in db.keys():
      options = options + db['encouragements'].value

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith('$new'):
    encouraging_message = message.content.split('$new ',1)[1]
    update_encoragements(encouraging_message)
    await message.channel.send('New encouraging message added.')

  if message.content.startswith('$del'):
    encouragements=[]
    if 'encouragements' in db.keys():
      index = int(message.content.split('$del',1)[1])
      delete_ecouragement(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)
    
  if message.content.startswith('$list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if message.content.startswith('$responding'):
    value = message.content.split('$responding ',1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Responding is on.')
    else:
      db['responding'] = False
      await message.channel.send('Responding is off.')


keep_alive()

client.run(os.environ['TOKEN'])



