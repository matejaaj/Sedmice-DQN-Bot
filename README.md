# DQN Sedmice Bot

This project implements training a Deep Q-Learning (DQN) agent to play the card game Sedmice.

## Introduction

Sedmice is a popular card game in Serbia. This project uses reinforcement learning, specifically the Deep Q-Learning (DQN) algorithm, to train a bot to play Sedmice. The bot is trained to make decisions based on the current state of the game.

All files and code have been transferred from Google Colab to this repository to ensure easy access and version control.

For more details about the game Sedmice, its rules, and strategies, please refer to [this link](http://www.igrajkarte.com/blog/post/sedmice-pravila/).

## Training

The DQN agent is trained against an opponent that plays random, always legal moves.

### Environment

The custom environment was created using the `gym` library to simulate the game of Sedmice. This environment manages the game state, defines the actions, and provides the observation space required for the agent.

The reward structure used during training:

- **Valid move**: +5 points
- **Playing a card that wins the pile**: +10 points per 10 or Ace card in the pile
- **Ending the round successfully**: +5 points
- **Winning a round**: +50 points
- **Losing a round**: -30 points
- **Invalid move**: -1000 points
  - **Invalid move reasons**:
    - Card not available in hand
    - Tried to continue round with invalid card
    - Played END on first turn
    - Played END but not played first

### Action Space

The possible actions the agent can take:

- **Playing one of the cards**: There are 8 possible cards (7, 8, 9, 10, J, Q, K, A).
- **Ending the round**: The action to not continue the round ('END').

This results in a total action space of 9 actions (8 cards + 1 END action).

### Observation Space

The observation space consists of the following:

- **Player's hand**: The count of each card in the player's hand (8 values: one for each card type).
- **Pile state**: The count of each card in the pile (8 values: one for each card type).
- **Combined won cards**: The count of each card won by both players combined (8 values: one for each card type).
- **Player points**: The points for both players (2 values).
- **First card in the pile**: The index of the first card played in the pile (1 value).

This results in an observation space of 27 values (8 + 8 + 8 + 2 + 1).

## Evaluation

After training, the model was evaluated over 10,000 episodes. The evaluation metrics are as follows:

- **Wins**: 65.60%
- **Losses**: 8.80%
- **Draws**: 7.40%
- **Invalid moves**: 18.20%

### Invalid Move Reasons:

- **Card not available in hand**: 59%
- **Tried to continue round with invalid card**: 35%
- **Played END on first turn**: 5%
- **Played END but not played first**: 1%

The agent generally performs well, winning a majority of the games. However, it still makes invalid moves in some cases, which stops the game. This indicates areas where the model can be improved for better performance.

## Future Improvements

- **Hyperparameters tuning**: Experiment more with different hyperparameters to optimize the performance of the DQN agent.
- **Testing against human players**: The next step is to test the DQN agent against human players to further evaluate its performance.
- **Advanced opponent modeling**: Train the agent against more sophisticated opponents to enhance its decision-making capabilities.
- **Graphical user interface (GUI)**: Develop a GUI for easier interaction and testing.

### Playing the Game in Console

To play the game in the console, you can use the `console_test_env.py` script
