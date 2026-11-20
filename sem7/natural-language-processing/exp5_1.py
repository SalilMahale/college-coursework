# Exercise 4: Comparing NLTK and spaCy NER on the same text
import nltk
import spacy
from nltk import word_tokenize, pos_tag, ne_chunk

# same input text as Question 2 and Question 3
text = """Barack Obama visited Paris on Monday.
Microsoft opened an office in California.
Albert Einstein worked at Princeton University.
The company earned 5 million dollars in 2025.
Mount Everest is located in Nepal near the Himalayas."""

# NLTK and spaCy use different names for the same types
same_type = {"ORGANIZATION": "ORG", "LOCATION": "LOC",
             "FACILITY": "FAC"}

# NLTK entities as {entity text: label}  (data downloaded in Question 2)
result = ne_chunk(pos_tag(word_tokenize(text)))
nltk_ents = {" ".join(word for word, tag in subtree.leaves()): subtree.label()
             for subtree in result if hasattr(subtree, "label")}

# spaCy entities as {entity text: label}
nlp = spacy.load("en_core_web_sm")
spacy_ents = {ent.text: ent.label_ for ent in nlp(text).ents}

# union of both, in order of appearance in the text
all_ents = set(nltk_ents) | set(spacy_ents)
all_ents = sorted(all_ents, key=lambda e: (text.find(e), -len(e)))

# Print input text first
print("INPUT TEXT")
print("-----------")
print(text)
print()

# Comparison output
print("NLTK vs SPACY NER COMPARISON")
print("----------------------------")
print(f"{'Entity':<22}{'NLTK':<15}{'spaCy':<9}Result")
print("-" * 60)
for e in all_ents:
    n = nltk_ents.get(e, "-")
    s = spacy_ents.get(e, "-")
    if n == "-":
        result_type = "Only spaCy"
    elif s == "-":
        result_type = "Only NLTK"
    elif same_type.get(n, n) == s:
        result_type = "Match"
    else:
        result_type = "Type differs"
    print(f"{e:<22}{n:<15}{s:<9}{result_type}")

print("\nEntities found by NLTK :", len(nltk_ents))
print("Entities found by spaCy:", len(spacy_ents))
print("Types used by NLTK     :", sorted(set(nltk_ents.values())))
print("Types used by spaCy    :", sorted(set(spacy_ents.values())))
