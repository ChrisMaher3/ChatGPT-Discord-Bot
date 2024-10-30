# necessary modules imported
import random
import asyncio
 
# the ASCII art used to visually display how many times you made an incorrect guess
stage1 = """ 
                    +---+
                       |
                     |
                     |
                     |
                       |
          =========' """

stage2 =  """ 
              +---+
              |        |
                       |
                      |
                      |
                       |
          =========' """

stage3 =  """ 
              +---+
              |        |
            O         |
             |        |
                       |
                       |
          =========' """

stage4 =  """ 
              +---+
              |        |
              O      |
             /|       |
                       |
                       |
          =========' """

stage5 =  """ 
              +---+
              |        |
              O      |
             /|\     |
                       |
                       |
          =========' """

stage6 =  """ 
              +---+
              |        |
              O      |
             /|\     |
             /        |
                       |
          =========' """
stage7 =  """ 
              +---+
              |        |
              O      |
             /|\     |
             / \     |
                       |
          =========' """

stages = [stage1, stage2, stage3, stage4, stage5, stage6, stage7]


# function used to pick a random word from the list, this word acts as the secret word that the player must guess
def give_word():
    word = ["velocity", "acceleration", "gravity", "friction", "thermodynamics", "electromagnetism", "quantum", "relativity"]
    return random.choice(word)



# the function which contains all the game info that is ran by the "bot.py" file
# "message" is the message sent by the user on Discord and "client" is the Discord client bot
async def hangman_game(message, client):
    # when the message "!hangman" is sent on Discord it starts the game
    if message.content.startswith('!hangman'):
        # initial variables are set
        stage_counter = 0
        current_stage = stages[stage_counter]
        word = give_word()
        guess_left = 7

# response contains the first stage of the game
        response = current_stage + "\n" + str(guess_left) + " guesses remaining\n"

# wordi is a string of dashes that represents the hidden word
        wordi = len(word) * "-"

        response += "The word is: " + wordi
        await message.channel.send(response)

        game_over = False

# while the game is not over this loop continues
        while not game_over:
            try:
                # the bot waits up to 30 secs for the player to send a message on discord containing the their guess for a letter in the word 
                guess_msg = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == message.author and m.channel == message.channel)
                guess = guess_msg.content.lower()
            # if no message is sent within 30 sec the bot sends a message sayining "timeout" and the game ends     
            except asyncio.TimeoutError:
                await message.channel.send('Timeout')
                return

# the following code checks if the guessed letter is in the hidden word
            index = []

# if the guessed letter is in the hidden word , its index position is stored in a list
            if guess in word:
                for i, letter in enumerate(word):
                    if letter == guess:
                        index.append(i)

# hidden word is converted into a list of individual letters
            wordi_list = list(wordi)

            correct_guess = False

            for i in index:
                wordi_list[i] = guess
                correct_guess = True

# wordi_new is the hidden word after filling in the correctly guessed letters
            wordi_new = ''.join(wordi_list)

            if correct_guess:
                wordi = wordi_new
                response = "correct!\n" + stages[stage_counter] + "\n" + wordi

# if there are no longer any letters hidden in the hidden word then the player has on the game
                if wordi == word:
                    response += "\nCongratulations! You've guessed the word!"
                    game_over = True

# if the guess was incorrect, the number of tries you have left to guess is decreased and you progess to the next hangman stage                   
            else:
                guess_left = guess_left - 1
                stage_counter = stage_counter + 1


# this code checks if you have any guesses remaining, if so a message explains the current state of the game, if not it's game over
                if stage_counter < len(stages):
                    response = guess + " is not in the word\n" + stages[stage_counter] + "\n" + wordi
                else:
                    response = "Game over! The word was " + word
                    game_over = True

# the number of remaining attempts is added to the message sent by the bot
            response += "\n" + str(guess_left) + " guesses remaining"
            await message.channel.send(response)
