import numpy as np

data = np.array([1, 2, 3, 10, 11, 12, 20, 30])
k = 2  

means = [1, 20]

print("Dataset:", data.tolist())  
print("Number of clusters (k):", k)
print("Initial means:", means)

for iteration in range(1, 5):
    clusters = {i: [] for i in range(k)}
    
    for point in data:
        distances = [abs(int(point) - m) for m in means]
        cluster_index = distances.index(min(distances))
        clusters[cluster_index].append(int(point))  
    
    print(f"\nIteration {iteration}:")
    for idx in clusters:
        print(f"  Cluster {idx+1}: {clusters[idx]}")
    
    new_means = []
    for idx in clusters:
        if len(clusters[idx]) > 0:
            new_means.append(round(sum(clusters[idx]) / len(clusters[idx]), 2))  
        else:
            new_means.append(means[idx])
    
    print("  Updated means:", new_means)
    means = new_means

print("\nFinal Clusters:")
for idx in clusters:
    print(f"Cluster {idx+1}: {clusters[idx]}")
