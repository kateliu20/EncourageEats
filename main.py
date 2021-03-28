import discord
import os
import requests
import json
import random
import schedule
import time
import tasks
from replit import db
import spoonacular as spoon
from discord.utils import get
from keep_alive import keep_alive
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands, tasks

client = discord.Client()

spoonapi = spoon.API("461f41ebb7c24e10ae843ba97a2a9cd8")

happy_words = ["happy", "amazing", "love", "excited", "good"]

happy_encouragements = [
  "that's great to hear!",
  "keep it up!",
  "yay"
]

ed_words = ["sad", 
"depressed", 
"unhappy", 
"ugly", 
"fat", 
"never be skinny", 
"hate", 
"anorexia", 
"throw up", 
"obese", 
"disgusting", 
"depressing", 
"bad", 
"lonely",
"alone",
"worthless", 
"lost"]

hunger_words = ["hungry", "starving", "i'm so hungry", "i want food", "i don't want to eat, hangry, i can't eat, i won't eat, i should eat, i shouldn't eat, i cannot eat"]

starter_encouragements = [
  "you are beautiful",
  "you deserve love",
  "your body is beautiful",
  "your resiliency continues to amaze me",
  "you are not alone",
  "you are beautiful",
  "you are loved",
  "it's okay"
]

hunger_encouragements = [
  "you should eat. remember that your body needs fuel"
]

healthy_ingredients = [

]
db["ingredients"]=healthy_ingredients

workoutQuoteUrl="https://bodybuilding-quotes.p.rapidapi.com/random-quote"
workoutQuoteHeaders = {
    'x-api-key': "thisismyapikey",
    'x-rapidapi-key': "0ea00d285cmshcf04b5e648a2f9bp11d4c0jsn9d4e11d5e21e",
    'x-rapidapi-host': "bodybuilding-quotes.p.rapidapi.com"
    }
workouts = [
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Aphrodite_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Aphrodite_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Aphrodite_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Apollon_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Apollon_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Apollon_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Ares_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Ares_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Ares_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Artemis_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Artemis_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Artemis_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Athena_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Athena_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Athena_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Atlas_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Atlas_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Dione_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Dione_Standard_english.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Dione_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Gaia_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Gaia_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Gaia_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hades_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hades_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hades_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Helios_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Helios_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Helios_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hera_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hera_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hera_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hermes_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hermes_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hyperion_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Hyperion_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Iris_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Iris_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Iris_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Kentauros_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Kentauros_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Kentauros_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Krios_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Krios_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Krios_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Kronos_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Kronos_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Kronos_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Metis_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Metis_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Metis_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Morpheus_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Morpheus_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Morpheus_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Nemesis_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Nemesis_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Nyx_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Nyx_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Nyx_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Persephone_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Persephone_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Poseidon_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Poseidon_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Poseidon_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Prometheus_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Prometheus_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Thanatos_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Thanatos_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Thanatos_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Triton_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Triton_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Triton_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Uranos_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Uranos_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Uranos_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Venus_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Venus_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Venus_Strength.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Zeus_Endurance.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Zeus_Standard.jpg",
    "https://raw.githubusercontent.com/dpano/bodyweightScraper/master/images/Zeus_Strength.jpg"
]

recipeResponse = [
  'Enjoy a nutritious meal:',
  'Get ready to eat with this nutritious meal:',
  "It's important to eat a well rounded meal:",
  'Call yourself Chef Boyardee with this meal:'
]

happyResponse = [
  "YAY! https://images.squarespace-cdn.com/content/55ee8615e4b077f58027f44a/1471703548148-HPYBR3WYG5FXJMN3V6AA/YAY_http-%3A%3Ai1361.photobucket.com%3Aalbums%3Ar666%3Akaramelkinema%3APosts%3A2013%3A07-July%3A03-DM2%3AMinions10_zpsdd28ca77.gif?content-type=image%2Fgif",
  "You being happy makes me happy! https://media0.giphy.com/media/pVHtTZecU68pJcZDfX/giphy.gif",
  "Nobody can stop you! https://media4.giphy.com/media/yidUzmRLUiqnzHo7aE/giphy.gif" 
]

sadResponse = [
  "Sorry to hear that, sending you a virtual hug https://media0.giphy.com/media/9JnRMIFMYAKpaHRXRF/giphy.gif",
  "Hang in there, sending you virtual love! https://media2.giphy.com/media/YT95XJOLvY1t2SJgpR/giphy.gif",
  "Know you are not alone! You can use $help to find resources. https://i.gifer.com/TVbe.gif"
]

