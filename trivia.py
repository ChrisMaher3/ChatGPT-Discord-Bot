import random
import discord
import asyncio

#all the questions
#if we had more time we would of made it so chatgpt will generate a random question for you
questions = [
"What is the name of the famous ship that sank in 1912?",
"What is the name of the highest mountain in Africa?",
"Who was the first President of the United States?",
"What type of animal is a Komodo Dragon?",
"What is the smallest country in the world?",
"Which planet in our solar system is closest to the Sun?",
"What famous artist painted The Persistence of Memory?",
"What is the best course?",
"What is the worst course?",
"Which country produces the most coffee in the world?",
"Which racer holds the record for the most F1 Grand Prix wins?",
"What country won the very first FIFA World Cup in 1930?",
"Which Indiana Jones movie was released back in 1984?",
"What does DC stand for?",
"Who was the first woman to win a Nobel Prize?",
"What year was the very first model of the iPhone released?",
"What does “HTTP” stand for?",
"What part of the atom has no electric charge?",
"Which planet has the most gravity?",
]
#takes a random question
def get_random_question():
    return random.choice(questions)
#checks if the message is private or in a server 
async def trivia_game(message, client):
    is_private = isinstance(message.channel, discord.DMChannel)
#currently the player has no question and hasnt used up any attempts as they have not started the game
    current_question = None
    attempts = 0
#the questions with hints
    hints = {
    "What is the name of the famous ship that sank in 1912?": ["It was meant to be unsinkable"],
    "What is the name of the highest mountain in Africa?": ["It's located in Tanzania"],
    "Who was the first President of the United States?": ["He was a General in the American Revolution"],
    "What is the smallest country in the world?": ["t is located in the city of Rome"],
    "Which planet in our solar system is closest to the Sun?": ["It's the smallest planet"],
    "What famous artist painted The Persistence of Memory?": ["His first name is Salvador"],
    "What is the best course?": ["Starts with a P"],
    "What is the worst course?": ["Starts with a b"],
    "Which country produces the most coffee in the world?": ["South American country"],
    "Which racer holds the record for the most F1 Grand Prix wins?": ["He is still driving today"],
    "What country won the very first FIFA World Cup in 1930?": ["It is a country in south South America"],
    "Which Indiana Jones movie was released back in 1984?": ["It has temple in its name"],
    "What does DC stand for?": ["________ Comics"],
    "Who was the first woman to win a Nobel Prize?": ["in 1903"],
    "What year was the very first model of the iPhone released?": ["Hint: it was released in the 21st century"],
    "What does “HTTP” stand for?": ["Hint: it's a protocol used for communication on the web"],
    "What part of the atom has no electric charge?": ["Hint: it's located in the nucleus of the atom"],
    "Which planet has the most gravity?": ["Hint: it's the largest planet in our solar system"],
    }
#the questions with the answers
    questions_and_answers = {
    "What is the name of the famous ship that sank in 1912?": "Titanic",
    "What is the name of the highest mountain in Africa?": "Mount Kilimanjaro",
    "Who was the first President of the United States?": "George Washington",
    "What type of animal is a Komodo Dragon?": "Lizard",
    "What is the smallest country in the world?": "Vatican City",
    "Which planet in our solar system is closest to the Sun?": "Mercury",
    "What famous artist painted The Persistence of Memory?": "Salvador Dali",
    "What is the best course?": "Physics",
    "What is the worse course?": "Business",
    "Which country produces the most coffee in the world?": "Brazil",
    "Which racer holds the record for the most F1 Grand Prix wins?": "Lewis Hamliton",
    "What country won the very first FIFA World Cup in 1930?": "Uruguay",
    "Which Indiana Jones movie was released back in 1984?": "Indiana Jones and the Temple of Doom",
    "What does DC stand for?": "Detective Comics",
    "Who was the first woman to win a Nobel Prize?": "Marie Curie",
    "What year was the very first model of the iPhone released?": "2007",
    "What does “HTTP” stand for?": "Hypertext Transfer Protocol",
    "What part of the atom has no electric charge?": "Neutron",
    "Which planet has the most gravity?": "Jupiter",
    }

#if the user types !trivia it picks one of the questions at random
    if message.content.startswith('!trivia'):
        current_question = get_random_question()
#if the user types ?!trivia it will send the question to the user through a direct message and not on the server
        if is_private:
            await message.author.send(current_question)
        else:
            await message.channel.send(current_question)
#tells the user to type their answer
    while current_question:
        await message.channel.send("Type your answer")
#allows time for the user to type their answer
#we messed around with using different settings for this or not using it and it doesnt work without it
        try:
            reply = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == message.author and m.channel == message.channel)
        except asyncio.TimeoutError:
            await message.channel.send('Timeout')
            return
#keeps track of the amount of attempts 
        attempts += 1
#converts everything to lowercase just in case the user uses upper case
        reply_content = reply.content.lower()
#if the users answer matches the currect answer the user is correct
        if reply_content == questions_and_answers[current_question].lower():
            await message.channel.send("Correct!")
            return
#if the user types hint it outputs the hint that is attacheted to that question
        elif reply_content == 'hint':
            if current_question in hints:
                hint_index = min(attempts - 1, len(hints[current_question]) - 1)
                hint = hints[current_question][hint_index]
#fail safe just in case there is no hints but every question does have a hint
            else:
                hint = "There is no hints for this question"
#same stuff, but this time for private messaging
            if is_private:
                await message.author.send(hint)
            else:
                await message.channel.send(hint)
#if the answer that the user types isnt the same as the correct answer the bot outputs wrong answer
        else:
            await message.channel.send("Wrong answer!")
            return