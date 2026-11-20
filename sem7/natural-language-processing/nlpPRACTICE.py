import matplotlib.pyplot as plt

plt.figure(figsize=(8, 4))
plt.hist(df["text_length"], bins=30)
plt.title("Hindi Wikipedia article length distribution")
plt.xlabel("Characters in text")
plt.ylabel("Count")
plt.show()