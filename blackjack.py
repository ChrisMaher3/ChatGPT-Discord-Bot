import random
import asyncio
import discord

#King, Queen and Jack are 10.
#The cards that can be dealt.
def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

#if the player gets an ace and his score is over 21 it changes the ace to a 1
def calculate_score(hand):
    score = sum(hand)
    if score > 21 and 11 in hand:
        hand.remove(11)
        hand.append(1)
    return sum(hand)

#starts the blackjack game when the user types !blackjack
async def blackjackgame(message, client):
    if message.content.startswith('!blackjack'):
        player_hands = {}
        player_scores = {}

#this adds the user into the game
        player_hands[message.author] = [deal_card(), deal_card()]
        player_scores[message.author] = calculate_score(player_hands[message.author])
#this adds the computer into the game
        computer_hand = [deal_card(), deal_card()]
        computer_score = calculate_score(computer_hand)

        #this ouputs the players score and the computers score
        def game_status():
            status = ""
            for player, hand in player_hands.items():
                status += f"{player.name}: {hand}, current score: {player_scores[player]}\n"
            status += f"Computer's first card: {computer_hand[0]}\n"
            return status

        await message.channel.send(game_status())

#this allows other players in the server to join, if no one joins within 10 seconds it just continues with the one player or how ever many join
        await message.channel.send("Type 'join' within 10 seconds to join the game.")
        try:
#when other users type join it deals them into the game
            while True: 
                join_message = await client.wait_for('message', timeout=10.0, check=lambda m: m.content.lower() == 'join')
                player_hands[join_message.author] = [deal_card(), deal_card()]
                player_scores[join_message.author] = calculate_score(player_hands[join_message.author])
                await message.channel.send(game_status())
        except asyncio.TimeoutError:
            pass

#while the game is not over it sends the user a message to hit or stand
        for player, hand in player_hands.items():
#if the player types stand it ends the game for them
            game_over = False  
#if the player types hit it give the player another card and asks them the question again 
            while not game_over:    
                await message.channel.send(f"{player.name}, type 'hit' to get another card, 'stand' to pass")
#it waits for the player to type hit or stand
                try: 
                    reply = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == player and m.channel == message.channel and m.content.lower() in ['hit', 'stand'])
                except asyncio.TimeoutError:
                    await message.channel.send(f"{player.name}, timeout")
                    break
#if the player types hit it gives a card to the player and asks the question again and shows the players score
                if reply.content.lower() == 'hit':
                    player_hands[player].append(deal_card())
                    player_scores[player] = calculate_score(player_hands[player])
                    await message.channel.send(f"{player.name}, your cards: {player_hands[player]}, current score: {player_scores[player]}")
#if the player types hit and the card that it gets brings the players total score over 21 it ends the game for the player and the player loses
                    if player_scores[player] > 21:
                        await message.channel.send(f"{player.name}, you went over 21. You lose!")
                        game_over = True
                elif reply.content.lower() == 'stand':
                    game_over = True
#while the computers score is less than 17 it will choose hit once it is 17 or over it will stand
        while calculate_score(computer_hand) < 17:
            computer_hand.append(deal_card())
#calculates the computers score
        computer_score = calculate_score(computer_hand)

#Shows the score of the player and the computer
        for player, hand in player_hands.items():
            response = f"{player.name}'s final hand: {hand}, final score: {player_scores[player]}\n"
            response += f"Computer's final hand: {computer_hand}, final score: {computer_score}\n"
#if your score is under 21 and the computers score went over 21 you win by default
            if computer_score  and player_scores[player] <= 21:
#if the computers score is under 21 and your score is also 21 and your score is less than the computers score you win
                response += "Computer went over 21. You win!"   
            elif player_scores[player] > computer_score and player_scores[player] <= 21:
                response += "You win!"
            elif player_scores[player] == computer_score and player_scores[player] <= 21:
                response += "It's a draw!"
            else:
                response += "You lose!"
                        
            await message.channel.send(response)