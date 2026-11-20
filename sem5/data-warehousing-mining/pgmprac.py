import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Hidden states and observations
states = ['Sunny', 'Rainy']
observations = ['Walk', 'Shop', 'Clean', 'Sleep']
obs_seq = ['Walk', 'Shop', 'Clean', 'Sleep']

# Initial probabilities: π
pi = np.array([0.6, 0.4])  # Sunny, Rainy

# Transition probability matrix A
A = np.array([
    [0.7, 0.3],  # From Sunny to Sunny/Rainy
    [0.4, 0.6]   # From Rainy to Sunny/Rainy
])

# Emission probability matrix B
B = np.array([
    [0.5, 0.2, 0.2, 0.1],   # Sunny emits: Walk, Shop, Clean, Sleep
    [0.1, 0.3, 0.4, 0.2]    # Rainy emits: Walk, Shop, Clean, Sleep
])

# Index mapping for states and observations
state_idx = {s: i for i, s in enumerate(states)}
obs_idx = {o: i for i, o in enumerate(observations)}

# -------------------- FORWARD ALGORITHM --------------------
alpha = np.zeros((len(obs_seq), len(states)))

# Initialize
for j in range(len(states)):
    alpha[0, j] = pi[j] * B[j, obs_idx[obs_seq[0]]]

# Recursion
for t in range(1, len(obs_seq)):
    for j in range(len(states)):
        alpha[t, j] = sum(alpha[t-1, i] * A[i, j] for i in range(len(states))) * B[j, obs_idx[obs_seq[t]]]

likelihood = np.sum(alpha[-1])
print('Likelihood of the observed sequence:', likelihood)

# -------------------- VITERBI ALGORITHM --------------------
V = np.zeros((len(obs_seq), len(states)))
ptr = np.zeros((len(obs_seq), len(states)), dtype=int)

# Initialization
for j in range(len(states)):
    V[0, j] = pi[j] * B[j, obs_idx[obs_seq[0]]]

# Recursion
for t in range(1, len(obs_seq)):
    for j in range(len(states)):
        seq_probs = [V[t-1, i] * A[i, j] for i in range(len(states))]
        V[t, j] = max(seq_probs) * B[j, obs_idx[obs_seq[t]]]
        ptr[t, j] = np.argmax(seq_probs)

# Backtrack
best_path = np.zeros(len(obs_seq), dtype=int)
best_path[-1] = np.argmax(V[-1])
for t in range(len(obs_seq)-2, -1, -1):
    best_path[t] = ptr[t+1, best_path[t+1]]

best_state_seq = [states[i] for i in best_path]
print('Best hidden sequence:', best_state_seq)

# -------------------- VISUALIZATION 1: FORWARD PROBABILITIES --------------------
plt.figure(figsize=(8, 5))
for i, state in enumerate(states):
    plt.plot(range(1, len(obs_seq)+1), alpha[:, i], marker='o', label=f'Alpha[{state}]')
plt.xticks(range(1, len(obs_seq)+1), obs_seq)
plt.xlabel('Observation Step')
plt.ylabel('Forward Probability')
plt.title('Forward Probabilities (Alpha values)')
plt.legend()
plt.tight_layout()
plt.show()

# -------------------- VISUALIZATION 2: BEST HIDDEN STATE SEQUENCE --------------------
plt.figure(figsize=(8,2))
te = np.arange(len(obs_seq))
plt.plot(te, best_path, marker='s', linestyle='-', color='tab:blue')
plt.yticks([0,1], states)
plt.xticks(te, obs_seq)
plt.xlabel('Observation Step')
plt.ylabel('Hidden State')
plt.title('Best Hidden State Sequence (Viterbi Path)')
plt.tight_layout()
plt.show()

