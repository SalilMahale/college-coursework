import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Hidden states and observations
states = ['Sunny', 'Rainy']
observations = ['Walk', 'Shop', 'Clean', 'Sleep']
obs_seq = ['Walk', 'Shop', 'Clean', 'Sleep']

# Initial probabilities: pi
pi = np.array([0.6, 0.4])  # Sunny, Rainy
print('initial probabilities\n', pi)

# Transition probability matrix A
A = np.array([
    [0.7, 0.3],  # From Sunny to Sunny/rainy
    [0.4, 0.6]   # From Rainy to sunny/Rainy
])
print('transition probability matrix\n', A)

# Emission probability matrix B
B = np.array([
    [0.5, 0.2, 0.2, 0.1],  # Sunny emits: walk, shop, Clean, sleep
    [0.1, 0.3, 0.4, 0.2]   # Rainy emits: walk, Shop, clean, Sleep
])
print('emission probability matrix\n', B)

# Index mapping for states and observations
state_idx = {s: i for i, s in enumerate(states)}  #maps states to 0,1
obs_idx = {o: i for i, o in enumerate(observations)}  #maps observations to 0,1,2,3

# 2 compute likelihood of observed sequence
alpha = np.zeros((len(obs_seq), len(states)))  #produce 4x2 matrix of zeros

# Initialize forward probabilities
for j in range(len(states)):
    alpha[0, j] = pi[j] * B[j, obs_idx[obs_seq[0]]]  # multiplies 0.6x0.5 and 0.4x0.1  result: [0.3,0.04]

# for remaining iterations
for t in range(1, len(obs_seq)):
    for j in range(len(states)):
        alpha[t, j] = sum(alpha[t-1, i] * A[i, j] for i in range(len(states))) * B[j, obs_idx[obs_seq[t]]]
        
print('\nvalues of alpha\n', alpha)
likelihood = np.sum(alpha[-1])  #sum the 2 values in the last alpha row
print('Likelihood of the observed sequence: ', likelihood)

#find best hidden state sequence (viterbi sequence)
V = np.zeros((len(obs_seq), len(states)))
ptr = np.zeros((len(obs_seq), len(states)), dtype=int)

# Initialization
for j in range(len(states)):
    V[0, j] = pi[j] * B[j, obs_idx[obs_seq[0]]]  #0.6x0.5
    ptr[0, j] = 0  #initial pointer is 0

# Recursion
for t in range(1, len(obs_seq)):
    for j in range(len(states)):
        seq_probs = [V[t-1, i] * A[i, j] for i in range(len(states))]
        V[t, j] = max(seq_probs) * B[j, obs_idx[obs_seq[t]]]
        ptr[t, j] = np.argmax(seq_probs)  # argmax returns the index of the maximum value in that list

print('\nvalues of Viterbi matrix V\n', V)
print('\nvalues of pointer matrix ptr\n', ptr)

# Backtrack for the most probable path
best_path = np.zeros(len(obs_seq), dtype=int)  #1-D np array of length 4
best_path[-1] = np.argmax(V[-1])  # rainy in the last row

for t in range(len(obs_seq)-2, -1, -1):  # 2,1,0
    best_path[t] = ptr[t+1, best_path[t+1]]

best_state_seq = [states[i] for i in best_path]
print('Best hidden sequence: ', best_state_seq)

#visualization
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

#visualization 2
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
