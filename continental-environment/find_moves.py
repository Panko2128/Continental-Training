# find_moves.py
import numpy as np
from .card import Card

# when looking for ways to form multiple melds, search first for all the straights, then the sets

# by default, call get_run_view for whatever meld(s)

# call run_to_set_view when all runs (0-3) have been created, except for when there are no sets to be made

# while in run view, each viable straight can be acquired through create runs, 
# and the numerical value of that action will correspond to the index that needs to be updated

# index 0 of the create_runs array corresponds to A,2,3,4 Hearts, or indices 0-2, 12 in the run_view array
# index 1 of the create_runs array corresponds to 2,3,4,5 Hearts, or indices 0-3 in the run_view array
# index 10 of the create_runs array corresponds to J,Q,K,A Hearts, or indices 9-12 in the r_v array
# index 11 of the create_runs array corresponds to A,2,3,4 Diamonds, or indices 13-15, 25 in the r_v array
    
# for a given straight in the create_runs array, the suit can be extracted by doing index // 11
# (suit * 13) + (index % 11) should result in the first index (of four) that need to be decremented

def post_run_game_state(game_state, action):
    """Processes the gamestate array after a player puts down a run
    
    The action parameter decides what run is played, and this function
    iterates through all the possible locations for each card in the run
    to figure out which to move to that player's run area

    Returns: 
    - updated gamestate array 
    """

    hand_public = get_curr_player(game_state)
    hand_private = hand_public + 100
    run_area = 20 + hand_public

    jokers_used = 0
    joker_represents = []

    zeroed_action = action - 8 # zeroed actions go from 0-43
    suit = zeroed_action // 11 # 0-10 gives 0, 11-21 gives 1, etc.
    rank = zeroed_action - (11 * suit)

    if rank == 0: # A, 2, 3, 4 - non-consecutive indices in gamestate array
        ace_index = 12 + 13 * suit
        two_index = 13 * suit
        three_index = 13 * suit + 1
        four_index = 13 * suit + 2
        run_card_indices = [ace_index, two_index, three_index, four_index]

    else: # regular run - consecutive indices in gamestate array
        bottom_index = 13 * suit + rank
        run_card_indices = [bottom_index + i for i in range(4)]

    # for each card in the run
        # access each of the three possible locations for that card
            # if the card's location is found to be the player's hand,
                # move it to the run area and stop looking for that card

            # if the card cannot be found in the player's hand,
                # increment the jokers_used count and store the card that
                # was joker subbed in the joker_represents array
    for index in run_card_indices:
        for n in range(3):
            card_pos = game_state[index + 54 * n]
            if card_pos == hand_public or card_pos == hand_private:
                game_state[index + 54 * n] = run_area
                break
            elif n == 2:
                jokers_used += 1
                joker_represents.append(index)

    joker_indices = [52, 53, 106, 107, 160, 161]

    # for each joker used
        # find a joker in the player's hand,
        # set its location to "substitute for card __ in a run"
        # using joker_represents to fill in the blank 
    for joker in range(jokers_used):
        for index in joker_indices:
            joker_loc = game_state[index]
            if joker_loc == hand_public or joker_loc == hand_private:
                game_state[index] = joker_represents.pop() + 32
                break
    
    assert(not joker_represents) 
    # all of the jokers used in the run should have been accounted for

    
    return game_state
        