angryResponse = [
  "If you're feeling angry or stressed, it's important to get exercise! Science has shown exercise can reduce stress! https://media2.giphy.com/media/4bjIKBOWUnVPICCzJc/source.gif",
  "Take a timeout! Saving a few minutes now and taking a rest can be hugely beneficial https://media.tenor.com/images/0eba24ce62b28c16e62173ffc4c3b939/tenor.gif",
  "Know you are not alone! You can use $help to find resources. https://i.gifer.com/TVbe.gif"
]

sickResponse = [
  "If you feel it is an emergency, call 911 immediately. Otherwise, use $help to find multiple resources that may fit you"
]

sleepyResponse = [
  "It's important to get at least 8 hours of sleep! Staying up late can cause a multitude of problems. https://media.tenor.com/images/79b6ad95f6f6b6dc0c57b862fbf456e8/tenor.gif",
  "Do not overwork yourself and listen to your body! https://media.tenor.com/images/c766c4b93868b75b59532b4cf17f004f/tenor.gif"
]

coolResponse = [
  "You're on top of the world! https://media.tenor.com/images/826902bc1cb0d83ebed999e7255782a1/tenor.gif",
  "You're unstoppable! Nothing can beat you https://media3.giphy.com/media/26BRDP1iv4gN1w1JC/source.gif",
  "Gonna go super saiyan soon! https://media0.giphy.com/media/ul1omlrGG6kpO/giphy.gif"
]

lovedResponse = [
  "We love you too! https://media.tenor.com/images/4294deb5ec97086243174b085d609695/tenor.gif",
  "https://media3.giphy.com/media/Yle9Yz9izeVRyiwavn/giphy.gif"
]
#print(data[0]['title']) #prints out food title

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_list(new_task):
  if "tasks" in db.keys():
    tasks = db["tasks"]
    tasks.append(new_task)
    db["tasks"] = tasks
  else:
    db["tasks"] = [new_task]

def delete_task(delMessage):
  tasks = db["tasks"]
  if len(tasks) > 0:
    try:
      tasks.remove(delMessage)
      db["tasks"] = tasks
    except ValueError:
      return "error"
  else:
    return "short"

def add_ingredient(ing):
  if "ingredients" in db.keys():
    ingredients = db["ingredients"]
    ingredients.append(ing)
    db["ingredients"] = ingredients
  else:
    print("hi")
    db["ingredients"] = [ing]

def del_ingredient(ingredient):
  ingredients = db["ingredients"]
  if len(ingredients) > 0:
    try: 
      ingredients.remove(ingredient)
      db["ingredients"]=ingredients
    except ValueError:
      return "error"
  else:
    return "short"
    

##def job():
    #print("hi! how are you doing today?")

#schedule.every().day.at("10:30").do(job)
#schedule.every(10).seconds.do(job)

#while True:
    #schedule.run_pending()
    #time.sleep(1)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#client = commands.Bot(command_prefix="!")
#@tasks.loop(seconds=1.0)

