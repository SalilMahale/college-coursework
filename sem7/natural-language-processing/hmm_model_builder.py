import json
from collections import defaultdict
LINE = "=" * 70
def print_section(title):
    print("\n" + LINE)
    print(title)
    print(LINE)
print(LINE)
print("HIDDEN MARKOV MODEL FOR POS TAGGING")
print(LINE)
# ---------------------------------------------------------------------------
# Read the tagged corpus
# ---------------------------------------------------------------------------
n = int(input("\nEnter number of sentences in corpus: "))
corpus = []
print("Enter tagged sentences:")
for i in range(n):
    line = input(f"Enter sentence {i + 1}: ")
    sentence = []
    for item in line.split():
        if item in ("<s>", "</s>"):
            continue
        word, tag = item.rsplit("/", 1)
        sentence.append((word.lower(), tag))
    corpus.append(sentence)
# ---------------------------------------------------------------------------
# Step 1: POS tag sequences
# ---------------------------------------------------------------------------
print_section("STEP 1 : POS TAGS")
tag_sequences = []
for sentence in corpus:
    pos_tags = ["<s>"] + [tag for _, tag in sentence] + ["</s>"]
    tag_sequences.append(pos_tags)
    print(" ".join(pos_tags))
# ---------------------------------------------------------------------------
# Step 2: Tag bigrams
# ---------------------------------------------------------------------------
print_section("STEP 2 : LIST OF POSSIBLE BIGRAMS")
bigram_count = defaultdict(int)
for pos_tags in tag_sequences:
    for i in range(len(pos_tags) - 1):
        bigram_count[(pos_tags[i], pos_tags[i + 1])] += 1
print("\n{:<25} {:>10}".format("Tag Bigram", "Frequency"))
print("-" * 40)
for (tag1, tag2), count in bigram_count.items():
    print("{:<25} {:>10}".format(f"{tag1} -> {tag2}", count))
# ---------------------------------------------------------------------------
# Step 3: Conditional (transition) probabilities
# ---------------------------------------------------------------------------
print_section("STEP 3 : CONDITIONAL PROBABILITIES")
previous_tag_count = defaultdict(int)
for (tag1, _), count in bigram_count.items():
    previous_tag_count[tag1] += count
print("\nFormula:")
print("P(Tag2 | Tag1) = Count(Tag1, Tag2) / Count(Tag1)")
print("\n")
transition_probability = {}
for (tag1, tag2), count in bigram_count.items():
    probability = count / previous_tag_count[tag1]
    transition_probability[(tag1, tag2)] = probability
    print(
        f"P({tag2} | {tag1}) = "
        f"{count}/{previous_tag_count[tag1]} = {probability:.4f}"
    )
tags = sorted({tag for sentence in corpus for _, tag in sentence})
# ---------------------------------------------------------------------------
# Step 4: Transition probability matrix
# ---------------------------------------------------------------------------
print_section("STEP 4 : TRANSITION PROBABILITY MATRIX")
matrix_tags = ["<s>"] + tags + ["</s>"]
print("\n{:<12}".format("From/To"), end="")
for tag in matrix_tags:
    print("{:<12}".format(tag), end="")
print()
print("-" * (12 + 12 * len(matrix_tags)))
for tag1 in matrix_tags:
    print("{:<12}".format(tag1), end="")
    for tag2 in matrix_tags:
        probability = transition_probability.get((tag1, tag2), 0)
        print("{:<12.4f}".format(probability), end="")
    print()
# ---------------------------------------------------------------------------
# Step 5: Emission probability matrix
# ---------------------------------------------------------------------------
print_section("STEP 5 : EMISSION PROBABILITY MATRIX")
emission_count = defaultdict(int)
tag_count = defaultdict(int)
vocabulary = set()
for sentence in corpus:
    for word, tag in sentence:
        emission_count[(word, tag)] += 1
        tag_count[tag] += 1
        vocabulary.add(word)
emission_probability = {
    (word, tag): count / tag_count[tag]
    for (word, tag), count in emission_count.items()
}
print("\nFormula:")
print("P(Word | Tag) = Count(Word, Tag) / Count(Tag)")
print("\n")
print("{:<15}".format("Word"), end="")
for tag in tags:
    print("{:<12}".format(tag), end="")
print()
print("-" * (15 + 12 * len(tags)))
for word in sorted(vocabulary):
    print("{:<15}".format(word), end="")
    for tag in tags:
        probability = emission_probability.get((word, tag), 0)
        print("{:<12.4f}".format(probability), end="")
    print()
# ---------------------------------------------------------------------------
# Save the model to JSON
# ---------------------------------------------------------------------------
model = {
    "tags": tags,
    "transition_probability": {
        f"{tag1}|||{tag2}": probability
        for (tag1, tag2), probability in transition_probability.items()
    },
    "emission_probability": {
        f"{word}|||{tag}": probability
        for (word, tag), probability in emission_probability.items()
    },
}
with open("hmm_model.json", "w") as file:
    json.dump(model, file, indent=4)
print_section("HMM MODEL CREATED SUCCESSFULLY")
print("\nTransition probabilities and")
print("emission probabilities saved in:")
print("hmm_model.json")