def post_set_game_state(game_state, action):
    """Processes the gamestate array after a player puts down a set
    
    The action parameter decides what set is played, and this function
    iterates through all the possible locations for each card in the set
    to figure out which card to move to that player's set area

    Returns: 
    - updated gamestate array 
    """

    hand_public = get_curr_player(game_state)
    hand_private = hand_public + 100
    set_area = 10 + hand_public

    jokers_used = 3

    zeroed_action = action - 52 # zeroed actions go from 0-12
    
    # Index 0 in the gamestate array contains the location of the "first" 2 of
    # Hearts.  
    # 
    # - we can add 13 to the index to reach where the location of the "first"
    #   2 of Diamonds is stored, and repeat twice more for the remaining two
    #   suits: Clubs and Spades
    # 
    # - then, to account for the two jokers in the "first" deck we add 2 to 
    #   the current index, which brings us to where the location of the
    #   "second" 2 of Hearts is stored
    #
    # - we can go back to adding 13 three more times, then add 2 (for the 
    #   two jokers in the "second" deck), then 13 again three more times 
    #
    # - if we add all of the indices to a list, we should have all 12 
    #   possible indices where a card of the specified rank can be found

    first_index = zeroed_action

    set_card_indices = []

    for deck in range(3): # three decks total
        for suit in range(4): # four suits that the card could be in
            set_card_indices.append(first_index + (13 * suit) + (2 * deck))

    # for each possible index,
        # check if the card is in the player's hand
        # if it is, decrement the jokers_used variable
        # if the player moves 3 cards of the specified rank to their set area,
        # stop searching for additional copies
    for index in set_card_indices:
        card_loc = game_state[index]
        if card_loc == hand_public or card_loc == hand_private:
            game_state[index] = set_area
            jokers_used -= 1
        if jokers_used == 0: 
            # the player has moved 3 cards of the specified rank to their set area
            break

    joker_indices = [52, 53, 106, 107, 160, 161]

    # for each joker used
        # find a joker in the player's hand,
        # set its location to "substitute for card __ in a run"
        # using joker_represents to fill in the blank 
    for joker in range(jokers_used):
        for index in joker_indices:
            joker_loc = game_state[index]
            if joker_loc == hand_public or joker_loc == hand_private:
                game_state[index] = first_index + 84
                break

    assert(jokers_used != 3)
    
    return game_state


def post_add_to_run_game_state(game_state, action):
    """Processes gamestate after adding a card to the top or bottom of a run.
    
    Whether it is to the top or bottom of the run is determined by the action.
    The specific card to add is also determined by the action.

    Returns:
    - updated gamestate array
    """
    hand_public = get_curr_player(game_state)
    hand_private = hand_public + 100

    if action <= 104: # adding card to bottom of straight
        zeroed_action = action - 65
        suit = zeroed_action // 10 # 0-9 gives 0 (Hearts), 10-19 gives 1, etc.
        rank = zeroed_action - (10 * suit) # rank 0 = Ace, rank 1 = 2, etc.

        joker_used = False
        joker_represents = None

        # find the index of the card we are adding
        add_card_base_index = rank + (suit * 13) - 1
        if rank == 0: # ace is high card in terms of indexing
            add_card_base_index += 12

        actual_index = find_card_with_base_index(game_state, add_card_base_index)

        if actual_index == -1:
            joker_used = True
            joker_represents = add_card_base_index + 32
            actual_index = find_card_with_base_index(game_state, 52)
            


        # find the location of the card we are trying to add below
        # i.e. we are adding a 5 of Hearts, so look for the run area with
        #      the 6 of Hearts
        next_card_base_index = rank + (suit * 13)

        for n in range(3):
            next_card_loc = next_card_base_index + 54 * n
            if 21 <= next_card_loc <= 26:
                break

        if not next_card_loc:
            for n in range(3):
                next2_card_loc = game_state[next_card_base_index + 54 * n + 1]
                if 21 <= next2_card_loc <= 26:
                    if 
                    break
        
        if next2_card_loc:
            for n in range(3):
                next2_card_loc = next_card_base_index + 54 * n + 1
                if 21 <= next2_card_loc <= 26:
                    break




        game_state[card_to_add_index] = card_loc


    else: # adding a card to top of straight
        return 0

def run_subbed_joker(game_state, base_index):
    """Checks if there is a joker run-subbed for the card at base_index
    
    Returns:
    - int > 0: the joker at this index is a run substituted version of the
      indexed card

    or
    - -1: there is no joker that is run-subbed for this card
    """
    joker_indices = [52, 53, 106, 107, 160, 161]
    for j_index in joker_indices:
        if 


