# TITLE: Montex - Simulated Texas Hold 'Em Poker Assistant
# AUTHOR: Andrew Smith
# DATE: 01/31/2024 (last updated)
# ABOUT: Determine the probability of winning a game of Texas Hold 'Em after entering card and player data. 

import random
import numpy as np
import time

# 0. Input Simulation Variables
# introduction text
print("MONTEX - SIMULATED POKER ASSISTANT")
print("Written by Andrew Smith")
print("Version 1.0 Copyright 2024 \n")

# input parameters
print("Input Parameters")
ops = int(input("> Number of Opponents: ")) # number of opponents playing against
print("")
print("Enter Pocket Cards")
p_card_1 = str(input("> Pocket Card #1: ")) # first pocket card
p_card_2 = str(input("> Pocket Cards #2: ")) # second pocket card

# initialize variables
runs = 1000 # default number of simulations to perform 
wins = 0 # number of winning hands
deck_org = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C', '13C', '14C', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', '11D', '12D', '13D', '14D', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H', '13H', '14H', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S', '13S', '14S'] # default deck of cards, original deck to be copied in simulations



# 1. Create Player Hand
def str_to_card(txt):
    # Convert string data to player card information
    # 2-10 = #, 11 = Jack (J), 12 = Queen (Q), 13 = King (K), 14 = Ace (A) || Clubs (C), Diamonds (D), Hearts (H), Spades (S)
    suit = txt[-1].upper() # last character of entry -> convert to uppercase
    value = txt[:-1].upper() # remaining characters are card value -> convert to uppercase if possible
    # convert face card values to numbers
    if value == "J":
        value = 11
    elif value == "Q":
        value = 12
    elif value == "K":
        value = 13
    elif value == "A":
        value = 14
    return str(value)+str(suit)
    
p_cards_org = [str_to_card(p_card_1), str_to_card(p_card_2)] # define player hand (original), convert input strings to card values. set as original as simulation will copy hand multiple times
# remove cards from the deck
deck_org.remove(p_cards_org[0])
deck_org.remove(p_cards_org[1])
     
     
     
# 2. Global Functions
# Convert hand to card values and suits
def cardValues(hand):
    # Take array of card values and convert into array of numerical values without suits
    # OUTPUT: array of ints, O(nlogn)
    num_hand = []
    for i in range(len(hand)): # go through each card
        num_hand.append(int(hand[i][:-1])) # remove suit, convert to integer
    num_hand.sort() # arrange in order
    return num_hand


def cardSuits(hand):
    # Take array of card values and convert into array of suits
    # OUTPUT: array of string characters, O(nlogn)
    suit_hand = []
    for i in range(len(hand)): # go through each card
        suit_hand.append(hand[i][-1]) # get last character for suit name
    suit_hand.sort() # arrange in order
    return suit_hand


# Check each rank of poker hands
def highCard(hand):
    # Return highest card value of a hand
    # OUTPUT: Card Value, O(n)
    hand_vals = cardValues(hand)
    return max(hand_vals)


