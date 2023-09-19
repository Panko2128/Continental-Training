# text
# player observations are as follows:
#
# The game_state array tracks the location of all 54 cards by having an index that corresponds to each card
#  
#   indices        |  meaning, or what card is represented
#  ________________|___________________________________________________
#  indices 0-12    |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Hearts) 
#  indices 13-25   |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Diamonds)
#  indices 26-38   |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Clubs)
#  indices 39-51   |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Spades)
#  indices 52-53   |  joker, joker
#                  |
#  indices 54-66   |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Hearts) 
#  indices 67-79   |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Diamonds)
#  indices 80-92   |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Clubs)
#  indices 93-105  |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Spades)
#  indices 106-107 |  joker, joker

#  indices 108-120 |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Hearts) 
#  indices 121-133 |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Diamonds)
#  indices 134-146 |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Clubs)
#  indices 147-159 |  2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, Ace (Spades)
#  indices 160-161 |  joker, joker 
# 
#  index 162       |  whose turn it is
#  index 163       |  current round
#  index 164       |  that player's hand total
#  indices 165-170 |  all players' hand sizes
#  indices 171-176 |  all players' running point totals
#  index 177       |  phase


# the values stored at these indices correspond to locations as follows:

# player 1 == p1

#    value    |   meaning
#  ___________|___________________________________________________________
#  0          | deck
#  1 - 6      | p1's hand - p6's hand (publicly picked up cards)
#  11 - 16    | p1's set area - p6's set area (anyone can play onto these)
#  21 - 26    | p1's straight area - p6's straight area (anyone can play onto these)
#  30         | discard pile top (what can get picked up in the draw phase)
#  31         | discard pile
#  32-83      | this Joker is a straight sub for card at index (value - 32)
#  84-97      | this Joker is a set sub for card with rank (value - 84) 
#             | i.e. 2, 3, 4, 5, 6, 7, 8, 9, 10, 11=J, 12=Q, 13=K, 14=Ace
#             | 
#  101 - 106  | p1's hand - p6's hand (private)


# returns a tuple, the first element being an array of length 13 
# (corresponding to ranks 2-10, J, Q, K, A)
#
#   - elements will be represent how many jokers are required to make that set, 
#     (negatives meaning they have >3 of that card)
#
# the second element will be the number of Jokers currently owned
#
# note: set of only jokers prohibited (never the optimal play)
# note2: ALWAYS PLAY STRAIGHTS FIRST AS THEY ARE MORE PICKY