def find_card_with_base_index(game_state, base_index):
    """Returns the index of the current player's copy of a specific card

    The card to search for is denoted by base_index, referring to the
    first 53 indices in the gamestate array (0-52). since there are three
    decks total, the card specified could be tied to any of the three**
    related indices.
    If the base_index is 52, will search for a joker (6 possible indices)



    Returns:
    - integer >= 0 to denote the actual index where the player's copy
      has it's location stored
    - -1 if card cannot be found (indicating that a joker is used)
    """

    hand_public = get_curr_player(game_state)
    hand_private = hand_public + 100

    joker_indices = [52, 53, 106, 107, 160, 161]


    if base_index == 52: # joker!
        for index in joker_indices:
            card_loc = game_state[index]
            if card_loc == hand_private or card_loc == hand_public:
                return index

    for n in range(3):
        card_loc = game_state[base_index + n * 54]
        if card_loc == hand_public or card_loc == hand_private:
            actual_index = base_index + n * 54
            return actual_index
    
    return -1

def find_run_card_area(game_state, empty_index, side):
    """Locates the run specified by empty_index and side.

    Searches the game_state array for the specified run, starting with the
    card that is the furthest away. For example, when empty_index is 0 and
    side is "bottom", the function looks for all of the 6543 (Hearts) in the
    game_state array. Then, it looks for an empty spot in those locations.
    Returns:
    - location of the empty spot
    """
    
    run_areas = None
    location = None

    if side == "bottom":
        furthest_index = empty_index + 4

        for n in range(4):
            base_index = furthest_index - n # start with furthest
            run_areas = in_run_area(game_state, base_index)

            if len(run_areas) == 1:
                location = run_areas[0]
                break
            



def in_run_area(game_state, base_index):
    """Finds out which run area(s) a card is in
    
    Returns:
    - the run area(s) in which the card appears
    """
    found_in = []
    for n in range(3):
        card_loc = game_state[base_index + 54 * n]
        if 21 <= card_loc <= 26:
            found_in.append(card_loc)
    return found_in


# returns the run_view of the hand after the run indicated by "index" is played
def post_run_hand(run_view, index):
    suit = index // 11
    root = index % 11

    consec_indices = 4

    if root == 0: # A,2,3,4 run
        ace_index = 13 * suit + 12

        consec_indices = 3

        start = suit * 13

        if run_view[ace_index] > 0: # avoids negative numbers of cards due to joker use
            run_view[ace_index] -= 1

    else: # any other kind of run
        start = (suit * 13) + (root - 1)  

    for i in range(consec_indices):
        if run_view[start + i] > 0:
            run_view[start + i] -= 1

    
    return run_view

# returns the set_view of the hand after the set indicated by "index" is played
def post_set_hand(set_view, index):
    if get_set_view[index] < 3:
        get_set_view[index] = 0
    else:
        get_set_view[index] -= 3

    return get_set_view

# returns however many jokers are needed to complete each set (in array format)
def create_sets(set_view):
    
    set_arr = np.full(13, 3)

    for rank, num_cards in enumerate(set_view):
        if num_cards > 3:
            set_arr[rank] -= 3
        else:
            set_arr[rank] -= num_cards


    return set_arr

# returns however many jokers are needed to complete each run/straight (in array format)
# index 0 corresponds to A234 of Hearts, then 2345, etc. as laid out in the action phase
# section of the readme
def create_runs(run_view):
    
    run_arr = np.zeros(44)


    i = 0
    for suit in range(4):
        for str_start in range(10): # 2 - J
            run_arr[10*suit+str_start+1] = 4 - sum(min(run_view[i:i+4], 1))
            i += 1

        i += 2 # A, 2, 3, 4

        sub_sum = min(run_view[i], 1) + min(run_view[i-12], 1) + min(run_view[i-11], 1) + min(run_view[i-10], 1)
        run_arr[10*suit+str_start+1] = 4 - sub_sum

        i += 1 # index should be back at 2 of the next suit (if it exists)

    return run_arr


def any_playable(arr):
    for elem in arr:
        if elem == 1:
            return True
    return False

def find_down(game_state, round, stage):

    run_view = get_run_view(game_state, get_curr_player(game_state))
    jokers_held = get_jokers_held(game_state)

    match round:

        case 1:
            set_view = run_to_set_view(run_view)
            down_action = find_down_1(set_view, jokers_held)

        case 2:
            down_action = find_down_2(run_view, jokers_held)

        case 3:
            set_view = run_to_set_view(run_view)
            down_action = find_down_3(set_view, jokers_held, stage)

        case 4:
            down_action = find_down_4(run_view, jokers_held, stage)

        case 5:
            down_action = find_down_5(run_view, jokers_held, stage)

    return down_action