def pairs(hand):
    # Check duplicate cards and return pair type and highest pair value
    # OUTPUT: [True/False, Type, Card Value], O(nlogn)
    hand_vals = cardValues(hand)
    
    # get card frequency
    freq = {i:hand_vals.count(i) for i in hand_vals} # create dictionary with frequency of each card occurence
    unique = list(freq.keys()) # unique cards (key list)
    counts = list(freq.values()) # number of occurences (value list)
    
    # reverse list to allow for doublets and triplet pairs to be sorted
    unique_two = unique.copy()
    unique_two.reverse()
    counts_two = counts.copy()
    counts_two.reverse()
    
    # sort list to find highest and second highest frequency card
    counts_sorted = counts.copy()
    counts_sorted.sort() # sorted frequency list -> UPDATE to reduce time complexity
    
    # determine pair type based on frequency list
    first = counts_sorted[-1] # most frequent card
    second = counts_sorted[-2] # 2nd most frequent card
        
    if first == 4:
        p = counts.index(4) # index position of card
        return [True, "four of a kind", unique[p] ]
    
    elif first == 3:
        p = counts.index(3) # index position of card
        if second == 1:
            return [True, "three of a kind", unique[p] ]
        elif second == 2:
            return [True, "full house", unique[p] ]
        elif second == 3:
            q = counts_two.index(3) # reverse list, q = index of second triplet card
            if unique_two[q] > unique[p]: # ex: AAABBBC, report B if B>A
                return [True, "full house", unique_two[q] ]
            else: # ex: AAABBC report A if A>B
                return [True, "full house", unique[p] ]
                
    elif first == 2:
        p = counts.index(2) # index position of card
        if second == 1: 
            return [True, "one pair", unique[p] ]
        elif second == 2:
            q = counts_two.index(2) # reverse list, q = index of second doublet card
            if(unique_two[q] > unique[p]): # ex: AABBCDE, report B if B>A
                return [True, "two pair", unique_two[q] ]
            else: # ex: AABBCDE report A if A>B
                return [True, "two pair", unique[p] ]
        
    else: # no pairs found
        return [False, "none", 0]


def isStraight(hand):
    # Determine whether a hand has a straight in it and if so, returns highest straight value
    # OUTPUT: [True/False, Card Value], O(n)

    cv = cardValues(hand) # get value of each card and sort
    cv = np.unique(cv) # remove duplicates 
   
    for i in range(len(cv)-1, len(cv)-4, -1): # check each straight starting point (start from end to get highest straight card value in case 6 are in a row)
        if cv[i] == cv[i-1] + 1 and cv[i-1] == cv[i-2] + 1 and cv[i-2] == cv[i-3] + 1 and cv[i-3] == cv[i-4] + 1:
            return [True, cv[i]]
        
    return [False, 0]
 

def isFlush(hand):
    # Determine whether a hand has a flush in it and if so, return highest flush value
    # OUTPUT: [True/False, Suit, Card Value], O(n)
    
    hand_suits = cardSuits(hand)
    
    # get suit frequency
    freq = {i:hand_suits.count(i) for i in hand_suits} # create dictionary with frequency of each card occurence
    unique = list(freq.keys()) # unique suits (key list)
    counts = list(freq.values()) # number of occurences (value list)
    
    if max(counts) >= 5:
        p = counts.index(max(counts)) # which suit has 5 or more cards
        suit = unique[p] # flush suit
        max_card = 0 # value of highest card in flush suit
        for i in hand:
            if i[-1] == suit and int(i[:-1]) > max_card: # if card has flush suit and greater than current max
                max_card = int(i[:-1])               
        return [True, suit, max_card]
    
    else:
        return [False, 0, 0]
    
    return [False, 0, 0] # return if havent before
    

def straightFlush(hand):
    # Check if a hand has a straight flush and if so, returns highest card value
    # OUTPUT: [True/False, Card Value], O(n)
    
    flush = isFlush(hand) # get return array of flush check
    suit = "" # flush suit
    sf_cards = [] # cards part of the straight flush
    
    if flush[0] == True: # if the hand is a flush
        suit = flush[1]
        
        # get cards only in flush suit
        for i in hand: # loop over each card
            if i[-1] == suit:
                sf_cards.append(i) # add card to straight flush cards
                
        straight = isStraight(sf_cards) # check if these cards are straight and get highest card
        if straight[0] == True: # if straight, then this is a straight flush
            return [True, straight[1]] # return top card
        else: # if not a straight, return false
            return [False, 0]
        
    else: # if not a flush, return false
        return [False, 0]
    
    return [False, 0] # return if havent before
        
    
