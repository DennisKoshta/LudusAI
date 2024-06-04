import random
import numpy as np

class PrisonersDilemma:
    def __init__(self):
        self.payoff_matrix = {
            ('Cooperate', 'Cooperate'): (3, 3),
            ('Cooperate', 'Defect'): (0, 5),
            ('Defect', 'Cooperate'): (5, 0),
            ('Defect', 'Defect'): (1, 1)
        }

    def play(self, strategy1, strategy2, rounds=100):
        score1, score2 = 0, 0
        history1, history2 = [], []
        for _ in range(rounds):
            move1 = strategy1(history1, history2)
            move2 = strategy2(history1, history2)
            history1.append(move1)
            history2.append(move2)
            round_score1, round_score2 = self.payoff_matrix[(move1, move2)]
            score1 += round_score1
            score2 += round_score2
        return score1, score2, history1, history2

    def tit_for_tat(history1, history2):
        if not history2:
            return 'Cooperate'
        return history2[-1]

    def always_cooperate(history1, history2):
        return 'Cooperate'

    def always_defect(history1, history2):
        return 'Defect'

    def random_strategy(history1, history2):
        return random.choice(['Cooperate', 'Defect'])

class QLearningStrategy:
    def __init__(self):
        self.payoff_matrix = {
            ('Cooperate', 'Cooperate'): (3, 3),
            ('Cooperate', 'Defect'): (0, 5),
            ('Defect', 'Cooperate'): (5, 0),
            ('Defect', 'Defect'): (1, 1)
        }

        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.1
    
    def get_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(['Cooperate', 'Defect'])
        return max(self.q_table.get(state, {'Cooperate': 0, 'Defect': 0}), key=self.q_table.get(state, {'Cooperate': 0, 'Defect': 0}).get)
    
    def update_q_value(self, state, action, reward, next_state):
        current_q = self.q_table.get(state, {}).get(action, 0)
        print(self.q_table.get(next_state, {'Cooperate': 0, 'Defect': 0}).values())
        print(self.q_table.get(next_state, {'Cooperate': 0, 'Defect': 0}))
        max_future_q = max(self.q_table.get(next_state, {'Cooperate': 0, 'Defect': 0}).values())
        # print(reward)
        # print(self.discount_factor)
        # print(max_future_q)
        new_q = current_q + self.learning_rate * (np.array(reward) + self.discount_factor * max_future_q - current_q)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

    def train(self, episodes, strategy):
        for e in range(episodes):
            state = ('', '')
            for _ in range(100):
                action = self.get_action(state)
                opponent_action = strategy(state[1], state[0])
                reward, next_state = self.payoff_matrix[(action, opponent_action)], (state[1] + opponent_action, state[0] + action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state

    def q_strategy(self, history1, history2):
        state = ''.join(history1), ''.join(history2)
        return self.get_action(state)

# q_learning_strategy = QLearningStrategy()
# q_learning_strategy.train(1000, q_learning_strategy.q_strategy())