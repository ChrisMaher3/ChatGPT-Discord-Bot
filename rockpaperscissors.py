import random
#converts the text to a string and lower case
def rock_paper_scissors(message: str) -> str:
    p_message = message.lower()
#stores the rock paper and scissors
    rps = ["Rock", "Paper", "Scissors"]
#the bot picks a random one from rps
    botpick = random.choice(rps)
#if the player chooses rock and the bot pick rocks its a draw
    if p_message == '!rock' and botpick == 'Rock':
        return 'Rock: Draw'
#if the player chooses rock and the bot chooses paper player loses
    if p_message == '!rock' and botpick == 'Paper':
        return 'Paper: Lose'
#if player chooses rock and bot chooses scissors the player wins
    if p_message == '!rock' and botpick == 'Scissors':
        return 'Scissors: Win'
#if the player chooses paper and the bot chooses paper its a draw
    if p_message == '!paper' and botpick == 'Paper':
        return 'Paper: Draw'
#if the player chooses paper and the bot picks scissors the player looses
    if p_message == '!paper' and botpick == 'Scissors':
        return 'Scissors: Lose'
#if the player chooses paper and the bot chooses rock the player wins
    if p_message == '!paper' and botpick == 'Rock':
        return 'Rock: Win'
#if the player chooses scissors and the bot picks scissors its a draw
    if p_message == '!scissors' and botpick == 'Scissors':
         return 'Scissors: Draw'
#if the player chooses scissors and the bot picks rock the player loses
    if p_message == '!scissors' and botpick == 'Rock':
        return 'Rock: Lose'
#if the player chooses scissors and the bot picks paper the player wins
    if p_message == '!scissors' and botpick == 'Paper':
        return 'Paper: Win'