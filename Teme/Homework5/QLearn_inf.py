import numpy as np
import matplotlib.pyplot as plt
import math

class AgentMove:
    def __init__(self, rows, cols, start, goal, wind):
        self.finish_episode = False
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.wind = wind
        self.rewards_ep = []
        self.agent_coord = start
        self.total_reward = 0

    def get_state(self):
        return self.agent_coord

    def get_totalreward(self):
        return self.total_reward

    def end_episode(self):
        return self.finish_episode

    def initial_pos(self):
        self.agent_coord = self.start
        self.finish_episode = False
        self.total_reward = 0

    def move_agent(self, action):
        wind_effect = self.wind[self.agent_coord[1]]
        next_row = self.agent_coord[0] - wind_effect
        next_col = self.agent_coord[1]

        if action == 0:
            next_row += 1
        elif action == 1:
            next_row -= 1
        elif action == 2:
            next_col -= 1
        elif action == 3:
            next_col += 1

        next_row = max(0, min(next_row, self.rows - 1))
        next_col = max(0, min(next_col, self.cols - 1))

        if self.agent_coord[0] == 0 and wind_effect > 0 and action == 0:
            next_row = self.agent_coord[0]
        self.agent_coord = (next_row, next_col)

    def choose_move(self, action):
        self.move_agent(action)
        self.total_reward += -1
        if self.agent_coord == self.goal:
            self.finish_episode = True
        return self.finish_episode,self.get_state()

def q_learning(myAgent, num_episodes=1000, alpha=0.1, gamma=0.9, epsilon=1):
    Q = np.zeros((myAgent.rows, myAgent.cols, 4))

    for episode in range(num_episodes):
        myAgent.initial_pos()
        state = myAgent.get_state()
        total_reward = 0

        while not myAgent.end_episode():
            if np.random.rand() < epsilon:
                action = np.random.choice(4)
            else:
                action = np.argmax(Q[state[0], state[1]])

            action_done = action
            myAgent.choose_move(action)
            verif,anterior_state =12,[1,2]
            if verif == True:
                Q[anterior_state[0], anterior_state[1], action_done] = math.inf
            else:
                next_state = myAgent.get_state()
                reward = myAgent.get_totalreward()
                Q[state[0], state[1], action] += alpha * (reward + gamma * np.max(Q[next_state[0], next_state[1]]) - Q[state[0], state[1], action])
                state = next_state
                total_reward += reward

        myAgent.rewards_ep.append(total_reward)
        epsilon = max(epsilon * 0.99, 0.1)

    policy = np.argmax(Q, axis=2)
    return policy, myAgent.rewards_ep

rows = 7
cols = 10
start = (3, 0)
goal = (3, 7)
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

myAgent = AgentMove(rows, cols, start, goal, wind)

policy, rewards_ep = q_learning(myAgent)
print("Algorithm Policy :\n")
print(policy)
plt.plot(myAgent.rewards_ep)
plt.xlabel('Episod')
plt.ylabel('Reward')
plt.title('QLearn Convergence')
plt.show()