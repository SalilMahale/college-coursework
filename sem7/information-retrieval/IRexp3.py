import os
import re
import pandas as pd
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

stop_words = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "am",
    "of", "to", "in", "on", "at", "for", "with", "by", "from", "as",
    "and", "or", "not", "but", "if", "then", "than", "so",
    "this", "that", "these", "those", "it", "its", "he", "she", "they",
    "we", "you", "i", "his", "her", "their", "our", "your", "my"
}

folder = "."
line = "=" * 40


# ---------- PREPROCESSING ----------
def preprocess(text):
    words = re.findall(r"[a-z]+", text.lower())
    return [stemmer.stem(w) for w in words if w not in stop_words]


# ---------- QUERY TOKENIZER ----------
def tokenize_query(query):
    query = query.lower().replace("(", " ( ").replace(")", " ) ")
    return query.split()


# ---------- DNF CHECK ----------
def is_dnf(query):
    depth = 0
    for token in tokenize_query(query):
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
        elif token == "or" and depth > 0:
            return False
    return True


# ---------- DNF CONVERSION (RECURSIVE PARSER) ----------
def parse_or(tokens):
    clauses = parse_and(tokens)
    while tokens and tokens[0] == "or":
        tokens.pop(0)
        clauses = clauses + parse_and(tokens)
    return clauses


def parse_and(tokens):
    clauses = parse_literal(tokens)
    while tokens and tokens[0] == "and":
        tokens.pop(0)
        right = parse_literal(tokens)
        clauses = [a + b for a in clauses for b in right]
    return clauses


def parse_literal(tokens):
    if tokens[0] == "(":
        tokens.pop(0)
        clauses = parse_or(tokens)
        tokens.pop(0)
        return clauses
    if tokens[0] == "not":
        tokens.pop(0)
        return [["not " + tokens.pop(0)]]
    return [[tokens.pop(0)]]


def to_dnf(query):
    return parse_or(tokenize_query(query))


# ---------- LOAD DOCUMENTS ----------
documents = []
files = sorted([f for f in os.listdir(folder) if f.endswith(".txt")])
if len(files) == 0:
    print("No .txt files found.")
    exit()

print("\nDocuments Loaded:\n")
for file in files:
    with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
        documents.append(f.read().strip())
    print(file)

n = len(documents)
query = input("\nEnter Boolean Query: ").lower()

# ---------- STEP 1 ----------
print("\n" + line)
print("STEP 1 : TOKENIZATION + STOPWORD REMOVAL + STEMMING")
print(line)
processed_docs = []
for i, doc in enumerate(documents, 1):
    tokens = preprocess(doc)
    processed_docs.append(tokens)
    print(f"\nD{i}")
    print("Original :", doc)
    print("Processed:", tokens)

# ---------- STEP 2 ----------
print("\n" + line)
print("STEP 2 : TERM x DOCUMENT MATRIX")
print(line)
terms = sorted(set(sum(processed_docs, [])))
matrix = {
    f"D{i + 1}": [1 if term in processed_docs[i] else 0 for term in terms]
    for i in range(n)
}
term_doc = pd.DataFrame(matrix, index=terms)
print(term_doc)

# ---------- STEP 3 ----------
print("\n" + line)
print("STEP 3 : CHECK WHETHER QUERY IS DNF")
print(line)
clauses = to_dnf(query)
if is_dnf(query):
    print("The query is already in DNF.")
else:
    print("The query is NOT in DNF. Converting using the distributive law...")
dnf_text = " OR ".join("(" + " AND ".join(c) + ")" for c in clauses)
print("DNF Form :", dnf_text.upper())

# ---------- STEP 4 ----------
print("\n" + line)
print("STEP 4 : QUERY CLAUSE COMPARISON (QCC)")
print(line)
final = {}
for q, clause in enumerate(clauses, 1):
    print(f"\nQCC {q} : {' AND '.join(clause).upper()}")
    table = []
    for d, doc in enumerate(processed_docs, 1):
        row = {"Document": f"D{d}"}
        qcc = 1
        for term in clause:
            if term.startswith("not "):
                word = stemmer.stem(term[4:].strip())
                value = 0 if word in doc else 1
            else:
                word = stemmer.stem(term)
                value = 1 if word in doc else 0
            row[term] = value
            qcc &= value
        row[f"QCC{q}"] = qcc
        final.setdefault(f"D{d}", []).append(qcc)
        table.append(row)
    print(pd.DataFrame(table).to_string(index=False))

# ---------- STEP 5 ----------
print("\n" + line)
print("STEP 5 : SIMILARITY AND FINAL RESULT")
print(line)
rows = []
for doc, values in final.items():
    row = {"Document": doc}
    for i, value in enumerate(values, 1):
        row[f"QCC{i}"] = value
    row["sim(dj,q)"] = max(values)
    rows.append(row)
final_df = pd.DataFrame(rows)
print(final_df.to_string(index=False))

retrieved = final_df[final_df["sim(dj,q)"] == 1]["Document"].tolist()
print("\nRetrieved Documents:")
print(", ".join(retrieved) if retrieved else "No document retrieved.")