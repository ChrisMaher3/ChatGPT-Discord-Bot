#Module for asynchronous operations this is for making requests and not blocking to wait for them to complete
import asyncio 
#Module to interact with Discords API
import discord
#Imports from the file names responses.py
import responses
#Imports from the file names rockpaperscissors.py
import rockpaperscissors
#Imports from the file names blackjack.py
import blackjack
#Imports from the file names trivia.py
import trivia
#Imports the module os for operating system realted functionality
import os
#Imports the module openai to interact with OpenAi APIs
import openai
#Imports commands from discord.ext to make discord bot commands
from discord.ext import commands
#Imports random module for generating random numbers
import random
import hangman

# empty list of players and story context this is to add a empty value to the variables below
players = []
story_context = ""

#Below is an async function to send messages using the discord bot
async def send_message(message, user_message, is_private):
#Below it is attempting to get a response form the responses module
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
#Below the code is trying the use the code from the rockpaperscissors.py to play rock paper scissors
    try:
        rockpapersci = rockpaperscissors.rock_paper_scissors(user_message)
        await message.author.send(rockpapersci) if is_private else await message.channel.send(rockpapersci)
    except Exception as e:
        print(e)

#Below is the function to run the discord bot the token similar to the Openai/Chatgpt API is unique and identifies our unique bot we set it to TOKEN
def run_discord_bot():
    TOKEN = 'Insert Discord Token Here'
#Below is required configurations for the discord bot this was found online and is required to run the bot.
    intents = discord.Intents.default()
    intents.message_content = True

#Below is used for whe !(command) is used that command is activated it essientially assigns ! to be reuired for commands
    bot = commands.Bot(command_prefix="!", intents=intents)
    @bot.event
    async def on_ready():
#Below lets the user know in the command terminal that the bot is succefully running.
        print(f'{bot.user} is now running!')

#Below handles the bots ability to handle incoming messages
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" ({channel})')

        is_private = isinstance(message.channel, discord.DMChannel)

#Below the code checks what the message starts with and based on that initiates the content it corresponds to.
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private)
        elif user_message.startswith('!blackjack'):
            await blackjack.blackjackgame(message, bot)
        elif user_message.startswith('!trivia'):
            await trivia.trivia_game(message, bot)
        elif user_message.startswith('!hangman'):
            await hangman.hangman_game(message, bot)
        else:
            await send_message(message, user_message, is_private)

            await bot.process_commands(message)
    
#Below is the chatgpt API this is a personal key that is linked to the openai account and allows you to intergrate the AI into your code
    openai.api_key = "Inset OpenAI api key here"
    
    @bot.command(name="chat")
    async def chat(ctx, *, prompt):
        response = openai.ChatCompletion.create(
#Below the model can be selected on the openai website and changed to your needs you can use gpt 3.5 like we did or gpt 4 which is better but more expensive.
        model="gpt-3.5-turbo",
        messages=[
#Below you can set what the bot is assigned to do in this case it is set to be a helpful assistant
            {"role": "system", "content": "You are a helpful assistant."},
#Below you set what goes into chatgpt in this case it is the message the user inputs after !chat
            {"role": "user", "content": prompt}
        ],
#Tokens limits is how many words the bot can generate at a time. 1000 tokens is around 750 words
        max_tokens=100,
#n specifies the amount of responses you want
        n=1,
#This tells chatgpt to stop
        stop=None,
#Temparture sets the bots creativity
        temperature=0.8,
        )
#Waits for the user input
        await ctx.send(response['choices'][0]['message']['content'])
#This bot command lets multiple people join at a time they simply have to type !join
    @bot.command(name="join")
    async def join(ctx):
        global players
        if ctx.author not in players:
            players.append(ctx.author)
            await ctx.send(f"{ctx.author.name} has joined the game.")
        else:
            await ctx.send(f"{ctx.author.name}, you are already in the game.")

 #Define a function to initialize the story context using the OpenAI API.    
    async def initialize_story_context(players):
        player_names = ', '.join([player.name for player in players])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a game master for a game like dungeons and dragons."},
            {"role": "user", "content": f"Create a quest for a group of adventurers consisting of {player_names}"}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=1,
            )
        story_context = response.choices[0].message.content
        return story_context

 #Define a bot command to generate a story with a given number of rounds. So it would be !story (number of rounds) eg !story 5 continues for 5 responses
    @bot.command(name="story")
    async def generate_story(ctx, rounds: int):
        global players
        global story_context
        if len(players) > 0:
            story_context = await initialize_story_context(players)
            for round in range(rounds):
                for player in players:
                    player_prompt = await generate_prompt(player)
                    await ctx.send(player_prompt)
                    player_action = await bot.wait_for('message', check=lambda message: message.author == player, timeout=60)
                    story_context = update_story_context(story_context, player, player_action.content)
            conclusion = await generate_conclusion()
            await ctx.send(conclusion)
        else:
                await ctx.send("No players joined the game. Try again later.")

          
#Define a function to generate prompts for players to take action in the story.
    async def generate_prompt(player):
        global story_context
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": story_context},
             {"role": "user", "content": f"Generate a prompt for {player.name} to take action in the story"}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=1,
        )
        
        prompt = response.choices[0].message.content
        return f"{player.name}, {prompt}"
        
 #Define a function to update the story context based on a player's action.
    def update_story_context(story_context, player, player_action):
        dice_roll = random.randint(1, 6)
#Generate a random dice roll from 1 to 6 and based on the action let the users action be successful or unsuccessful
        success = dice_roll >= 4
        action_result = "successfully" if success else "unsuccessfully"
        updated_story_context = f"{story_context}\nPlayer {player.name} attempted to {player_action}. They {action_result} did it! (Rolled {dice_roll})"
#Returns the updated story context.
        return updated_story_context

#Generates the conclusion after it reaches the number of prompts specified.
    async def generate_conclusion():
        global story_context
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": story_context},
            {"role": "user", "content": "Generate a conclusion for the story"}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
            )
        return response.choices[0].message.content


#Run the bot using the provided token.  
    TOKEN = 'Inset Discord Token here'
    bot.run(TOKEN)