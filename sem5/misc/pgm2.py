import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True)

# Transition matrix
transition_matrix = np.array([
    [0.7, 0.2, 0.1],  # From X
    [0.3, 0.4, 0.3],  # From Y
    [0.2, 0.3, 0.5]   # From Z
])

initial_shares = np.array([0.5, 0.3, 0.2])

# 1. Show the transition matrix
print("Transition Matrix:\n", transition_matrix)

# 2. Market shares after 5 years: show the step and result
p_power_5 = np.linalg.matrix_power(transition_matrix, 5)
print("\nTransition Matrix to the power 5 (P^5):\n", p_power_5)
shares_after_5_years = initial_shares @ p_power_5
print("\nMarket shares after 5 years (Initial * P^5):", shares_after_5_years)

# 3. Market share evolution over time (for line plot)
years = 10
shares_over_time = [initial_shares]
for i in range(1, years+1):
    next_share = shares_over_time[-1] @ transition_matrix #take the last appended list and multiply
    shares_over_time.append(next_share)
shares_over_time = np.array(shares_over_time) #shape (11,3) each column represents x,y and z

# Plot: market share over time
plt.figure(figsize=(8,5))
plt.plot(range(years+1), shares_over_time[:,0], label='X')
plt.plot(range(years+1), shares_over_time[:,1], label='Y')
plt.plot(range(years+1), shares_over_time[:,2], label='Z')
plt.xlabel('Year')
plt.ylabel('Market Share')
plt.title('Market Share Evolution Over Time')
plt.legend()
plt.tight_layout()
plt.show()

# 4. Show eigenvalues and eigenvectors
eigvals, eigvecs = np.linalg.eig(transition_matrix.T) 
print("\nEigenvalues:\n", eigvals)
print("\nEigenvector Matrix:\n", eigvecs)

# 5. Show the eigenvector corresponding to eigenvalue closest to 1
steady_state_index = np.isclose(eigvals, 1) #real_if_close takes out the complex part if any
steady_state_vector = np.real_if_close(eigvecs[:, steady_state_index]) #the index of the eigenvector corresponds to index of eigenvalues
print("\nEigenvectors closest to 1 (steady-state):\n", steady_state_vector)

# 6. Normalize the steady-state vector and show the answer
eigenvec_flat = steady_state_vector[:,0] #flatten to 1d array by taking the first column
steady_state_shares = eigenvec_flat / np.sum(eigenvec_flat) #normalize to 1
print("\nNormalized steady-state shares:", steady_state_shares)
print("\nFinal steady-state (long run) market shares:")
print(f"X: {steady_state_shares[0]:.4f}, Y: {steady_state_shares[1]:.4f}, Z: {steady_state_shares[2]:.4f}")

# Bar chart for steady-state shares
plt.figure(figsize=(5,5))
plt.bar(['X','Y','Z'], steady_state_shares)
plt.title('Long-Run Steady-State Market Shares')
plt.ylabel('Share')
plt.tight_layout()
plt.show()
