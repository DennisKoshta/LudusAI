import random
import numpy as np

PAYOFF = {
            ('Cooperate', 'Cooperate'): 3,
            ('Cooperate', 'Defect'): 0,
            ('Defect', 'Cooperate'): 5,
            ('Defect', 'Defect'): 1
        }

class PrisonersDilemma:
    def __init__(self):
        pass

    def play(self, strategy1, strategy2, rounds=100):
        score1, score2 = 0, 0
        history1, history2 = [], []
        for _ in range(rounds):
            move1 = strategy1(history1, history2)
            move2 = strategy2(history1, history2)
            history1.append(move1)
            history2.append(move2)
            round_score1, round_score2 = PAYOFF[(move1, move2)], PAYOFF[(move2, move1)]
            score1 += round_score1
            score2 += round_score2
        return score1, score2, history1, history2

    def tit_for_tat(self, history1, history2):
        if not history2:
            return 'Cooperate'
        return history2[-1]

    def always_cooperate(self, history1, history2):
        return 'Cooperate'

    def always_defect(self, history1, history2):
        return 'Defect'

    def random_strategy(self, history1, history2):
        return random.choice(['Cooperate', 'Defect'])

class QLearningStrategy:
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0
        self.min_exploration_rate = 0.01
        self.exploration_decay_rate = 0.99

    def get_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(['Cooperate', 'Defect'])
        return max(self.q_table.get(state, {'Cooperate': 0, 'Defect': 0}), key=self.q_table.get(state, {'Cooperate': 0, 'Defect': 0}).get)

    def update_q_value(self, state, action, reward, next_state):
        
        current_q = self.q_table.get(state, {}).get(action, 0)
        max_future_q = max(self.q_table.get(next_state, {'Cooperate': 0, 'Defect': 0}).values())
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

    def decay_exploration_rate(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay_rate)

    def train(self, episodes, opponent_strategy):
        for _ in range(episodes):
            state = ""
            for _ in range(100):
                action = self.get_action(state)
                opponent_action = opponent_strategy(state.split(',')[1], state.split(',')[0])

                print(state, action, opponent_action)

                if opponent_action not in ['Cooperate', 'Defect']:
                    print(opponent_action)
                    opponent_action = random.choice(['Cooperate', 'Defect'])

                reward = PAYOFF[(action, opponent_action)]
                next_state = f"{state.split(',')[0]}{action},{state.split(',')[1]}{opponent_action}"
                self.update_q_value(state, action, reward, next_state)
                state = next_state

    def q_strategy(self, history1, history2):
        state = (''.join(history1), ''.join(history2))
        return self.get_action(state)