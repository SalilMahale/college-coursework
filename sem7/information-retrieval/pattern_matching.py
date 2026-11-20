"""
Experiment 5: Pattern Matching for Information Retrieval
Supports: Exact word match, Prefix, Suffix, Substring, Lexical Range,
          Approximate (fuzzy) search using edit distance, and Regular Expressions.
"""

import os
import re
import glob
import difflib

WORD_PATTERN = r"[A-Za-z0-9']+"

# Folder holding one text file per document, placed beside this program.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "documents")


# ------------------------- Step 1: Load Dataset -------------------------

def natural_key(file_path):
    """Sort file names so that D2 comes before D10 instead of after it."""
    name = os.path.basename(file_path)
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r'(\d+)', name)]


def load_documents(folder=DATA_DIR):
    """Read every .txt file of the folder as one document.

    The document ID is the file name without its extension (D1.txt -> D1)
    and the document text is the entire content of that file.
    """
    documents = []

    if not os.path.isdir(folder):
        print(f"Document folder not found: {folder}")
        return documents

    for file_path in sorted(glob.glob(os.path.join(folder, "*.txt")), key=natural_key):
        with open(file_path, "r", encoding="utf-8") as document_file:
            text = " ".join(line.strip() for line in document_file if line.strip())

        if text:
            doc_id = os.path.splitext(os.path.basename(file_path))[0]
            documents.append((doc_id, text))

    return documents


DOCUMENTS = load_documents()


# ------------------------- Helper Functions -------------------------

def split_sentences(text):
    """Split a document into individual sentences."""
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]


def get_words(sentence):
    """Return every word of a sentence along with its start and end position."""
    return [(m.group(), m.start(), m.end()) for m in re.finditer(WORD_PATTERN, sentence)]


def build_vocabulary():
    """Collect the set of all distinct words present in the whole collection."""
    vocabulary = set()
    for _, text in DOCUMENTS:
        for word in re.findall(WORD_PATTERN, text):
            vocabulary.add(word.lower())
    return sorted(vocabulary)


def highlight(sentence, spans):
    """Insert markers around every matched portion of the sentence."""
    spans = sorted(set(spans))
    output = sentence
    for start, end in reversed(spans):
        output = output[:start] + "[" + output[start:end] + "]" + output[end:]
    return output


def edit_distance(source, target):
    """Levenshtein distance: minimum insertions, deletions and replacements."""
    m, n = len(source), len(target)
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        table[i][0] = i
    for j in range(n + 1):
        table[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if source[i - 1] == target[j - 1] else 1
            table[i][j] = min(table[i - 1][j] + 1,        # deletion
                              table[i][j - 1] + 1,        # insertion
                              table[i - 1][j - 1] + cost)  # replacement
    return table[m][n]


# ------------------------- Step 3: Perform Matching -------------------------

def match_sentence(sentence, search_type, pattern, fuzzy_words=None):
    """Return the list of matched spans found inside one sentence."""
    spans = []
    key = pattern.lower()

    if search_type == "exact":
        for word, start, end in get_words(sentence):
            if word.lower() == key:
                spans.append((start, end))

    elif search_type == "prefix":
        for word, start, end in get_words(sentence):
            if word.lower().startswith(key):
                spans.append((start, end))

    elif search_type == "suffix":
        for word, start, end in get_words(sentence):
            if word.lower().endswith(key):
                spans.append((start, end))

    elif search_type == "substring":
        for m in re.finditer(re.escape(pattern), sentence, re.IGNORECASE):
            spans.append((m.start(), m.end()))

    elif search_type == "regex":
        for m in re.finditer(pattern, sentence, re.IGNORECASE):
            if m.group():
                spans.append((m.start(), m.end()))

    elif search_type == "range":
        low, high = [w.strip().lower() for w in re.split(r'[-,\s]+', pattern) if w.strip()][:2]
        for word, start, end in get_words(sentence):
            if low <= word.lower() <= high:
                spans.append((start, end))

    elif search_type == "approximate":
        for word, start, end in get_words(sentence):
            if word.lower() in fuzzy_words:
                spans.append((start, end))

    return spans


def search(search_type, pattern, max_errors=2):
    """Run the selected pattern matching method over the whole collection."""
    fuzzy_words = {}

    if search_type == "approximate":
        candidates = difflib.get_close_matches(pattern.lower(), build_vocabulary(),
                                               n=25, cutoff=0.6)
        for candidate in candidates:
            distance = edit_distance(pattern.lower(), candidate)
            if distance <= max_errors:
                fuzzy_words[candidate] = distance
        print("Fuzzy candidates (word : edit distance) ->",
              ", ".join(f"{w} : {d}" for w, d in fuzzy_words.items()) or "none")

    # ------------------------- Step 4: Display Results -------------------------
    total = 0
    for doc_id, text in DOCUMENTS:
        for sentence in split_sentences(text):
            spans = match_sentence(sentence, search_type, pattern, fuzzy_words)
            if spans:
                total += 1
                print(f"{doc_id} : {highlight(sentence, spans)}")

    if total == 0:
        print("No matching sentence found in the collection.")
    else:
        print(f"Total matching sentences : {total}")


# ------------------------- Step 2: Input Pattern and Search Type -------------------------

SEARCH_TYPES = ["exact", "prefix", "suffix", "substring", "range", "approximate", "regex"]


def main():
    print("Pattern Matching for Information Retrieval")

    if not DOCUMENTS:
        print("No documents loaded. Please check the documents folder.")
        return

    print(f"Loaded {len(DOCUMENTS)} documents :", ", ".join(d for d, _ in DOCUMENTS))
    print("Available search types :", ", ".join(SEARCH_TYPES))
    print("Type 'quit' as the search type to stop.\n")

    while True:
        search_type = input("Enter search type: ").strip().lower()

        if search_type == "quit":
            print("Search session ended.")
            break

        if search_type not in SEARCH_TYPES:
            print("Invalid search type. Please choose from the list above.\n")
            continue

        if search_type == "range":
            pattern = input("Enter range (start word - end word): ").strip()
        else:
            pattern = input("Enter pattern: ").strip()

        if not pattern:
            print("Pattern cannot be empty.\n")
            continue

        print()
        search(search_type, pattern)
        print()


if __name__ == "__main__":
    main()
