# various helper functions will follow
import numpy as np
from card import Card


# sends card to discard pile
def to_discard(game_state, card):
    game_state[card.id] = 31

# sends card to player hand, publicly or privately depending on the "public" boolean
def to_hand(game_state, card, player, public):
    game_state[card.id] = player if public else player + 100

# deals num_cards
def deal(deck, n, game_state):
    for i in n:
        for player in range(6):
            to_hand(game_state, deck.pop(), player, False)

# calculates the players' scores for that round
def calc_scores(game_state):
    for i in range(162):
        card_loc = game_state[i] % 100
        if card_loc % 100 >= 1 and card_loc[i] % 100 <= 6:
            game_state[170 + card_loc] += i.get


# returns the index of the maximum value in the list (ties resolved by earliest appearance)
def find_max_index(masked_action):
    curr_max = 0
    
    for i, val in enumerate(masked_action):
        if val > curr_max:
            curr_max = val
            curr_max_index = i

    return curr_max_index


# returns an array that determines which players have priority during the draw phase (by index!)
# [3, 4, 5, 6, 1, 2] means that it is p3's turn, so they have the most prio, then p5, and lastly p2
def get_prio_list(curr_player):
    prio_list = [curr_player]

    player = curr_player

    for num in range(5):
        if player == 6:
            player = 1
        else:
            player += 1
        prio_list.append(player)

    return player


def change_hand_size(game_state, player, delta):
    """Adjusts a player's hand size in the gamestate array

       Amount to change by is based on parameter delta (a positive or negative integer)
    """
    game_state[player + 164] += delta

def change_to_draw_phase(game_state):
    """Changes the phase element to 0 (draw)"""

    game_state[177] = 0


def change_to_play_phase(game_state):
    """Changes the phase element to 1 (play)"""

    game_state[177] = 1


def find_discard_pile_top(game_state):
    """Finds the index of the card on top of the discard pile"""
    for i, location in enumerate(game_state):
        if location == 30:
            return i
    return -1

