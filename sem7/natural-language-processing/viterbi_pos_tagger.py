import json
# Must match the start/end markers used by the program that builds hmm_model.json
START = "<s>"
END = "</s>"
LINE = "=" * 70
def print_section(title):
    print("\n" + LINE)
    print(title)
    print(LINE)
print("VITERBI ALGORITHM FOR POS TAGGING")
# ---------------------------------------------------------------------------
# Load the HMM model
# ---------------------------------------------------------------------------
with open("hmm_model.json", "r") as file:
    model = json.load(file)
tags = model["tags"]
transition_probability = {}
for key, probability in model["transition_probability"].items():
    tag1, tag2 = key.split("|||")
    transition_probability[(tag1, tag2)] = probability
emission_probability = {}
for key, probability in model["emission_probability"].items():
    word, tag = key.split("|||")
    emission_probability[(word, tag)] = probability
# ---------------------------------------------------------------------------
# Input sentence
# ---------------------------------------------------------------------------
sentence = input("\nEnter sentence to tag: ").lower().split()
print("\nInput Sentence:")
print(" ".join(sentence))
print_section("VITERBI FORMULA")
print("V_t(s) = max [ V_(t-1)(s') × P(s | s') × P(word_t | s) ]")
# ---------------------------------------------------------------------------
# Forward pass
# ---------------------------------------------------------------------------
viterbi = []        # viterbi[t][tag] : best probability of ending in tag at t
backpointer = []    # backpointer[t][tag]: best previous tag
step_values = []    # detailed record of every computed cell
for i, word in enumerate(sentence):
    current_probability = {}
    current_backpointer = {}
    print_section(f"STEP {i + 1} : {word}")
    for current_tag in tags:
        emission = emission_probability.get((word, current_tag), 0)
        if emission == 0:
            continue
        # ---- First word: start from the <s> marker -------------------------
        if i == 0:
            transition = transition_probability.get((START, current_tag), 0)
            probability = transition * emission
            if probability > 0:
                current_probability[current_tag] = probability
                current_backpointer[current_tag] = START
                step_values.append({
                    "Step": i + 1,
                    "Word": word,
                    "Tag": current_tag,
                    "Previous Tag": START,
                    "Transition": transition,
                    "Emission": emission,
                    "Viterbi": probability,
                })
                print(f"Tag: {current_tag}")
                print(f"Transition = P({current_tag} | {START}) = {transition:.4f}")
                print(f"Emission = P({word} | {current_tag}) = {emission:.4f}")
                print(f"Viterbi = {transition:.4f} × {emission:.4f}")
                print(f"      = {probability:.8f}")
        # ---- Remaining words: pick the best previous tag -------------------
        else:
            best_probability = 0
            best_previous_tag = None
            best_transition = 0
            for previous_tag in viterbi[i - 1]:
                transition = transition_probability.get((previous_tag, current_tag), 0)
                probability = viterbi[i - 1][previous_tag] * transition * emission
                if probability > best_probability:
                    best_probability = probability
                    best_previous_tag = previous_tag
                    best_transition = transition
            if best_previous_tag is not None:
                current_probability[current_tag] = best_probability
                current_backpointer[current_tag] = best_previous_tag
                step_values.append({
                    "Step": i + 1,
                    "Word": word,
                    "Tag": current_tag,
                    "Previous Tag": best_previous_tag,
                    "Transition": best_transition,
                    "Emission": emission,
                    "Viterbi": best_probability,
                })
                print(f"Tag: {current_tag}")
                print(f"Previous Tag = {best_previous_tag}")
                print(
                    f"Transition = P({current_tag} | {best_previous_tag}) "
                    f"= {best_transition:.4f}"
                )
                print(f"Emission = P({word} | {current_tag}) = {emission:.4f}")
                print(
                    f"Viterbi = {viterbi[i - 1][best_previous_tag]:.8f} × "
                    f"{best_transition:.4f} × {emission:.4f}"
                )
                print(f"      = {best_probability:.8f}")
    viterbi.append(current_probability)
    backpointer.append(current_backpointer)
# ---------------------------------------------------------------------------
# Final Viterbi table
# ---------------------------------------------------------------------------
print_section("FINAL VITERBI TABLE")
print("\n{:<10}".format("Tag"), end="")
for word in sentence:
    print("{:<15}".format(word), end="")
print()
print("-" * (10 + 15 * len(sentence)))
for tag in tags:
    print("{:<10}".format(tag), end="")
    for i in range(len(sentence)):
        value = viterbi[i].get(tag, 0)
        print("{:<15.8f}".format(value), end="")
    print()
# ---------------------------------------------------------------------------
# Final state: transition into the end marker
# ---------------------------------------------------------------------------
print_section("FINAL STATE")
last_column = viterbi[-1]
best_final_tag = None
best_final_probability = 0
for tag in last_column:
    end_probability = transition_probability.get((tag, END), 0)
    final_probability = last_column[tag] * end_probability
    print(f"{tag} -> {END} : {final_probability:.8f}")
    if final_probability > best_final_probability:
        best_final_probability = final_probability
        best_final_tag = tag
# ---------------------------------------------------------------------------
# Backtracking
# ---------------------------------------------------------------------------
print_section("BACKTRACKING")
if best_final_tag is None:
    print("No valid Viterbi sequence found.")
else:
    best_tags = [best_final_tag]
    for i in range(len(sentence) - 1, 0, -1):
        best_tags.append(backpointer[i][best_tags[-1]])
    best_tags.reverse()
    print("\nBacktracking path:")
    for word, tag in zip(sentence, best_tags):
        print(word, "->", tag)
    print_section("FINAL TAGGED SENTENCE")
    print(" ".join(f"{word}/{tag}" for word, tag in zip(sentence, best_tags)))