# ensure player isn't already down (in the environment)
# the find_down functions will correspond to indices 8-64 in the action space
def find_down_1(set_view, num_jokers_held):

    set_arr = create_sets(set_view)

    down_arr = np.zeros(57)

    for rank in range(13):
        if set_arr[rank] - min(num_jokers_held, 2) <= 0:
            down_arr[44 + rank] = 1

    return down_arr

def find_down_2(run_view, num_jokers_held):
    
    run_arr = create_runs(run_view)

    down_arr = np.zeros(57)

    for run_start in range(13):
        if run_arr[run_start] - min(num_jokers_held, 3) <= 0:
            down_arr[run_start] = 1

    return down_arr

def find_down_3(set_view, num_jokers_held, stage):
    if stage == 1:
        return find_down_1(set_view, num_jokers_held)
    else:
        down_arr = np.zeros(57)

        jokers_required = create_sets(set_view)

        first_down = find_down_1(run_view, num_jokers_held) # can I make any sets?

        for index, can_make in enumerate(first_down[44:]): 
            if can_make == 1: # if I can make one set,
                jokers_left = num_jokers_held - jokers_required[index]
                second_set_view = post_set_hand(set_view, index) # look at the hand after removing those cards
                if any_playable(find_down_1(second_set_view, jokers_left)): # if there is 1 or more playable second set, the action at index is legal
                    down_arr[44 + index] = 1

        return down_arr

# straight + set
def find_down_4(run_view, num_jokers_held, stage):
    if stage == 1:
        get_set_view = run_to_set_view(run_view)
        return find_down_1(set_view, num_jokers_held)
    else:
        down_arr = np.zeros(57)

        jokers_required = create_runs(run_view)

        first_down = find_down_2(run_view, num_jokers_held) # can I make any runs?

        for index, can_make in enumerate(first_down[:44]): 
            if can_make == 1: # if I can make one run,
                jokers_left = num_jokers_held - jokers_required[index]
                get_set_view = run_to_set_view(post_run_hand(run_view, index)) # look at the hand after removing those cards
                if any_playable(find_down_1(set_view, jokers_left)): # can I then make a set?
                    down_arr[index] = 1

        return down_arr

# straight + straight
def find_down_5(run_view, num_jokers_held, stage):
    if stage == 1:
        return find_down_2(run_view, num_jokers_held)
    else:
        down_arr = np.zeros(57)

        jokers_required = create_runs(run_view)

        first_down = find_down_2(run_view, num_jokers_held) # can I make any runs?

        for index, can_make in enumerate(first_down[:44]): 
            if can_make == 1: # if I can make one run,
                jokers_left = num_jokers_held - jokers_required[index]
                second_run_view = post_run_hand(run_view, index) # look at the hand after removing those cards
                if any_playable(find_down_2(second_run_view, jokers_left)): # can I make another run?
                    down_arr[index] = 1

        return down_arr


# returns an array of 1s and 0s corresponding to legal plays
# this array corresponds to indices 65 - 157 in the action space 
def find_play_cards(game_state):

    plays = np.zeros(93)

    # straights

    played_runs = played_runs(game_state)

    for suit in range(4):
        prev = played_runs[13*suit + 12]
        for rank in range(13): # 2 -> Ace
            curr = played_runs[13*suit + rank]
            if curr > prev and rank < 12:
                plays[10*suit + rank] = 1
            elif curr < prev and rank > 1:
                plays[10*suit + 40 + rank - 3] = 1
            prev = curr


    # sets
    played_sets = played_sets(game_state)

    for rank in range(13):
        plays[80 + rank] = played_sets[rank]

    return plays

# returns an array of 1s and 0s, 1s representing a valid joker sub (current player has
# that substituted card in their hand and can legally trade it)
#
# this array corresponds to indices 158 - 219 in the action space
def find_joker_exch(game_state):

    held_cards = get_run_view(game_state, get_curr_player(game_state))

    possible_subs = np.zeros(52)

    joker_indices = [53, 54, 106, 107, 160, 161]

    for index in joker_indices:
        if index >= 32 and index <= 83:
            card_index = index - 32
            if held_cards[card_index] > 0:
                possible_subs[card_index] = 1
        elif index >= 84 and index <= 97:
            for card_index in range(index - 84, 13, 52):
                if held_cards[card_index] > 0:
                    possible_subs[card_index] = 1

    return possible_subs