#async def sendDailyMessage():
  #channel = client.get_channel(825414166943629322-825484178979029072)
  #channel.send("hi! how are you doing today?")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$commands'):
      await message.channel.send('```Here are the list of commands you can do:\n• $hello to start a conversation\n• $inspire to get a motivational quote \n• $mood to track your mood for today\n• $help for when you need mental health help that is beyond this discord \n• $recipe generates a healthy recipe for you. Rated healthy score out of /100 \n• $ingredients [ingredients to add] to input what ingredients you have for recipes \n• $cupboard to see what ingredients you currently have \n• $removeingredients [ingredients] to remove ingredients from the cupboard \n• $new [task to add] to add a task\n• $del [task to delete] to delete a task\n• $tasks to view your tasks for the day\n• $exercise to generate workouts```')

    if msg.startswith('$hello'):
      await message.channel.send('hi! how are u?')
    
    if msg.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)
    
    if msg.startswith('$mood'):
      await message.channel.send('how are you feeling today?')
      number_of_responses = 7
      emoji_numbers = ["🙂", "😢", "😡", "🤢", "😴", "😎", "🥰"]
      for i in range(number_of_responses):
        await message.add_reaction(emoji_numbers[i])
    
    if msg.startswith('$help'):
      await message.channel.send('I hope you are safe. Here are some helpful links or numbers you can reach out to: \n\n**National Suicide Prevention Lifeline:** 800-273-8255 \n**National Eating Disorder Association:** 1-800-931-2237 or \nText “NEDA” to 741-741 \n**The National Alliance on Mental Illness:** Text “NAMI” to 741-741 \n**Crisis Text Line:** Text HOME to 741-741 \nFor students of color, you can text STEVE to 741-741 \n**Trevor Project Lifeline:** 1-866-488-7386 \n**Trevor Project Crisis Textline:** Text 678-678 \n**Trevor Chat & other resources:** https://www.thetrevorproject.org/get-help-now/ \n**Trans Lifeline:** 877-565-8860\n**Pride Institute:** (800) 547-7433 24/7')

    options = starter_encouragements

    options2 = hunger_encouragements 
    options3 = happy_encouragements
       #if "encouragements" in db.keys():
      #options = options + db["encouragements"]

    #recipe 
    if msg.startswith("$recipe") or msg.startswith("$food"):
      ingredients = db["ingredients"]
      if len(ingredients) < 1:
        await message.channel.send(' I cannot make recips when you have nothing in the cupboard Add with $ingredients')
        return
      await message.channel.send("Generating recipe with items in your cupboard!")
      response = spoonapi.search_recipes_by_ingredients(random.choice(ingredients), number = 1) #looksup food by ingredient
      data=response.json()
      nutrition = spoonapi.get_recipe_information(data[0]['id']) #looks up food info
      nutData = nutrition.json()
      await message.channel.send(random.choice(recipeResponse))
      await message.channel.send("Recipe link: " + nutData["sourceUrl"])
      await message.channel.send("Dish: " + data[0]['title'])
      await message.channel.send("Health Score: " + str(nutData['healthScore']) + "/100")

    if any(word in msg for word in ed_words):
      await message.channel.send(random.choice(options)) 
    
    if any(word in msg for word in happy_words):
      await message.channel.send(random.choice(options3))

    if any(word in msg for word in hunger_words):
      await message.channel.send(random.choice(options2))   
    
    if msg.startswith("$new"):
      new_task = msg.split("$new ",1)[1]
      update_list(new_task)
      await message.channel.send("new task added")

    if msg.startswith("$del"):
      tasks = []
      if "tasks" in db.keys():
        delMessage = msg.split("$del ",1)[1]
        answer = delete_task(delMessage)
        if(answer == "error"):
          await message.channel.send("Error: Task not found")
          return
        elif(answer=="short"):
          await message.channel.send("Cannot delete with 0 tasks to do")
          return
        tasks = db["tasks"]
      await message.channel.send(tasks)

    if msg.startswith("$exercise") or msg.startswith("$workout"):
      await message.channel.send(random.choice(workouts))

    if msg.startswith("$cupboard"):
      ingredients = db["ingredients"]
      await message.channel.send("According to me, you currently have: ")
      if(len(ingredients)<1):
        await message.channel.send("Nothing. Add ingredients with $ingredients [ingredients to add]")
      else:
        finishedMessage = ""
        for ingredient in ingredients:
          finishedMessage += ingredient + " "
        await message.channel.send(finishedMessage)

    if msg.startswith("$ingredients"):
      ingredients = msg.split(" ")
      finalMessage = "Ingredients added to your cupboard: "
      for ingredient in ingredients:
        if ingredient != "$ingredients":
          add_ingredient(ingredient)
          finalMessage += ingredient + " "
      if finalMessage == "Ingredients added to your cupboard: ":
        await message.channel.send("Please check your input, no ingredients detected")
      else:
        await message.channel.send(finalMessage)
      
    if msg.startswith("$removeingredients"):
      ingredients = msg.split(" ")
      finalMessage = "Deleted "
      for ingredient in ingredients:
        if ingredient != "$removeingredients":
          try:
            del_ingredient(ingredient)
            finalMessage += ingredient + " "
          except ValueError:
            await message.channel.send("Error: Could not find ingredient " + ingredient + " in your cupboard" )
      if finalMessage == "Deleted ":
        await message.channel.send("Please check your input, no ingredients detected")
      else:
        await message.channel.send(finalMessage + " from your cupboard")

    if msg.startswith("$tasks"):
      tasks = []
      if "tasks" in db.keys():
        tasks = db["tasks"]
      await message.channel.send('Here are your tasks for today:')
      for task in tasks:
        await message.channel.send("• "+task)

@client.event
async def on_raw_reaction_add(payload):
  if(payload.user_id!=825372151237705738):
    if(payload.emoji.name == "😢"):
      await client.get_channel(payload.channel_id).send(random.choice(sadResponse))
    if(payload.emoji.name == "🙂"):
      await client.get_channel(payload.channel_id).send(random.choice(happyResponse))
    if(payload.emoji.name == "😡"):
      await client.get_channel(payload.channel_id).send(random.choice(angryResponse))
    if(payload.emoji.name == "🤢"):
      await client.get_channel(payload.channel_id).send(random.choice(sickResponse))
    if(payload.emoji.name == "😴"):
      await client.get_channel(payload.channel_id).send(random.choice(sleepyResponse))
    if(payload.emoji.name == "😎"):
      await client.get_channel(payload.channel_id).send(random.choice(coolResponse))
    if(payload.emoji.name == "🥰"):
      await client.get_channel(payload.channel_id).send(random.choice(lovedResponse))

keep_alive()
client.run(os.getenv('TOKEN'))