import os
import glob
import math
import pandas as pd

pd.set_option("display.float_format", lambda x: f"{x:.4f}")

FOLDER = os.path.dirname(os.path.abspath(__file__))

def load_documents():
    paths = sorted(glob.glob(os.path.join(FOLDER, "D*.txt")))
    if not paths:
        raise FileNotFoundError("No document files (D1.txt, D2.txt ...) found in " + FOLDER)
    collection = {}
    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path, "r", encoding="utf-8") as f:
            collection[name] = f.read().strip()
    return collection

DOCS = load_documents()
DOC_NAMES = list(DOCS.keys())
QUERY = "gold silver truck"

STOPWORDS = {"of", "in", "a", "an", "the"}

def simple_stem(word):
    word = word.lower()
    if word.endswith("ed"):
        word = word[:-1]
    return word

def tokenize(text):
    words = text.lower().replace(",", "").replace(".", "").split()
    words = [w for w in words if w not in STOPWORDS]
    return [simple_stem(w) for w in words]

for name in DOC_NAMES:
    print(f"{name} =", DOCS[name])
print("Q =", QUERY)

doc_terms = {doc: tokenize(text) for doc, text in DOCS.items()}
query_terms = tokenize(QUERY)

terms = []
for doc in DOC_NAMES:
    for term in doc_terms[doc]:
        if term not in terms:
            terms.append(term)

cluster_ids = [f"K{i+1}" for i in range(len(terms))]

print("\n" + "=" * 70)
print("STEP 1: Stopword Removal & Stemming")
print("=" * 70)
print(",".join(terms))

step2 = pd.DataFrame(index=cluster_ids)
for doc in DOC_NAMES:
    step2[doc] = [doc_terms[doc].count(term) for term in terms]
step2["fiq"] = [query_terms.count(term) for term in terms]

presence = (step2[DOC_NAMES] > 0).astype(int)

print("\n" + "=" * 70)
print("STEP 2: Intra-Cluster Similarity (TF)")
print("=" * 70)
print(step2)

N = len(DOCS)

step3_tf = step2[DOC_NAMES].astype(float).copy()
for doc in DOC_NAMES:
    max_freq = step3_tf[doc].max()
    if max_freq > 0:
        step3_tf[doc] = step3_tf[doc] / max_freq

max_freq_q = step2["fiq"].max()
fiq_norm = step2["fiq"] / max_freq_q if max_freq_q > 0 else step2["fiq"].astype(float)

def document_frequency(row):
    return int((row > 0).sum())

def idf(n):
    return math.log10(1 + N / n)

step3 = step3_tf.copy()
step3["n_i"] = presence.apply(document_frequency, axis=1)
step3["idf"] = step3["n_i"].apply(idf)

print("\n" + "=" * 70)
print("STEP 3: Intra-Cluster Dissimilarity (IDF)")
print("=" * 70)
print(step3)

w_ij = step3_tf.multiply(step3["idf"], axis=0)
w_ij.columns = DOC_NAMES
w_iq = (fiq_norm + 0.5) * step3["idf"]

step4 = w_ij.copy()
step4["Wiq"] = w_iq

print("\n" + "=" * 70)
print("STEP 4: Calculate Wij and Wiq")
print("=" * 70)
print(step4)

print("\n" + "=" * 70)
print("STEP 5: To Find Similarity Value For di")
print("=" * 70)

def cosine_similarity(w_doc, w_query):
    numerator = (w_doc * w_query).sum()
    sum_wij2 = (w_doc ** 2).sum()
    sum_wiq2 = (w_query ** 2).sum()
    denominator = math.sqrt(sum_wij2 * sum_wiq2)
    return numerator, sum_wij2, sum_wiq2, denominator, numerator / denominator

sims = {}
for doc in DOC_NAMES:
    numerator, sum_wij2, sum_wiq2, denominator, similarity = cosine_similarity(w_ij[doc], w_iq)
    sims[doc] = similarity
    print(f"Sim({doc.lower()},q) = {numerator:.3f} / sqrt({sum_wij2:.3f} x {sum_wiq2:.3f}) = {numerator:.3f}/{denominator:.3f} = {similarity:.3f}")

print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
for doc, value in sims.items():
    print(f"sim({doc},Q) = {value:.3f}")
print("\nRanking (Most to Least Similar):")
for doc, value in sorted(sims.items(), key=lambda x: -x[1]):
    print(f"{doc}: {value:.3f}")
