import os
import discord
import json
import requests
from replit import db
from keep_alive import keep_alive

#Uses the IMDB API and returns the id of the movie with user specified name
def get_movie_id(movie_name):
  response = requests.get('https://imdb-api.com/en/API/SearchMovie/' + os.environ['IMDB_KEY'] + '/' + movie_name)
  json_data = json.loads(response.text)
  movie_id = json_data['results'][0]['id']
  return(movie_id)

#Uses the if returned by the get_movie_id function and gets information regarding ratings of the movie
#The three ratings that are stored are from IMDB, Metacritic and RottenTomatoes
def get_movie_rating(movie_id):
  response = requests.get('https://imdb-api.com/en/API/Ratings/' + os.environ['IMDB_KEY'] + '/' + movie_id)
  json_data = json.loads(response.text)
  movie_rating = [json_data['imDb'], json_data['metacritic'], json_data['rottenTomatoes']]
  return(movie_rating)

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))
  

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if msg.startswith('$hello'):
    await message.channel.send("Hello!")

#User can type $movie ____ and the above mentioned functions will retrieve the ratings and send them as a message on Discord.
  if msg.startswith('$movie'):
    movie_name = msg.split("$movie ", 1)[1]
    movie_id = get_movie_id(movie_name)
    movie_ratings = get_movie_rating(movie_id)
    await message.channel.send("IMDB: " + movie_ratings[0] + ", Metacritic: " + movie_ratings[1] + ", RottenTomatoes: " + movie_ratings[2])
    
#Keep alive is a different file that is required so that I can host the Bot. After that I use Uptime Robot to keep pinging it so that it always stays on
#even when the repl.it tabs are closed. I currently don't possess specific information about it, I just use it to keep my Bot alive at all times. I will
#upload it to GitHub in case some wants to use it as well.
keep_alive()
client.run(os.environ['TOKEN'])
