import matplotlib.pyplot as plt

# -------- User Input --------
data = list(map(int, input("Enter dataset values separated by space: ").split()))
num_bins = int(input("Enter number of bins: "))

# Step 1: Sort the dataset
sorted_data = sorted(data)

# Step 2: Divide into bins (equal depth partitioning)
bin_size = len(sorted_data) // num_bins
bins = []
for i in range(num_bins):
    if i == num_bins - 1:  # last bin takes remaining values
        bins.append(sorted_data[i * bin_size:])
    else:
        bins.append(sorted_data[i * bin_size:(i + 1) * bin_size])

# Step 3: Bin by Mean
bin_by_mean = []
for b in bins:
    mean_value = sum(b) // len(b)
    bin_by_mean.append([mean_value] * len(b))

# Step 4: Bin by Median
bin_by_median = []
for b in bins:
    b_sorted = sorted(b)
    mid = len(b) // 2
    if len(b) % 2 == 0:
        median_value = (b_sorted[mid - 1] + b_sorted[mid]) // 2
    else:
        median_value = b_sorted[mid]
    bin_by_median.append([median_value] * len(b))

# Step 5: Bin by Boundary
bin_by_boundary = []
for b in bins:
    first, last = b[0], b[-1]
    new_bin = []
    for val in b:
        if abs(val - first) <= abs(val - last):
            new_bin.append(first)
        else:
            new_bin.append(last)
    bin_by_boundary.append(new_bin)

# -------- Printing Results --------
print("\nOriginal Dataset:", data)
print("Sorted Dataset:", sorted_data)
print("Number of Bins:", num_bins)
for i, b in enumerate(bins, start=1):
    print("Bin", i, ":", b)

print("\nBin by Mean:")
for i, b in enumerate(bin_by_mean, start=1):
    print("Bin", i, ":", b)

print("\nBin by Median:")
for i, b in enumerate(bin_by_median, start=1):
    print("Bin", i, ":", b)

print("\nBin by Boundary:")
for i, b in enumerate(bin_by_boundary, start=1):
    print("Bin", i, ":", b)

# -------- Visualization --------
plt.figure(figsize=(12, 8))

# Original Data
plt.subplot(2, 2, 1)
plt.hist(sorted_data, bins=num_bins, color="skyblue", edgecolor="black")
plt.title("Original Dataset")

# Bin by Mean
plt.subplot(2, 2, 2)
plt.hist([val for sublist in bin_by_mean for val in sublist], bins=num_bins, color="orange", edgecolor="black")
plt.title("Bin by Mean")

# Bin by Median
plt.subplot(2, 2, 3)
plt.hist([val for sublist in bin_by_median for val in sublist], bins=num_bins, color="green", edgecolor="black")
plt.title("Bin by Median")

# Bin by Boundary
plt.subplot(2, 2, 4)
plt.hist([val for sublist in bin_by_boundary for val in sublist], bins=num_bins, color="red", edgecolor="black")
plt.title("Bin by Boundary")

plt.tight_layout()
plt.show()
