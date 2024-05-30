import sqlite3
from collections import Counter, defaultdict

def fetch_texts_and_titles(db_path):
    # データベースからタイトルとテキストを取得
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, text FROM texts")
    data = cursor.fetchall()
    conn.close()
    return data

def analyze_texts(texts):
    word_counts = []
    for text in texts:
        words = text.split()
        word_counts.append(Counter(words))
    
    all_words = set()
    for wc in word_counts:
        all_words.update(wc.keys())
    
    # 単語の出現状況を集計
    data = defaultdict(lambda: ['-'] * len(texts))
    total_counts = defaultdict(int)
    for idx, wc in enumerate(word_counts):
        for word in wc:
            if data[word][idx] == '-':
                data[word][idx] = wc[word]
            else:
                data[word][idx] += wc[word]
            total_counts[word] += wc[word]

    # 単語を出現回数の合計で降順にソート
    sorted_words = sorted(all_words, key=lambda word: -total_counts[word])
    for word in sorted_words:
        counts = ','.join(str(count) if count != '-' else '-' for count in data[word])
        print(f"{word}: {counts}")

# 使用例
db_path = 'FILE.db'  # SQLiteデータベースファイルのパスを設定
data = fetch_texts_and_titles(db_path)
titles, texts = zip(*data)
print("Titles:", ", ".join(titles))
analyze_texts(texts)
