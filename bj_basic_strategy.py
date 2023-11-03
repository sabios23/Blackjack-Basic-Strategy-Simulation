import random

card_symbols = ["hearts", "clubs", "spades", "diamonds"]
card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
my_deck = []

def bj_value(value):
    if value == "A":
        return 11
    elif value == "K" or value == "Q" or value == "J" or value == "10":
        return 10
    else:
        return int(value)

def create_deck():
    deck = []
    for symbol in card_symbols:
        for value in card_values:
            card = {
                "value": value, 
                "symbol": symbol,
                "blackjack_value": bj_value(value) 
            }
            deck.append(card)
    random.shuffle(deck)
    return deck

def compute_score(cards):
    score = 0
    number_of_aces = 0

    for card in cards:
        if card["value"] == "A":
            number_of_aces += 1 

    for card in cards:
        score += card["blackjack_value"]

    while number_of_aces > 0 and score > 21:
        score -= 10
        number_of_aces -= 1
    return score

# 1 - HIT
# 2 - STAY
# 3 - Double Down (not implemented)
# 4 - SPLIT (not implemented)
def basic_startegy(player_hand, dealer_card):

    player_score = compute_score(player_hand)
    dealer_score = dealer_card["blackjack_value"]

    if len(player_hand) == 2:
        if(player_hand[0]["value"] == player_hand[1]["value"]):
            if(player_hand[0]["blackjack_value"] >= 2 and player_hand[0]["blackjack_value"] <=8 or player_hand[0]["blackjack_value"] == 11):
                return 1
            else:
                return 2

        if(player_hand[0]["blackjack_value"] == 11 or player_hand[1]["blackjack_value"] == 11):  
            if(player_score >= 13 and player_score < 18):
                return 1
            else:
                return 2          
    
    if player_score >= 5 and player_score <= 11:
        return 1
    if player_score == 12 and (dealer_score == 2 or dealer_score == 3):
        return 1
    if (player_score >= 12 and player_score <= 16) and (dealer_score >= 7 and dealer_score <= 11):
        return 1 
    if player_score >= 17:
        return 2
    if (player_score >= 13 and player_score <= 16) and dealer_score <= 6:
        return 2
    if player_score == 12 and (dealer_score >=4 and dealer_score <=6):
        return 2

def evaluate_game(player, dealer):
    global wins
    global losses
    global draws
    if player > 21:
        losses += 1
        return -1
    elif dealer > 21:
        wins += 1
        return 1
    elif player > dealer:
        wins += 1
        return 1
    elif dealer > player:
        losses += 1
        return -1
    else:
        draws +=1
        return 0

def log_game(player_hand, dealer_hand, game_result):
    if game_result == 1:
        print("Player WINS", file = f)
    elif game_result == -1:
        print("Dealer WINS", file = f)
    else:
        print("DRAW", file = f)

    print("Player -", compute_score(player_hand), file = f)
    for card in player_hand:
        print(card["value"], card["symbol"], file = f)
    print("Dealer -", compute_score(dealer_hand), file = f)
    for card in dealer_hand:
        print(card["value"], card["symbol"], file = f)
    print("--------------------------", file = f)

def game():
    # -------------------------------
    # init
    my_deck = create_deck()
    player = []
    dealer = []

    # -------------------------------
    # dealing initial cards
    player.append(my_deck.pop())
    dealer.append(my_deck.pop())
    player.append(my_deck.pop())
    dealer.append(my_deck.pop())

    # -------------------------------
    # player play
    while(basic_startegy(player, dealer[0]) == 1):
        player.append(my_deck.pop())
    player_score = compute_score(player)

    # -------------------------------
    # dealer play
    dealer_score = compute_score(dealer)
    if(player_score <= 21):
        while dealer_score < 17:
            dealer.append(my_deck.pop())
            dealer_score = compute_score(dealer)

    # -------------------------------
    # evaluating the game for collecting stats
    result = evaluate_game(player_score, dealer_score)

    # -------------------------------
    # logging results
    log_game(player, dealer, result)

wins = 0
losses = 0
draws = 0
f = open('log.txt', 'w')

for games in range(10000):
    game()

print("wins:", wins)
print("losses:", losses)
print("draws:", draws)
print("winrate =", wins / (wins + losses + draws) * 100, "%")
f.close()