import json, nltk, discord, asyncio, random, os
import urllib.request as urllib
from functools import reduce

def GetBeeFact():
    response = urllib.urlopen('https://en.wikipedia.org/w/api.php?action=query&titles=Bee&prop=revisions&rvprop=content&format=json')
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    bee_facts_text = json.loads(data.decode(encoding))["query"]["pages"]["4654"]["revisions"][0]["*"]
    tags_to_remove = ["''", ")", "[[", "]]"]
    bee_facts_text = reduce(lambda a, k: a.replace(k, ""), tags_to_remove, bee_facts_text)
    tokenizer = nltk.data.load('nltk/english.pickle')
    unformatted_sentences = tokenizer.tokenize(bee_facts_text)
    formatted_sentences = []
    for s in unformatted_sentences:
        if "===" in s or "{{" in s or "/" in s or '\"' in s or "|" in s or "<" in s or len(s.split(' ')) < 5 or "bee" not in s:
            continue
        else:
            formatted_sentences.append(s)
    return formatted_sentences[random.randint(1, len(formatted_sentences) - 1)]

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')

@client.event
async def on_message(message):
    if "buzz" in message.content.lower() or "bee" in message.content.lower() and message.author != client.user:
        bee_fact = GetBeeFact()
        await client.send_message(message.channel, bee_fact)

client.run(os.environ['BEEBOTTOKEN'])
