import numpy as np
from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = defaultdict(int)
        self.cards_won = defaultdict(int)
        self.points = 0

    def draw_card(self, card):
        self.hand[card] += 1

    def play_card(self, card):
        if self.hand[card] > 0:
            self.hand[card] -= 1
            return card


    def need_cards(self):
        return sum(self.hand.values()) < 4

    def card_count(self):
        return sum(self.hand.values())

    def add_won_cards(self, cards):
        for card, count in cards.items():
            self.cards_won[card] += count
            if card in ['10', 'A']:
                self.points += 10 * count

    def show_hand(self):
        return {card: count for card, count in self.hand.items() if count > 0}

    def show_won_cards(self):
        return {card: count for card, count in self.cards_won.items() if count > 0}
