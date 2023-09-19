import numpy as np
from utils import *
from find_moves import *
from deck import Deck


def get_action_mask(game_state, stage, down_status, owned_joker):
    """Returns a mask corresponding to legal actions in that game state 
    
    In the draw phase, returns a mask for each player, based on turn order.
    In the play phase, returns a single mask for the current player based on round, held cards, jokers, etc.
    See README for action descriptions.

    Returns one of the following:
    - array (len=6) of int arrays (len=8)
    - array (len=272)
    """
    if get_phase(game_state) == "draw":
        return get_draw_action_masks(get_prio_list(get_curr_player(game_state)))
    else: # play phase
        
        return get_play_action_mask(game_state, get_round(game_state), stage, down_status, owned_joker)


def get_action(phase, actions, mask):
    """ Performs AND operation elementwise between action and mask arrays
    
    In the draw phase, returns an array containing each player's desired action
    In the play phase, returns the current player's selected action

    Returns one of the following:
    - array (len=6) of ints
    - int
    """
    
    if not phase:
        player_actions = np.zeros(6)
        for i in range(6):
            player_actions[i] = np.multiply(mask[i], actions[i])
        return player_actions

    else:
        masked_action = np.multiply(mask, actions)
        return find_max_index(masked_action)


def process_action(game_state, action):
    """Carries out the legal actions chosen by players
    
    In both the play and draw phases, updates card positions in the gamestate
    array as well as  various other tracking variables like ... ADD MORE HERE

    Returns:
    - new game_state array
    - ADD MORE HERE
    """
    

    if get_phase(game_state):

    else: # play phase


def get_draw_action_masks(prio_list):
    """Creates the action mask for each player based on whose turn it is (illustrated by priority list)

    Returns:
    - array of length 6, the elements of which are arrays of length 273 (the elements starting at index 8 are zeroed)    
    """
    mask_array = np.zeros(6)
    for i, prio in enumerate(prio_list):
        sub_array = np.zeros(273)
        sub_array[0] = 1
        sub_array[7] = 1
        for p in prio_list[i + 1:]:
            sub_array[p] = 1

        mask_array[prio - 1] = sub_array

    return mask_array


def get_play_action_mask(game_state, stage, down_status, owned_joker):
    """Finds all legal actions for the current player based on held cards, round, etc.

    Returns:
    - array of length 273, representing the complete action mask for the current player
    """
    
    # first, calculate mask without regard for what cards are held by the current player
    # based on round, phase and "down stage" (ex. in round 3, have you already played your first set or not)
    time_based_mask = np.zeros(273)
    down_range = (8 , 65)
    play_range = (65 , 158)
    joker_exch_range = (158, 220)
    discard_range = (220, 272)
    time_based_mask[272] = 1 # discarding a Joker is allowed by default

    if down_status == 0: # player is not down
        # allow put down, discard, joker exchange
        # prevent playing any cards
        for i in range(down_range):
            time_based_mask[i] = 1
        for i in range(joker_exch_range):
            time_based_mask[i] = 1
        for i in range(discard_range):
            time_based_mask[i] = 1

        # prevent discarding an joker gained in an illegal exchange
        if owned_joker == False:
            time_based_mask[272] = 0

    elif down_status == 1: # player is putting down
        # allow put down, joker exchange
        # prevent playing/discarding any cards
        for i in range(down_range):
            time_based_mask[i] = 1
        for i in range(joker_exch_range):
            time_based_mask[i] = 1
        
        time_based_mask[272] = 0 # prevent joker discard (no discards allowed)

    else: # player has already put down
        # allow playing or discarding any cards, as well as joker exchange
        # prevent putting down
        for i in range(play_range):
            time_based_mask[i] = 1
        for i in range(joker_exch_range):
            time_based_mask[i] = 1
        for i in range(discard_range):
            time_based_mask[i] = 1
        
    # then, calculate legal moves solely based on what cards are in the current player's hand,
    # as well as jokers that have been played, sets/runs that are on the board
    hand_draw_mask = np.zeros(8)
    hand_down_mask = find_down(game_state, get_round(game_state), stage)
    hand_play_mask = find_play_cards(game_state)
    hand_joker_exch_mask = find_joker_exch(game_state)
    hand_discard_mask = find_discard_cards(game_state, owned_joker)

    hand_based_mask = np.concatenate(hand_draw_mask, hand_down_mask, 
                                     hand_play_mask, hand_joker_exch_mask, 
                                     hand_discard_mask)
    

    return np.multiply(time_based_mask, hand_based_mask)


def get_draw_actions(actions, action_masks):
    """Creates the array containing each players action "bid" in the draw phase
    
    Returns:
    - array of length 6 of ints, representing each player's desired action"""

    bids = np.zeros(6)

    for i in range(6):
        bids[i] = find_max_index(np.multiply(actions[i], action_masks[i]))
        # the max index should be < 8

    return bids


def who_gets_discard(prio_list, actions):
    """Computes which player is getting the card on top of the discard pile

    Returns:
    - int 1-6 inclusive, representing a player number
    """

    deny_tuples = []

    for p in prio_list:
        action = actions[p - 1]
        if action == 0:
            for denier, denied in deny_tuples:
                if denied == p:
                    return denier
            return p
        
        elif action >= 1 and action <= 6:
            deny_tuples.append(p, action)

    return 0


def process_draw_action(game_state, action, deck):
    """Processes the actions legally selected by players in the draw phase
    
    Returns:
    - array of length 176, representing the updated gamestate
    - ADD MORE HERE
    """
        
    curr_player = get_curr_player(game_state)

    discard_top_index = find_discard_pile_top(game_state)
    assert(discard_top_index != -1)
    
    # figure out who gets the discard card:
    # - if curr_player gets it, move it to their hand (public)
    # - if nobody wants it, draw a card to curr_player's hand (private)
    # - if a player other than the current one gets it, move it to their
    #   hand (public) and draw a card to that player's hand and 
    #   curr_player's hand (both private)
    #
    # update hand size(s)
    
        
    who_gets = who_gets_discard(get_prio_list(curr_player), action)
        
    if who_gets == curr_player or deck.cards_left() == 1:
        game_state[discard_top_index] = curr_player
        change_hand_size(game_state, curr_player, 1)

    elif who_gets == 0:
        drawn_card_index = deck.draw_card()
        game_state[drawn_card_index] = curr_player + 100

        # top of discard pile is now "dead" - all players know that card is "unavailable"
        game_state[discard_top_index] += 1

        change_hand_size(game_state, curr_player, 1)

    else:

        penalty_index = deck.draw_card()
        drawn_card_index = deck.draw_card()

        game_state[penalty_index] = who_gets + 100
        game_state[drawn_card_index] = curr_player + 100

        change_hand_size(game_state, curr_player, 1)
        change_hand_size(game_state, who_gets, 2)

    change_to_play_phase(game_state)

    # return new game_state 

    return game_state
    ##########################################################################


def process_play_action(game_state, action, stage):
    """Processes the action selected by curr_player in the play phase
    
    Returns:
    - array of length 176, representing the updated gamestate
    - ADD MORE HERE
    """
    if action <= 51: # put down straight
        game_state = post_run_game_state(game_state, action)


    elif action <= 64: # put down set
        game_state = post_set_game_state(game_state, action)

    elif action <= 144: # add card to a run

    elif action <= 157: # add card to a set

    elif action <= 219: # exchange card for joker

    else: # discard 

    
