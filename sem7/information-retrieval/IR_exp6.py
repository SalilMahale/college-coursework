import re
import ir_datasets
import nltk
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOP_WORDS = set(stopwords.words('english'))

dataset = ir_datasets.load("cranfield")
docs = {d.doc_id: d.text for d in dataset.docs_iter()}
queries = {q.query_id: q.text for q in dataset.queries_iter()}

FEEDBACK = {
    "3":  (["1", "2", "3", "4", "5"], ["6", "7", "8", "9", "10"]),
    "29": (["250", "514", "609", "225", "793"], ["797", "420", "683", "211", "927"]),
}

alpha, beta, gamma = 1.0, 0.75, 0.15
TOP_K = 10

def preprocess(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS]

def relevance_feedback(query_id, Dr, Dn):
    original_query = queries[query_id]
    query_tf = Counter(preprocess(original_query))
    doc_tf = {d: Counter(preprocess(docs[d])) for d in Dr + Dn}
    vocabulary = set(query_tf)
    for d in Dr + Dn:
        vocabulary |= set(doc_tf[d])
    rows = []
    for term in sorted(vocabulary):
        q = query_tf[term]
        sum_rel = sum(doc_tf[d][term] for d in Dr)
        sum_non = sum(doc_tf[d][term] for d in Dn)
        max_non = max(doc_tf[d][term] for d in Dn)
        rocchio = alpha * q + (beta / len(Dr)) * sum_rel - (gamma / len(Dn)) * sum_non
        ide_regular = alpha * q + beta * sum_rel - gamma * sum_non
        ide_dec_hi = alpha * q + beta * sum_rel - gamma * max_non
        rows.append([term, q, sum_rel, sum_non,
                     max(0, rocchio), max(0, ide_regular), max(0, ide_dec_hi)])
    table = pd.DataFrame(rows, columns=["keyword", "query", "Dr", "Dn",
                                        "Rocchio", "Ide_Regular", "Ide_Dec_Hi"])
    table = table.sort_values("Rocchio", ascending=False, kind="stable").round(2)
    print("Original Query:", original_query.replace("\n", " "))
    print("\nModified Query Terms Table:")
    print(table.head(20).to_string(index=False))
    print("\nModified Queries:")
    for method in ["Rocchio", "Ide_Regular", "Ide_Dec_Hi"]:
        top_terms = table.sort_values(method, ascending=False, kind="stable").head(TOP_K)
        top_terms = top_terms[top_terms[method] > 0]["keyword"]
        print(f"{method}: {' '.join(top_terms)}")

for query_id, (Dr, Dn) in FEEDBACK.items():
    print("=" * 90)
    print("Query ID:", query_id)
    relevance_feedback(query_id, Dr, Dn)
    print()
