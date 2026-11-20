"""
Experiment No 04
Aim: To implement the N-gram model from a text corpus and do
     adjacent word prediction in Python (Bigram and Trigram).
"""

from collections import defaultdict, Counter

CORPUS_PATH = "corpus.txt"


# ---------------- Step 0: Load and tokenize the corpus ----------------
def load_corpus(filepath):
    sentences = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens = line.lower().split()
            sentences.append(tokens)
    return sentences


# ---------------- Step 1: Build n-grams ----------------
def build_ngrams(sentences, n):
    ngram_counts = Counter()
    for sentence in sentences:
        for i in range(len(sentence) - n + 1):
            ngram = tuple(sentence[i:i + n])
            ngram_counts[ngram] += 1
    return ngram_counts


# ---------------- Step 2: Conditional probabilities ----------------
def conditional_probabilities(ngram_counts):
    context_totals = defaultdict(int)
    grouped = defaultdict(dict)
    for ngram, count in ngram_counts.items():
        context, next_word = ngram[:-1], ngram[-1]
        context_totals[context] += count
        grouped[context][next_word] = count

    probabilities = {}
    for context, next_words in grouped.items():
        total = context_totals[context]
        probabilities[context] = {w: c / total for w, c in next_words.items()}
    return probabilities


# ---------------- Step 3: Print a boxed table ----------------
def print_table(probabilities, label):
    print(f"\nStep 2: {label} Conditional Probabilities:")

    rows = []
    for context, next_words in probabilities.items():
        ctx_str = ' '.join(context)
        for word, prob in next_words.items():
            prob_str = "1" if prob == 1 else f"{prob:.6f}"
            rows.append((ctx_str, word, prob_str))

    w1 = max(len('Context'), max(len(r[0]) for r in rows))
    w2 = max(len('Next Word'), max(len(r[1]) for r in rows))
    w3 = max(len('Probability'), max(len(r[2]) for r in rows))
    border = "+" + "-" * (w1 + 2) + "+" + "-" * (w2 + 2) + "+" + "-" * (w3 + 2) + "+"

    print(border)
    print(f"| {'Context':<{w1}} | {'Next Word':<{w2}} | {'Probability':<{w3}} |")
    print(border)
    for ctx_str, word, prob_str in rows:
        print(f"| {ctx_str:<{w1}} | {word:<{w2}} | {prob_str:<{w3}} |")
        print(border)


# ---------------- Step 4: Predict next word(s) ----------------
def predict_next(probabilities, context):
    context = tuple(context)
    print(f"\nStep 3: Predictions for '{' '.join(context)}':")
    if context not in probabilities:
        print(f"No prediction available for context: {' '.join(context)}")
        return
    next_words = probabilities[context]
    for word, prob in next_words.items():
        print(f"{word} (Probability: {prob:.4f})")

    max_prob = max(next_words.values())
    best = [(w, p) for w, p in next_words.items() if p == max_prob]
    print("Selected next word(s):")
    print(", ".join(f"{w} (Probability: {p:.4f})" for w, p in best))


# ---------------- Main program ----------------
if __name__ == "__main__":
    sentences = load_corpus(CORPUS_PATH)

    print("Corpus loaded:")
    for s in sentences:
        print(' '.join(s))

    # ===================== BIGRAM MODEL =====================
    print("\n===================== BIGRAM MODEL =====================")
    bigram_counts = build_ngrams(sentences, 2)

    print("\nStep 1: Listing all bigrams (w1, w2)")
    for bigram, count in bigram_counts.items():
        print(f"({bigram[0]}, {bigram[1]}) -> {count}")

    bigram_probabilities = conditional_probabilities(bigram_counts)
    print_table(bigram_probabilities, "Bigram")

    bigram_word = input("\nEnter word for bigram prediction: ").lower().strip()
    predict_next(bigram_probabilities, (bigram_word,))

    # ===================== TRIGRAM MODEL =====================
    print("\n===================== TRIGRAM MODEL =====================")
    trigram_counts = build_ngrams(sentences, 3)

    print("\nStep 1: Listing all trigrams (w1, w2, w3)")
    for trigram, count in trigram_counts.items():
        print(f"({trigram[0]}, {trigram[1]}, {trigram[2]}) -> {count}")

    trigram_probabilities = conditional_probabilities(trigram_counts)
    print_table(trigram_probabilities, "Trigram")

    trigram_context = input("\nEnter two words for trigram prediction: ").lower().strip().split()
    if len(trigram_context) != 2:
        print("Please enter exactly two words for trigram prediction.")
    else:
        predict_next(trigram_probabilities, trigram_context)
