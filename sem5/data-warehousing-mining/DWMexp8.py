from itertools import combinations

# Custom Dataset: Grocery Store Transactions
transactions = [
    ['Milk', 'Bread', 'Butter'],
    ['Bread', 'Diaper', 'Beer', 'Eggs'],
    ['Milk', 'Diaper', 'Beer', 'Cola'],
    ['Bread', 'Milk', 'Diaper', 'Beer'],
    ['Bread', 'Milk', 'Diaper', 'Cola'],
    ['Milk', 'Bread', 'Butter', 'Eggs'],
    ['Bread', 'Butter', 'Diaper'],
    ['Milk', 'Diaper', 'Beer'],
    ['Bread', 'Milk', 'Cola'],
    ['Milk', 'Bread', 'Butter', 'Beer']
]

print("=" * 80)
print("APRIORI ALGORITHM - ASSOCIATION RULE MINING")
print("=" * 80)

# Print Dataset
print("\n    TRANSACTION DATASET    ")
for i, transaction in enumerate(transactions, 1):
    print(f"T{i}: {transaction}")

# Print Total Transactions
total_transactions = len(transactions)
print(f"\nTotal Number of Transactions: {total_transactions}")

# User Input
min_support = float(input("\nEnter minimum support (0-1, e.g., 0.3): "))
min_confidence = float(input("Enter minimum confidence (0-1, e.g., 0.6): "))

# Helper Functions
def get_support_count(itemset, transactions):
    count = 0
    itemset_set = set(itemset)
    for transaction in transactions:
        if itemset_set.issubset(set(transaction)):
            count += 1
    return count

def get_support(itemset, transactions):
    return get_support_count(itemset, transactions) / len(transactions)

def get_unique_items(transactions):
    items = set()
    for transaction in transactions:
        for item in transaction:
            items.add(item)
    return sorted(list(items))

# Apriori Algorithm
print("\n" + "=" * 80)
print("FREQUENT ITEMSET GENERATION")
print("=" * 80)

# Generate C1 and L1
unique_items = get_unique_items(transactions)

print("\n    C1 - CANDIDATE 1-ITEMSETS WITH SUPPORT    ")
C1 = []
for item in unique_items:
    support_count = get_support_count([item], transactions)
    support = get_support([item], transactions)
    C1.append((frozenset([item]), support_count, support))
    print(f"{{{item}}}: Support Count = {support_count}, Support = {support:.2f}")

print(f"\n    L1 - FREQUENT 1-ITEMSETS (Min Support = {min_support})    ")
L1 = []
for itemset, sup_count, sup in C1:
    if sup >= min_support:
        L1.append(itemset)
        print(f"{set(itemset)}: Support Count = {sup_count}, Support = {sup:.2f}")

# Store all frequent itemsets
all_frequent_itemsets = {1: [(itemset, get_support(list(itemset), transactions)) for itemset in L1]}

# Generate higher level itemsets
k = 2
Lk_prev = L1

while Lk_prev:
    # Generate Ck (Candidate k-itemsets)
    print(f"\n    C{k} - CANDIDATE {k}-ITEMSETS WITH SUPPORT    ")
    Ck = set()
    for i in range(len(Lk_prev)):
        for j in range(i + 1, len(Lk_prev)):
            union = Lk_prev[i] | Lk_prev[j]
            if len(union) == k:
                Ck.add(union)
    
    if not Ck:
        print(f"No candidate {k}-itemsets generated.")
        break
    
    Ck_with_support = []
    for itemset in Ck:
        support_count = get_support_count(list(itemset), transactions)
        support = get_support(list(itemset), transactions)
        Ck_with_support.append((itemset, support_count, support))
        print(f"{set(itemset)}: Support Count = {support_count}, Support = {support:.2f}")
    
    # Generate Lk (Frequent k-itemsets)
    print(f"\n    L{k} - FREQUENT {k}-ITEMSETS (Min Support = {min_support})    ")
    Lk = []
    for itemset, sup_count, sup in Ck_with_support:
        if sup >= min_support:
            Lk.append(itemset)
            print(f"{set(itemset)}: Support Count = {sup_count}, Support = {sup:.2f}")
    
    if not Lk:
        print(f"No frequent {k}-itemsets found.")
        break
    
    # Store frequent itemsets
    all_frequent_itemsets[k] = [(itemset, get_support(list(itemset), transactions)) for itemset in Lk]
    
    Lk_prev = Lk
    k += 1

# Generate Association Rules
print("\n" + "=" * 80)
print("ASSOCIATION RULES")
print("=" * 80)

rules = []
for k in range(2, max(all_frequent_itemsets.keys()) + 1):
    for itemset, support in all_frequent_itemsets[k]:
        itemset_list = list(itemset)
        
        # Generate all non-empty subsets as antecedents
        for i in range(1, len(itemset_list)):
            for antecedent in combinations(itemset_list, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                
                if len(consequent) > 0:
                    antecedent_support = get_support(list(antecedent), transactions)
                    confidence = support / antecedent_support if antecedent_support > 0 else 0
                    
                    if confidence >= min_confidence:
                        consequent_support = get_support(list(consequent), transactions)
                        lift = confidence / consequent_support if consequent_support > 0 else 0
                        
                        rules.append({
                            'antecedent': set(antecedent),
                            'consequent': set(consequent),
                            'support': support,
                            'confidence': confidence,
                            'lift': lift
                        })

print(f"\n    ASSOCIATION RULES (Min Confidence = {min_confidence})    ")
if rules:
    print(f"\nTotal Association Rules Found: {len(rules)}\n")
    print(f"{'Rule':<45} {'Support':<10} {'Confidence':<12} {'Lift':<10}")
    print("-" * 80)
    for rule in rules:
        rule_str = f"{rule['antecedent']} => {rule['consequent']}"
        print(f"{rule_str:<45} {rule['support']:<10.3f} {rule['confidence']:<12.3f} {rule['lift']:<10.3f}")
else:
    print("\nNo association rules found with the given thresholds.")

# Print All Frequent Itemsets Summary
print("\n" + "=" * 80)
print("FREQUENT ITEMSETS SUMMARY")
print("=" * 80)

for k in sorted(all_frequent_itemsets.keys()):
    print(f"\n    FREQUENT {k}-ITEMSETS    ")
    for itemset, support in all_frequent_itemsets[k]:
        print(f"{set(itemset)}: Support = {support:.3f}")

print("\n" + "=" * 80)
print("APRIORI ALGORITHM COMPLETED")
print("=" * 80)
