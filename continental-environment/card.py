class Card:
    CARD_COUNT = 0

    VALUE_ARR = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 15]

    JOKER_VAL = 20

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.id = Card.CARD_COUNT
        Card.CARD_COUNT += 1

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    
class Joker(Card):
    def __init__(self):
        super().__init__("Joker", "Joker")

    def __str__(self):
        return "Joker"
    
#  index  |   card   
# ________|_________
#  0      | 2 of Hearts
#  1      | 3 of Hearts
#  2      | 4 of Hearts
#  3      | 5 of Hearts
#  4      | 6 of Hearts
#  5      | 7 of Hearts
#  6      | 8 of Hearts
#  7      | 9 of Hearts
#  8      | 10 of Hearts
#  9      | Jack of Hearts
#  10     | Queen of Hearts
#  11     | King of Hearts
#  12     | Ace of Hearts
#  13     | 2 of Diamonds
#  14     | 3 of Diamonds
#  15     | 4 of Diamonds
#  16     | 5 of Diamonds
#  17     | 6 of Diamonds
#  18     | 7 of Diamonds
#  19     | 8 of Diamonds
#  20     | 9 of Diamonds
#  21     | 10 of Diamonds
#  22     | Jack of Diamonds
#  23     | Queen of Diamonds
#  24     | King of Diamonds
#  25     | Ace of Diamonds
#  26     | 2 of Clubs
#  27     | 3 of Clubs
#  28     | 4 of Clubs
#  29     | 5 of Clubs
#  30     | 6 of Clubs
#  31     | 7 of Clubs
#  32     | 8 of Clubs
#  33     | 9 of Clubs
#  34     | 10 of Clubs
#  35     | Jack of Clubs
#  36     | Queen of Clubs
#  37     | King of Clubs
#  38     | Ace of Clubs
#  39     | 2 of Spades
#  40     | 3 of Spades
#  41     | 4 of Spades
#  42     | 5 of Spades
#  43     | 6 of Spades
#  44     | 7 of Spades
#  45     | 8 of Spades
#  46     | 9 of Spades
#  47     | 10 of Spades
#  48     | Jack of Spades
#  49     | Queen of Spades
#  50     | King of Spades
#  51     | Ace of Spades
#  52     | Joker
#  53     | Joker

