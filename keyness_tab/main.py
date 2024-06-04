import sqlite3
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import math

# Database connection and query function
def load_text_from_db(title):
    conn = sqlite3.connect('FILE.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM texts WHERE title=?", (title,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return ""

# Tokenize text content
def tokenize(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return Counter(tokens)

# Function to calculate loglikelihood
def loglikelihood(f1, f2, n1, n2):
    E1 = n1 * (f1 + f2) / (n1 + n2)
    E2 = n2 * (f1 + f2) / (n1 + n2)
    G2 = 2 * ((f1 * math.log(f1 / E1) if f1 > 0 else 0) + (f2 * math.log(f2 / E2) if f2 > 0 else 0))
    return G2

# Input title and load texts
reference_title = input("Enter the title for the reference text: ")
target_title = input("Enter the title for the target text: ")

reference_text = load_text_from_db(reference_title)
target_text = load_text_from_db(target_title)

reference_freq = tokenize(reference_text)
target_freq = tokenize(target_text)

# Total number of words in each corpus
total_reference = sum(reference_freq.values())
total_target = sum(target_freq.values())

# Calculate loglikelihood and effect size for each word in the target corpus
results = []
for word in target_freq:
    ref_count = reference_freq.get(word, 0)
    target_count = target_freq[word]

    # Loglikelihood
    ll = loglikelihood(target_count, ref_count, total_target, total_reference)
    
    # Effect size (Odds Ratio)
    odds_ratio = (target_count / total_target) / (ref_count / total_reference) if ref_count > 0 else float('inf')
    
    results.append((word, target_count, ref_count, ll, odds_ratio))

# Sort results by loglikelihood value
results.sort(key=lambda x: x[3], reverse=True)

# Display the results
for result in results:
    print(f"Word: {result[0]}, Target Freq: {result[1]}, Reference Freq: {result[2]}, LL: {result[3]:.2f}, Odds Ratio: {result[4]:.2f}")
