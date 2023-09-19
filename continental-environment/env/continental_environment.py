import functools
import random
from copy import copy

import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete

from pettingzoo.utils.env import ParallelEnv

from deck import Deck
from card import Card
from utils import *
from find_moves import *

class ContEnv(ParallelEnv):
    metadata = {
        "name": "continental_environment_v0",
    }

    def __init__(self):
       
        self.down_status = None

     # track turn, round and hand sizes 

        self.game_state = None

        self.deck = None

        self.discard_id = None

        self.phase = None

        self.curr_player_down_stage = None

        self.possible_agents = ["p1", "p2", "p3", "p4", "p5", "p6"]



# make deck, gamestate array, deal cards, initialize non-card info
    def reset(self, seed=None, options=None):
        self.agents = copy(self.possible_agents)

        # create/shuffle deck
        self.deck = Deck()

        self.deck.shuffle()
        
        # create gamestate array
        self.game_state = np.zeros(177)

        # move one card to discard pile top
        self.discard_id = self.deck.draw_card().id
        self.game_state[self.discard_id] = 30

        # deal cards out to player

        # set down status array to zeros (not down)

        observations = {
            "p1": p1_obs,
            "p2": p2_obs,
            "p3": p3_obs,
        }

        return observations, {}

    def step(self, actions):

        curr_player = get_curr_player(self.game_state)

        # Draw Phase
        if self.phase == "draw":

            # these are based on player number
             
            prio = get_prio_list(curr_player)

            # Check action masks for each player
            action_masks = self.get_draw_action_masks(prio)
            actions = self.get_draw_actions(actions)

            

            # Apply actions for each player
            to_process = []
            for p in range(6):
                to_process.append(get_action_from_mask(actions[p], action_masks[p], "draw"))
            
            # will assume value [0,6]
            # 0 -> nobody wants the card at discard top
            # 1 - 6 -> player with that player number is getting it
            who_gets = self.process_draw_actions(prio, to_process)

            # if the current player (curr_player) ends up wanting the card, no penalty
            # discard top -> public in curr_player's hand
            if who_gets == curr_player:
                self.game_state[self.discard_id] = curr_player


            # if "0" is recipient of the card, nobody wanted the card (no conditionals kicked in)
            # discard top -> discard bottom
            # card on deck -> private in curr_player's hand
            elif who_gets == 0:
                drawn_id = self.deck.draw_card().id

                self.game_state[self.discard_id] = 31
                self.game_state[drawn_id] = curr_player + 100

            # otherwise, a player (whose turn it is not) gets the card + penalty
            # then, curr_player draws

            # discard top -> public in who_gets's hand
            # deck -> private in who_gets's hand
            # deck -> private in curr_player's hand

            # update who_gets's hand size (always increases by 2)
            else:
                penalty_id = self.deck.draw_card().id
                drawn_id = self.deck.draw_card().id

                self.game_state[self.discard_id] = who_gets
                self.game_state[penalty_id] = who_gets + 100
                self.game_state[drawn_id] = curr_player + 100
                self.game_state[who_gets + 164] += 2

            # update curr_player's hand size after drawing (always increases by 1)
            self.game_state[curr_player + 164] += 1

            if self.down_status[curr_player - 1] == 0:
                self.phase = "down"
            else:
                self.phase = "play"



        # Down (or Discard) Phase
        elif self.phase == "down":

            down_action = actions[curr_player - 1]
            down_mask = 

        # Play (or Discard) Phase
        elif self.phase == "play":

    
            
        # Calculate rewards, terminations, and other information here
        rewards = {}
        terminations = {}
        infos = {}

        # Update the observations for each player here
        observations = self.get_observations()

        return observations, rewards, terminations, infos

    def render(self):
        pass

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]
    
    


    
    