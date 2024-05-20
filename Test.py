import re
import os
import datetime
import sqlite3

class TextFileCRUD:
    def __init__(self, dbname='FILE.db'):
        self.dbname = dbname

    def create_table(self):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS texts(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,text TEXT)')
            conn.commit()
            conn.close()
        except Exception as e:
            print("An error occurred:", e)

    def insert_data(self, title, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                text = file.read()
                conn = sqlite3.connect(self.dbname)
                cur = conn.cursor()
                cur.execute('INSERT INTO texts(title, text) VALUES (?, ?)', (title, text))
                conn.commit()
                conn.close()
                print("Data has been added.")
        except Exception as e:
            print("An error occurred:", e)

    def read_data(self, search_term):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute('SELECT id, title, text FROM texts WHERE title = ? OR id = ?', (search_term, search_term))
            rows = cur.fetchall()
            conn.close()
            formatted_rows = [(f"Title: {row[0]}, Text: {row[1]}") for row in rows]
            return formatted_rows
        except Exception as e:
            print("An error occurred:", e)

    def search_and_save(self, search_term):
        try:
            rows = self.read_data(search_term)
            if not rows:
                print("No matching data found.")
                return

            for row in rows:
                file_id, title, text = row
                search_results = self.search_text(text, search_term)
                if search_results:
                    self.save_search_result(file_id, title, search_term, search_results)
                    print(f"Search results for '{search_term}' in '{title}' have been saved.")
                else:
                    print(f"No occurrences of '{search_term}' found in '{title}'.")
        except Exception as e:
            print("An error occurred:", e)

    def search_text(self, text, search_term):
        search_results = []

        # Find all occurrences of the search term in the text
        matches = re.finditer(r'\b{}\b'.format(re.escape(search_term)), text, re.IGNORECASE)
        for match in matches:
            start_index = max(0, match.start() - 10)  # Index of 5 words to the left
            end_index = min(len(text), match.end() + 10)  # Index of 5 words to the right
            context = text[start_index:end_index]
            # Colorize the search term
            colored_context = context.replace(search_term, '\033[91m{}\033[0m'.format(search_term), 1)
            search_results.append(colored_context)

        return search_results

    def save_search_result(self, file_id, title, search_term, search_results):
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        initials = ''.join(word[0] for word in title.split())
        file_name = f"{file_id}-{timestamp}-{initials}-{search_term}.txt"
        save_directory = "search_results"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        file_path = os.path.join(save_directory, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Search results for '{search_term}' in '{title}':\n\n")
            for result in search_results:
                file.write(result + "\n")

        print(f"Search results saved to: {file_path}")


def main():
    handler = TextFileCRUD(dbname='FILE.db')
    handler.create_table()
    while True:
        operation = input("Please input the operation (C: Create, R: Read, S: Search and Save, Q: Quit): ")

        if operation.upper() == "C":
            title = input("Please input the title: ")
            file_path = input("Please input the file path: ")
            handler.insert_data(title, file_path)

        elif operation.upper() == "R":
            search_term = input("Please input the title or ID to search: ")
            result = handler.read_data(search_term)
            print("\n".join(result))

        elif operation.upper() == "S":
            search_term = input("Enter the search term: ")
            handler.search_and_save(search_term)

        elif operation.upper() == "Q":
            break

        else:
            print("Invalid operation.")

if __name__ == "__main__":
    main()
