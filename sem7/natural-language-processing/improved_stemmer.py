# Modified Porter Stemmer - corrects words the original algorithm stems wrongly
from porter_stemmer import porter_stem

# Fix 1: irregular words that Porter over-stems or cannot handle
EXCEPTIONS = {
    "news": "news",
    "universal": "universal",
    "university": "university",
    "universe": "universe",
    "mice": "mouse",
    "feet": "foot",
    "children": "child",
}

def improved_stem(word):
    """Porter stem plus two corrections."""
    w = word.lower()

    if w in EXCEPTIONS:                   # Fix 1: direct dictionary lookup
        return EXCEPTIONS[w]

    stem = porter_stem(w)

    # Fix 2: restore the 'y' that Step 1c had converted into 'i'
    if stem.endswith("i") and (w.endswith("y") or w.endswith("ies") or w.endswith("ied")):
        stem = stem[:-1] + "y"
    return stem

if __name__ == "__main__":
    text = input("Enter words: ")
    print("\nWord            Porter Stem     Corrected Stem")
    for word in text.split():
        print(f"{word:<16}{porter_stem(word):<16}{improved_stem(word)}")