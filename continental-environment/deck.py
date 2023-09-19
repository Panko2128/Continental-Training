from .card import Card

import random

class Deck:
    def __init__(self):

        suits = ["H", "D", "C", "S"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        game_deck = []

        for num in range(3):
            game_deck += [Card(s, r) for s in suits for r in ranks] 
            game_deck += [Card("Joker", "Joker") for num in range(0,2)]



    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.is_empty():
            return self.cards.pop()
        else:
            return None
    
    # to 3 players
    # def deal(self, num, p1, p2, p3, ):
    #     for i in num:
    #         p1.append(self.draw_card())
    #         p2.append(self.draw_card())
    #         p3.append(self.draw_card())

    def cards_left(self):
        return len(self.cards)

    def is_empty(self):
        return len(self.cards) == 0

    def __len__(self):
        return len(self.cards)