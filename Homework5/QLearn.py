import numpy as np
import matplotlib.pyplot as plt

# Dimensiunile mediului
num_rows = 7
num_cols = 10
start_state = (3, 0)
goal_state = (3, 7)
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
num_actions = 4
learning_rate = 0.5
discount_factor = 0.9
epsilon = 0.1
num_episodes = 1000
Q = np.zeros((num_rows, num_cols, num_actions))

# Funcție pentru a alege o acțiune bazată pe politica Q cu epsilon-greedy
def choose_action(state):
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    else:
        return np.argmax(Q[state])

# Funcție pentru a lua o acțiune
def take_action(state, action):
    wind_effect = min(wind[state[1]], state[0])
    next_state = (max(0, min(num_rows-1, state[0] - wind_effect)), 
                  max(0, min(num_cols-1, state[1] + [-1, 1, 0, 0][action])))
    return next_state

# Simulare Q-learning
rewards_per_episode = []
max_steps_per_episode = 1000  # Modificați acest număr după necesități

for episode in range(num_episodes):
    state = start_state
    total_reward = 0
    steps = 0  # Adăugăm un contor pentru numărul de pași

    while state != goal_state and steps < max_steps_per_episode:
        action = choose_action(state)
        next_state = take_action(state, action)
        
        reward = -1  # Răsplată constantă pentru fiecare tranziție
        
        Q[state][action] = Q[state][action] + learning_rate * \
                           (reward + discount_factor * np.max(Q[next_state]) - Q[state][action])
        
        state = next_state
        total_reward += reward
        steps += 1  # Incrementăm contorul de pași

    rewards_per_episode.append(total_reward)

# Afișarea politicii
policy = np.argmax(Q, axis=2)

print("Politica determinată de algoritm:")
print(policy)

# Bonus: Verificați convergența algoritmului
plt.plot(rewards_per_episode)
plt.xlabel('Episod')
plt.ylabel('Recompensă totală')
plt.title('Convergența algoritmului Q-learning')
plt.show()
