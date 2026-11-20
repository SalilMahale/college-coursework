import pandas as pd

df = pd.read_csv("Car_Stolen.csv")

print("DATASET:\n", df.to_string(index=False))

num_tuples = len(df)
print("\nNumber of tuples:", num_tuples)

class_counts = df['Stolen'].value_counts()

priors = {cls: count / num_tuples for cls, count in class_counts.items()}

print("\nIndependent Probability of Classes (P(C)):")
for cls, prob in priors.items():
    print(f"P({cls}) = {prob:.3f}")

test_tuple = {'Color': 'Red', 'Type': 'SUV', 'Origin': 'Domestic'}

conditional_probs = {}

print("\nConditional Probabilities P(A|C):")
for cls in priors.keys():
    subset = df[df['Stolen'] == cls]  
    total_in_class = len(subset)
    conditional_probs[cls] = {}
    
    for attr, value in test_tuple.items():
        count = len(subset[subset[attr] == value])
        prob = count / total_in_class if total_in_class > 0 else 0
        conditional_probs[cls][attr] = prob
        print(f"P({attr}={value} | {cls}) = {prob:.3f}")

total_probs = {}
for cls in priors.keys():
    product = priors[cls]
    for attr in test_tuple:
        product *= conditional_probs[cls][attr]
    total_probs[cls] = product

predicted_class = max(total_probs, key=total_probs.get)

print("\nTest Tuple:", test_tuple)
print("Predicted Class:", predicted_class)
