import gym
from gym import spaces
from collections import defaultdict
import random
from game import CardGame

class PlayerEnv(gym.Env):
    def __init__(self, game_state):
        super(PlayerEnv, self).__init__()
        self.game_state = game_state
        self.action_space = spaces.Discrete(9)  # 8 different cards and one 'END' action
        self.observation_space = spaces.Box(low=0, high=52, shape=(8 + 8 + 8 + 2 + 1,), dtype=int)  # player's hand, pile on the table, won cards, points, first card in pile

    def reset(self):
        self.game_state.reset()
        return self._get_obs()

    def step(self, action):
        card = self._action_to_card(action)
        reward, done, needs_to_play_again, info = self.game_state.step(card)
        if not done and not needs_to_play_again:
            done, needs_again_opponent = self.game_state.play_opponent_move()
            if not done and needs_again_opponent:
                done, _ = self.game_state.play_opponent_move()

        if done:
            reward += self.game_state.winner_reward()

        return self._get_obs(), reward, done, info

    def render(self, mode='human'):
        print(f"\n{'='*20} GAME STATE {'='*20}")

        for i, player in enumerate(self.game_state.players):
            print(f"Player {i+1} ({player.name}):")
            print(f"  Hand: {player.show_hand()}")
            print(f"  Won Cards: {player.show_won_cards()}")
            print(f"  Points: {player.points}")
            print('-' * 50)

        print(f"Pile: {dict(self.game_state.pile)}")
        print(f"First Card Played: {self.game_state.first_card_played}")
        print('='*50)

    def close(self):
        pass

    def _get_obs(self):
        obs = []

        # player's cards
        player = self.game_state.players[0]
        obs.extend([player.hand[card] for card in ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']])

        # pile
        obs.extend([self.game_state.pile[card] for card in ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']])

        # won cards
        combined_won_cards = defaultdict(int)
        for p in self.game_state.players:
            for card, count in p.cards_won.items():
                combined_won_cards[card] += count
        obs.extend([combined_won_cards[card] for card in ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']])

        # points of both players
        for p in self.game_state.players:
            obs.append(p.points)

        # first card in pile
        first_card_index = self._card_to_index(self.game_state.first_card_played)
        obs.append(first_card_index)

        return np.array(obs, dtype=np.int32)

    def _action_to_card(self, action):
        card_map = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'END']
        if action == 8:
            return 'END'
        return card_map[action]

    def _card_to_index(self, card):
        card_map = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        if card is None:
            return -1  # no card on table
        return card_map.index(card)
