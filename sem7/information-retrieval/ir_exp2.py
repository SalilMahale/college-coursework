import re
import unicodedata
import pandas as pd
from collections import Counter

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from textblob import TextBlob

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

text = input('Enter the paragraph: ')

print("=" * 70)
print("ORIGINAL TEXT")
print("=" * 70)
print(text)

accent_removed = (
    unicodedata.normalize('NFKD', text)
    .encode('ASCII', 'ignore')
    .decode('utf-8')
)

print("\n==========================")
print("1. ACCENT REMOVAL")
print("==========================")
print(accent_removed)

whitespace_removed = re.sub(r'\s+', ' ', accent_removed).strip()

print("\n==========================")
print("2. WHITE SPACE REMOVAL")
print("==========================")
print(whitespace_removed)

print("\n==========================")
print("3. CASE CONVERSION")
print("==========================")

print("\nCase Sensitive Text:")
print(whitespace_removed)

lower_text = whitespace_removed.lower()

print("\nLower Case Text:")
print(lower_text)

tokens = word_tokenize(lower_text)

print("\n==========================")
print("4. TOKENIZATION")
print("==========================")
print(tokens)

stop_words = set(stopwords.words('english'))

filtered_tokens = []

for word in tokens:
    if word.isalpha():
        if word not in stop_words:
            filtered_tokens.append(word)

print("\n==========================")
print("5. STOP WORD REMOVAL")
print("==========================")
print(filtered_tokens)

blob = TextBlob(lower_text)
noun_phrases = blob.noun_phrases

print("\n==========================")
print("6. NOUN GROUP IDENTIFICATION")
print("==========================")

for np in noun_phrases:
    print(np)

lemmatizer = WordNetLemmatizer()

# Convert Penn Treebank POS tags to WordNet POS tags
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

tagged_words = pos_tag(filtered_tokens)

lemmas = []

for word, tag in tagged_words:
    wn_tag = get_wordnet_pos(tag)
    lemmas.append(lemmatizer.lemmatize(word, wn_tag))

stemmer = PorterStemmer()

stems = []

for word in filtered_tokens:
    stems.append(stemmer.stem(word))

print("\n==========================")
print("7 & 8. LEMMATIZATION vs STEMMING")
print("==========================")

df = pd.DataFrame({
    "Original Word": filtered_tokens,
    "Lemmatization": lemmas,
    "Stemming": stems
})

print(df)
print("\n=== Step 9: Indexing ===")
final_terms = sorted(set(lemmas))
print(final_terms)