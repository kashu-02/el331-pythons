import sqlite3
from collections import Counter
import re


def get_text(title):
    conn = sqlite3.connect('FILE.db')
    c = conn.cursor()
    c.execute('SELECT text FROM texts WHERE title = ?', (title,))
    text = c.fetchall()
    conn.close()
    return text[0][0]


def tokenize(text):
    print(type(text))
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def count_words(words):
    return Counter(words)


def count_common_words(count1, count2):
    common_words_set = set(count1.keys()) & set(count2.keys())
    common_counts = {word: (count1[word], count2[word], count1[word] + count2[word]) for word in common_words_set}
    common_counts = sorted(common_counts.items(), key=lambda x: x[1][2], reverse=True)
    return common_counts


def common_words(title1, title2):
    text1 = get_text(title1)
    text2 = get_text(title2)

    words1 = tokenize(text1)
    words2 = tokenize(text2)

    count1 = count_words(words1)
    count2 = count_words(words2)

    common_counts = count_common_words(count1, count2)

    return common_counts


def main():
    print("Put the titles of the plays you want to compare")
    title1 = input("Title 1: ")
    title2 = input("Title 2: ")
    common_words_list = common_words(title1, title2)

    current_page = 0
    print(f"Common words in {title1} and {title2}:")
    # list top 20 common words
    for word, counts in common_words_list[:20]:
        print(f"{word}: {counts[0]} in {title1}, {counts[1]} in {title2}, total {counts[2]}")

    while current_page < len(common_words_list):
        print("Press 'n' for next page, 'p' for previous page, 'q' to quit: ")
        user_input = input()
        if user_input == 'n':
            current_page += 20
            for word, counts in common_words_list[current_page:current_page + 20]:
                print(f"{word}: {counts[0]} in {title1}, {counts[1]} in {title2}, total {counts[2]}")
        elif user_input == 'p':
            current_page -= 20
            for word, counts in common_words_list[current_page:current_page + 20]:
                print(f"{word}: {counts[0]} in {title1}, {counts[1]} in {title2}, total {counts[2]}")
        elif user_input == 'q':
            break
        else:
            print("Invalid input")




main()