def find_discard_cards(game_state, owned_joker):
    hand = get_run_view(game_state, get_curr_player(game_state))

    for num_cards in hand:
        if num_cards > 0:
            num_cards = 1

    disc_actions = hand + [owned_joker]

# returns the inputted player's observation space
def player_sees(game_state, player_number):
    player_obs = np.zeros(171)

    hand_loc = player_number

    for i in range(162):
        card_loc = game_state[i]
        if card_loc < 101 or card_loc == hand_loc + 100:
            player_obs = card_loc
        whose = card_loc % 100
        if whose > 0 and whose <= 6:
            player_obs[164 + whose] += 1
    
    player_obs[162] = get_curr_player(game_state) # whose turn it is
    player_obs[163] = get_round(game_state) # what round it is
    player_obs[164] = get_hand_value(game_state) # 
    for i in range(165, 177):
        player_obs[i] = game_state[i]

    return player_obs

# run mode (straight mode) how many of each card is owned
def get_run_view(game_state, player_number): 
    hand_loc_value = player_number

    card_arr = np.zeros(52)

    for deck in range(3):
        for i in range(52):
            card_loc = game_state[i + 54*deck]

            if card_loc == hand_loc_value or card_loc == hand_loc_value + 100:
                card_arr[i] += 1
        
    
    return card_arr

# set mode: how many of each rank is owned (suit doesn't matter)
def get_set_view(game_state, player_number): 
    hand_loc_value = player_number

    card_arr = np.zeros(13)

    for deck in range(3):
        for i in range(52):
            rank = i % 13
            card_loc = game_state[i + 54* deck]

            if card_loc == hand_loc_value or card_loc == hand_loc_value + 100:
                card_arr[rank] += 1
    
    return card_arr

# 
def run_to_set_view(run_view_view):
    get_set_view = np.zeros(13)

    for i in range(52):
        rank = i % 13
        get_set_view[rank] += 1

# returns the array representation of onboard straights
def played_runs(game_state):

    card_arr = np.zeros(52)

    for deck in range(3):
        for i in range(52):
            card_loc = game_state[i + 54*deck]

            if card_loc >= 21 and card_loc <= 26:
                card_arr[i] += 1
        
        joker_loc = game_state[54*deck + 52]

        if joker_loc >= 32 and joker_loc <= 83:
            card_arr[joker_loc - 22] += 1

        joker_loc = game_state[54*deck + 53]

        if joker_loc >= 32 and joker_loc <= 83:
            card_arr[joker_loc - 22] += 1

    return card_arr

# returns the array representation of onboard sets
def played_sets(game_state):

    card_arr = np.zeros(13)

    for deck in range(3):
        for i in range(52):
            rank = i % 13
            card_loc = game_state[i + 54* deck]

            if card_loc >= 11 and card_loc <= 16:
                card_arr[rank] = 1
    
    return card_arr

# returns the number of jokers held by the current player
def get_jokers_held(game_state):

    hand_loc_value = game_state[162]

    j_count = 0

    joker_indices = [52, 53, 106, 107, 160, 161]

    for j_index in joker_indices:
        if game_state[j_index] == hand_loc_value or game_state[j_index] == hand_loc_value + 100:
            j_count += 1

    return j_count

# returns the point value of the current player's hand
def get_hand_value(game_state, player):


    hand = get_set_view(game_state, player)

    jokers_held = get_jokers_held(game_state)

    score = 0

    for num in range(13):
        hand[num] * Card.VALUE_ARR[num]

    score += jokers_held * Card.JOKER_VAL

    return score

# returns the number of the player whose turn it is
def get_curr_player(game_state):
    return game_state[162]

# returns the current round
def get_round(game_state):
    return game_state[163]


def get_phase(game_state):
    """Returns "draw" or "play" based on the phase stored in gamestate"""

    return game_state[177]

