import numpy as np

# Define the transition probability matrix
P = np.array([
    [0.2, 0.2, 0.2, 0.2, 0.2],
    [0.1, 0.9, 0, 0, 0],
    [0.1, 0, 0.9, 0, 0],
    [0.1, 0, 0, 0.9, 0],
    [0.1, 0, 0, 0, 0.9]
])

# Find the eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(P.T)

# Find the eigenvector corresponding to eigenvalue 1
stationary = eigenvectors[:, np.isclose(eigenvalues, 1)]

# Normalize it so that the sum of the elements is 1
stationary = stationary[:, 0] / np.sum(stationary[:, 0])

# Print the stationary distribution
print(stationary)
