import string

# ---------- Step 1 : Stopword list ----------
stopwords = ["a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on",
             "for", "and", "or", "it", "its", "this", "that", "with", "as", "at",
             "by", "from", "be", "can", "will", "their", "they", "them", "he",
             "she", "his", "her", "have", "has", "not", "but", "all", "also",
             "most", "many", "very", "one", "so", "than", "then", "there",
             "these", "those", "which", "who", "you", "your", "we", "our", "i",
             "if", "do", "does", "did", "about", "into", "over", "after",
             "before", "again", "new", "now", "today", "every", "when", "how",
             "what", "both", "such", "some", "no", "yes"]


# ---------- Step 2 : Preprocessing function ----------
def preprocess(text):
    text = text.lower()                       # lowercasing
    for ch in string.punctuation:             # punctuation removal
        text = text.replace(ch, " ")
    words = text.split()                      # tokenisation
    clean = []
    for w in words:
        if w not in stopwords:                # stopword removal
            clean.append(w)
    return clean


# ---------- Step 3 : Read and preprocess the 5 documents ----------
file_names = ["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt", "doc5.txt"]
doc_names = ["DOC 1", "DOC 2", "DOC 3", "DOC 4", "DOC 5"]

documents = []
for name in file_names:
    f = open("d:/College/Sem7/IR/" + name, "r")
    documents.append(preprocess(f.read()))
    f.close()

print("All 5 documents loaded and preprocessed successfully.")

# ---------- Step 4 : Accept the user query ----------
query = input("Enter your query : ")
query_words = preprocess(query)

# ---------- Step 5 : Check whether the query words exist anywhere ----------
found = []
missing = []
for w in query_words:
    present = False
    for doc in documents:
        if w in doc:
            present = True
    if present:
        found.append(w)
    else:
        missing.append(w)

if len(missing) > 0:
    print("\nWord(s) not found in any document :", missing)

if len(found) == 0:
    print("MATCH NOT FOUND. Please try a different query.")
else:
    # ---------- Step 6 : Term Frequency Table ----------
    print("\nTERM FREQUENCY TABLE")
    header = "Document".ljust(12)
    for w in query_words:
        header = header + w.ljust(12)
    header = header + "Total"
    print(header)
    print("-" * len(header))

    scores = []
    for i in range(len(documents)):
        row = doc_names[i].ljust(12)
        total = 0
        for w in query_words:
            count = documents[i].count(w)
            total = total + count
            row = row + str(count).ljust(12)
        row = row + str(total)
        print(row)
        scores.append(total)

    # ---------- Step 7 : Rank the documents ----------
    print("\nSEARCH RESULTS (RANKED)")
    rank = 1
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    for i in order:
        if scores[i] > 0:
            print("Rank", rank, ":", doc_names[i], "--> Score :", scores[i])
            rank = rank + 1

    if rank == 1:
        print("MATCH NOT FOUND. No document contains the query terms.")
