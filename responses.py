import random
import string

#converts the message to a string and makes sure it is lower case
def get_response(message: str) -> str:
    p_message = message.lower()
#coin is storing heads or tails
    coin = ["Heads", "Tails"]
#this will generate a password that is 22 characters long, i wont recommand using a password that this generat
    def generate_password(length):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    password = generate_password(22)
#generates the password when the user types !password, i would recommend typing ?!password instead so it sends to a private message instead of public server
    if p_message == '!password':
        return(password)
#bot responds to a user if they say hello
    if p_message == 'hello':
        return 'Hey'
#rolls a dice pices a random number between 1 and 6
    if message == '!roll':
        return str(random.randint(1, 6))
#gives a list of commands
    if p_message == '!help':
        return '`To flip a coin type !coinflip \n To play rock paper scissors type ! followed by rock, paper or scissors, eg. !rock. \n To roll a dice type !roll. \n To play blackjack type !blackjack, then follow the instructions. \n To play a trivia game type !trivia, if you dont know an answer type hint to get a hint. \n To generate a password type !password. \n type !hangman to play hangman \n !chat and a question to ask chatgpt a question \n !join to join a story then type !story then a number for how long it will be.`'
#flips a coin uses the coin varibale from earlier
    if p_message == '!coinflip':
        return(random.choice(coin))
#egg
    if "egg" in p_message.lower():
        return "eggcellent"
    
  