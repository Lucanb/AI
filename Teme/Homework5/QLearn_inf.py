import numpy as np
import matplotlib.pyplot as plt
import math

class WindyGridWorld:
    def __init__(self, rows, cols, start, goal, wind):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.wind = wind
        self.agent_position = start
        self.episode_finished = False
        self.total_reward = 0

    def reset(self):
        self.agent_position = self.start
        self.episode_finished = False
        self.total_reward = 0

    def move_agent(self, action):
        wind_effect = self.wind[self.agent_position[1]]
        next_row = self.agent_position[0] - wind_effect
        next_col = self.agent_position[1]

        if action == 0:  # Sus
            next_row += 1
        elif action == 1:  # Jos
            next_row -= 1
        elif action == 2:  # Stânga
            next_col -= 1
        elif action == 3:  # Dreapta
            next_col += 1

        next_row = max(0, min(next_row, self.rows - 1))  # Asigură că rămâne în limitele de sus și jos
        next_col = max(0, min(next_col, self.cols - 1))  # Asigură că rămâne în limitele stânga-dreapta

        # Asigură că agentul rămâne pe loc dacă este la marginea de sus și vântul încearcă să-l împingă în afara mediului
        if self.agent_position[0] == 0 and wind_effect > 0 and action == 0:
            next_row = self.agent_position[0]

        self.agent_position = (next_row, next_col)

    def take_action(self, action):
        self.move_agent(action)
        self.total_reward += -1
        if self.agent_position == self.goal:
            self.episode_finished = True
            return action,True
        return action,False

    def get_state(self):
        return self.agent_position

    def get_reward(self):
        return self.total_reward

    def is_episode_finished(self):
        return self.episode_finished

def q_learning(env, num_episodes=1000, alpha=0.1, gamma=0.9, epsilon=1):
    Q = np.zeros((env.rows, env.cols, 4))  # 0: sus, 1: jos, 2: stânga, 3: dreapta
    rewards_per_episode = []

    for episode in range(num_episodes):
        env.reset()
        state = env.get_state()
        total_reward = 0

        while not env.is_episode_finished():
            if np.random.rand() < epsilon:
                action = np.random.choice(4)
            else:
                action = np.argmax(Q[state[0], state[1]])
                #print(Q[state[0], state[1]])

            anterior_state = env.get_state()
            action_done,verif = env.take_action(action)

            if verif == True:
                Q[anterior_state[0],anterior_state[1],action_done] = math.inf
            else:
                
                next_state = env.get_state()
                reward = env.get_reward()

                Q[state[0], state[1], action] += alpha * (reward + gamma * np.max(Q[next_state[0], next_state[1]]) - Q[state[0], state[1], action])

                state = next_state
                total_reward += reward

        rewards_per_episode.append(total_reward)

        # Actualizează epsilon pentru explorare
        epsilon = max(epsilon * 0.99, 0.1)

    policy = np.argmax(Q, axis=2)
    print("Politica determinată de algoritm:")
    print(policy)

    # Afișează graficul recompenselor în raport cu episodul
    plt.plot(rewards_per_episode)
    plt.xlabel('Episod')
    plt.ylabel('Recompensă totală')
    plt.title('Convergența algoritmului Q-learning')
    plt.show()

# Setările mediului
rows = 7
cols = 10
start = (3, 0)
goal = (3, 7)
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

# Crează mediu
env = WindyGridWorld(rows, cols, start, goal, wind)

# Antrenează agentul folosind Q-learning
q_learning(env)