def handRank(hand):
    # Get the ranking of the hand based on all the different poker hands possible
    # 1 = high card, 2 = one pair, 3 = two pair, 4 = three of a kind, 5 = straight, 6 = flush, 7 = full house, 8 = four of a kind, 9 = straight flush, 10 = royal flush
    # OUTPUT: [Hand Rank, Card Value], O(nlogn)
    
    score = [1, highCard(hand)] # [hand rank, card value], high card is set as default
        
    pair = pairs(hand) # check pairs
    if pair[0] == True: # pair is present
        if pair[1] == "one pair":
            score = [2, pair[2]]
        elif pair[1] == "two pair":
            score = [3, pair[2]]
        elif pair[1] == "three of a kind":
            score = [4, pair[2]]
        elif pair[1] == "full house":
            score = [7, pair[2]]
            return score
        elif pair[1] == "four of a kind":
            score = [8, pair[2]]
            return score
    
    straight = isStraight(hand) # checks straights
    if straight[0] == True: # straight is present
        score = [5, straight[1]]
    
    flush = isFlush(hand) # checks flush
    if flush[0] == True: # flush is present
        straight_flush = straightFlush(hand) # check if straight flush
        if straight_flush[0] == True: # straight flush
            if straight_flush[1] == 14: # royal flush
                score = [10, 14]
            else: # straight flush
                score = [9, straight_flush[1]]
        else: # flush
            score = [6, flush[2]] 
    
    return score
    
    
def rank_to_text(rank):
    # Convert hand rank number to name type
    # OUTPUT: string
    val = int(rank)
    rank_names = ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"]
    return rank_names[val - 1]


def win_results_display(num_wins, num_opponents):
    # Display win liklihood and compare it to random liklihood to show loss/gain of odds
    win_pct = wins / runs # win percentage -> # wins / # hands
    exp_pct = 1 / (ops+1) # expected number of win percentage
    gain_pct = win_pct - exp_pct # gained percentage is the difference
    if(gain_pct > 0):
        print("Winning Percentage: " + str("{:.3f}%".format( 100*win_pct )) + " (+" + str("{:.3f}%".format(100*gain_pct) ) + ")" ) # add positive sign
    else:
        print("Winning Percentage: " + str("{:.3f}%".format( 100*win_pct )) + " (" + str("{:.3f}%".format(100*gain_pct) ) + ")" ) # negative value
    return
    
   
    
# 3. Pre-Flop Monte Carlo Simulation
p_cards = p_cards_org # copy player cards

for i in range(runs):
    # Reset and Initialize Variables
    p_hand = [] # player hand (all 7)
    o_cards = [] # opponents' cards
    o_hands = [] # opponent hands
    m_cards = [] # middle (community)
    
    # Deal Cards
    deck = deck_org # copy deck
    random.shuffle(deck) # shuffle deck
    # set opponent hands (individual)
    for j in range(ops):
        o_cards.append( [ deck[0], deck[1] ] ) # give top two cards
        deck = deck[2:] # remove dealt cards
    # deal middle cards (community)
    m_cards = deck[0:5]
    deck = deck[5:] # remove dealt cards
    
    # Define Hands
    # player hand (7 cards)
    p_hand = p_cards + m_cards # add middle cards to hand
    # opponent hands (7 cards each)
    for j in range(ops):
        o_hands.append( o_cards[j] + m_cards ) # add middle cards to each opponents hand
    
    # Evaluate Winning Hands
    # get hand rank of each player
    p_score = handRank(p_hand) # player scores -> [hand rank, card value]
    o_scores = [] # opponent scores
    for j in range(ops):
        o_scores.append( handRank(o_hands[j]) ) # get score of each opponent hand
    # check if win
    for j in range(ops):
        if p_score[0] >= o_scores[j][0]: # win/tie
            if p_score[0] == o_scores[j][0]: # player tied with opponent
                if p_score[1] > o_scores[j][1]: # player won
                    pass # player beat opponent, check next opponent
                elif p_score[1] < o_scores[j][1]: # player lost
                    break # exit for loop if player loses
                else: # tie 
                    break # count ties as a loss, go to next opponent
            else:
                pass # if player does not lose, keep checking other opponents
        else: # player lost
            break # exit for loop if player loses
        
        if j == ops-1: # player has beaten all opponent hands
            wins += 1 # add to win count
    
    
    
