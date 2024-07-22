import random
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

class CardGame:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = self.create_deck()
        self.pile = defaultdict(int)
        self.pile_winner_index = 0
        self.first_player_index = 0
        self.current_player_index = 0
        self.first_card_played = None
        self.deal_cards()

    def create_deck(self):
        cards = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [card for card in cards for _ in range(4)]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        while any(player.need_cards() for player in self.players) and self.deck:
            for player in self.players:
                if player.need_cards() and self.deck:
                    player.draw_card(self.deck.pop())

    def reset(self):
        self.deck = self.create_deck()
        self.pile = defaultdict(int)
        self.pile_winner_index = 0
        self.first_card_played = None
        self.first_player_index = 0
        self.current_player_index = 0
        for player in self.players:
            player.hand = defaultdict(int)
            player.cards_won = defaultdict(int)
            player.points = 0
        self.deal_cards()

    def step(self, card):
        needs_to_play_again = False
        if card == 'END':

            if self.current_player_index != self.first_player_index:
                reward = -100
                done = True
                return reward, done, needs_to_play_again

            elif self.first_card_played is None:
                reward = -100
                done = True
                return reward, done, needs_to_play_again
            else:
                reward, done, needs_to_play_again = self._end_round()
                self.current_player_index = self.pile_winner_index
                return reward, done, needs_to_play_again


        if (self.current_player_index == self.first_player_index) and self.first_card_played is not None:
            if card != self.first_card_played and card != '7':
                reward = -100
                done = True
                return reward, done, needs_to_play_again

        if self.players[self.current_player_index].hand[card] <= 0:
            reward = -100
            done = True
            return reward, done, needs_to_play_again

        self.players[self.current_player_index].play_card(card)
        self.pile[card] += 1

        if self.first_card_played is None:
            self.first_card_played = card
            self.pile_winner_index = self.current_player_index
            self.first_player_index = self.current_player_index
        else:
            if card == self.first_card_played or card == '7':
                self.pile_winner_index = self.current_player_index

        if not needs_to_play_again:
            self._next_turn()
        reward = 0
        done = self._check_game_over()
        return reward, done, needs_to_play_again

    def _next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % 2

    def _end_round(self):
        self.players[self.pile_winner_index].add_won_cards(self.pile)
        reward = (self.pile['10'] + self.pile['A']) * 10 + 5

        self.pile = defaultdict(int)
        self.first_card_played = None

        needs_to_play_again = False
        if self.first_player_index == self.pile_winner_index:
            needs_to_play_again = True

        self.first_player_index = self.pile_winner_index
        done = self._check_game_over()
        if not done:
            self.deal_cards()

        return reward, done, needs_to_play_again

    def play_opponent_move(self):
        opponent = self.players[self.current_player_index]
        valid_cards = []

        if (self.current_player_index == self.first_player_index) and self.first_card_played is not None:
            valid_cards = [card for card, count in opponent.hand.items() if count > 0 and (card == '7' or card == self.first_card_played)]
            valid_cards.append('END')
        else:
            valid_cards = [card for card in opponent.hand if opponent.hand[card] > 0]

        choice = random.choice(valid_cards)
        print(f"{opponent.name} (Player Index {self.current_player_index}) plays {choice}")

        _, done, needs_again = self.step(choice)
        return done, needs_again

    def _check_game_over(self):
        if len(self.deck) == 0 and all(player.card_count() == 0 for player in self.players):
            return True
        return False

def main():
    player_names = ["Player 1", "Player 2"]
    game = CardGame(player_names)

    while True:
        current_player = game.players[game.current_player_index]
        opponent_index = (game.current_player_index + 1) % 2
        opponent_player = game.players[opponent_index]
        print(f"\n{'='*20} {current_player.name}'s Turn (Player Index {game.current_player_index}) {'='*20}")
        print(f"Your hand: {current_player.show_hand()}")
        print(f"Opponent's hand: {opponent_player.show_hand()}")
        print(f"Pile: {dict(game.pile)}")
        print(f"First Card Played: {game.first_card_played}")
        for i, player in enumerate(game.players):
            print(f"Player {i+1} ({player.name}) Won Cards: {player.show_won_cards()}")

        card = input("Enter the card you want to play (or 'END' to end the round): ").strip()

        if card not in current_player.hand and card != 'END':
            print("Invalid card. Try again.")
            continue

        print(f"{current_player.name} (Player Index {game.current_player_index}) plays {card}")
        reward, done, needs_to_play_again = game.step(card)

        if done:
            break

        if not needs_to_play_again:
            done, needs_again = game.play_opponent_move()
            if done:
                break
            while needs_again:
                done, needs_again = game.play_opponent_move()
                if done:
                    break

        if done:
            break

    print("\nGame Over!")
    for i, player in enumerate(game.players):
        print(f"Player {i+1} ({player.name}):")
        print(f"  Won Cards: {player.show_won_cards()}")
        print(f"  Points: {player.points}")
        print('-' * 50)

if __name__ == "__main__":
    main()