# 4. Calculate Pre-Flop Results
print("")
win_results_display(wins, ops)



# 5. Enter Flop Cards
print("")
print("Enter Flop Cards")
flop_card_1 = str(input("> Flop Card #1: ")) # first flop card
flop_card_2 = str(input("> Flop Card #2: ")) # second flop card
flop_card_3 = str(input("> Flop Card #3: ")) # third flop card
flop_cards = [str_to_card(flop_card_1), str_to_card(flop_card_2), str_to_card(flop_card_3)] # save flop cards
# remove flop cards from deck
deck_org.remove(flop_cards[0])
deck_org.remove(flop_cards[1])
deck_org.remove(flop_cards[2])

# display current player hand
current_hand = p_cards_org + flop_cards # create current player hand
hand_rank_temp = handRank(current_hand)[0] # current hand rank of player
print("")
print("Current Hand: " + str(rank_to_text(hand_rank_temp)) )



# 6. Flop Monte-Carlo Simulation
p_cards = p_cards_org # copy player cards
wins = 0 # reset win counter

for i in range(runs):
    # Reset and Initialize Variables
    p_hand = [] # player hand (all 7)
    o_cards = [] # opponents' cards
    o_hands = [] # opponent hands
    m_cards = [] # middle (community)
    
    # Deal Cards
    deck = deck_org # copy deck
    random.shuffle(deck) # shuffle deck
    # set opponent hands (individual)
    for j in range(ops):
        o_cards.append( [ deck[0], deck[1] ] ) # give top two cards
        deck = deck[2:] # remove dealt cards
    # deal middle cards (community)
    m_cards = flop_cards + deck[0:2] # use known cards + 2 random cards for turn and river
    deck = deck[2:] # remove dealt cards
    
    # Define Hands
    # player hand (7 cards)
    p_hand = p_cards + m_cards # add middle cards to hand
    # opponent hands (7 cards each)
    for j in range(ops):
        o_hands.append( o_cards[j] + m_cards ) # add middle cards to each opponents hand
    
    # Evaluate Winning Hands
    # get hand rank of each player
    p_score = handRank(p_hand) # player scores -> [hand rank, card value]
    o_scores = [] # opponent scores
    for j in range(ops):
        o_scores.append( handRank(o_hands[j]) ) # get score of each opponent hand
    # check if win
    for j in range(ops):
        if p_score[0] >= o_scores[j][0]: # win/tie
            if p_score[0] == o_scores[j][0]: # player tied with opponent
                if p_score[1] > o_scores[j][1]: # player won
                    pass # player beat opponent, check next opponent
                elif p_score[1] < o_scores[j][1]: # player lost
                    break # exit for loop if player loses
                else: # tie 
                    break # count ties as a loss, go to next opponent
            else:
                pass # if player does not lose, keep checking other opponents
        else: # player lost
            break # exit for loop if player loses
        
        if j == ops-1: # player has beaten all opponent hands
            wins += 1 # add to win count
    
    
    
# 7. Calculate Flop Results
win_results_display(wins, ops)



# 8. Enter Turn Card
print("")
print("Enter Turn Card")
turn_card = str_to_card( str(input("> Turn Card: ")) ) # turn card -> convert to card
# remove turn card from deck
deck_org.remove(turn_card)

# display current player hand
current_hand = p_cards_org + flop_cards + [turn_card] # create current player hand
hand_rank_temp = handRank(current_hand)[0] # current hand rank of player
print("")
print("Current Hand: " + str(rank_to_text(hand_rank_temp)) )



# 9. Turn Monte-Carlo Simulation
p_cards = p_cards_org # copy player cards
wins = 0 # reset win counter

for i in range(runs):
    # Reset and Initialize Variables
    p_hand = [] # player hand (all 7)
    o_cards = [] # opponents' cards
    o_hands = [] # opponent hands
    m_cards = [] # middle (community)
    
    # Deal Cards
    deck = deck_org # copy deck
    random.shuffle(deck) # shuffle deck
    # set opponent hands (individual)
    for j in range(ops):
        o_cards.append( [ deck[0], deck[1] ] ) # give top two cards
        deck = deck[2:] # remove dealt cards
    # deal middle cards (community)
    m_cards = flop_cards + [turn_card] + [deck[0]]
    deck = deck[1:] # remove dealt cards
    
    # Define Hands
    # player hand (7 cards)
    p_hand = p_cards + m_cards # add middle cards to hand
    # opponent hands (7 cards each)
    for j in range(ops):
        o_hands.append( o_cards[j] + m_cards ) # add middle cards to each opponents hand
    
    # Evaluate Winning Hands
    # get hand rank of each player
    p_score = handRank(p_hand) # player scores -> [hand rank, card value]
    o_scores = [] # opponent scores
    for j in range(ops):
        o_scores.append( handRank(o_hands[j]) ) # get score of each opponent hand
    # check if win
    for j in range(ops):
        if p_score[0] >= o_scores[j][0]: # win/tie
            if p_score[0] == o_scores[j][0]: # player tied with opponent
                if p_score[1] > o_scores[j][1]: # player won
                    pass # player beat opponent, check next opponent
                elif p_score[1] < o_scores[j][1]: # player lost
                    break # exit for loop if player loses
                else: # tie 
                    break # count ties as a loss, go to next opponent
            else:
                pass # if player does not lose, keep checking other opponents
        else: # player lost
            break # exit for loop if player loses
        
        if j == ops-1: # player has beaten all opponent hands
            wins += 1 # add to win count
    
    
    
# 10. Calculate Turn Results
win_results_display(wins, ops)



# 11. Enter River Card
print("")
print("Enter River Card")
river_card = str_to_card( str(input("> River Card: ")) ) # river card -> convert to card
# remove river card from deck
deck_org.remove(river_card)

# display current player hand
player_hand = p_cards_org + flop_cards + [turn_card,river_card] # create final player hand
hand_rank_temp = handRank(player_hand)[0] # hand rank of player
print("")
print("Current Hand: " + str(rank_to_text(hand_rank_temp)) )



# 12. River Monte-Carlo Simulation
wins = 0 # reset win counter
m_cards = flop_cards + [turn_card,river_card] # define middle cards
p_score = handRank(player_hand) # automatically define player hand and score

for i in range(runs):
    # Reset and Initialize Variables
    o_cards = [] # opponents' cards
    o_hands = [] # opponent hands
    
    # Deal Cards
    deck = deck_org # copy deck
    random.shuffle(deck) # shuffle deck
    # set opponent hands (individual)
    for j in range(ops):
        o_cards.append( [ deck[0], deck[1] ] ) # give top two cards
        deck = deck[2:] # remove dealt cards
    
    # Define Hands
    # opponent hands (7 cards each)
    for j in range(ops):
        o_hands.append( o_cards[j] + m_cards ) # add middle cards to each opponents hand
    
    # Evaluate Winning Hands
    # get hand rank of each player
    o_scores = [] # opponent scores
    for j in range(ops):
        o_scores.append( handRank(o_hands[j]) ) # get score of each opponent hand
    # check if win
    for j in range(ops):
        if p_score[0] >= o_scores[j][0]: # win/tie
            if p_score[0] == o_scores[j][0]: # player tied with opponent
                if p_score[1] > o_scores[j][1]: # player won
                    pass # player beat opponent, check next opponent
                elif p_score[1] < o_scores[j][1]: # player lost
                    break # exit for loop if player loses
                else: # tie 
                    break # count ties as a loss, go to next opponent
            else:
                pass # if player does not lose, keep checking other opponents
        else: # player lost
            break # exit for loop if player loses
        
        if j == ops-1: # player has beaten all opponent hands
            wins += 1 # add to win count
    
    
    
# 13. Calculate River Results
win_results_display(wins, ops)