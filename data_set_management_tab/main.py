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
        text = ''
        try:
            file = open(file_name)
            text = file.read()
            print(text)
        except Exception as e:
            print(e)
        finally:
            file.close()
        try:
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
            cur.execute('SELECT title, text FROM texts WHERE title = ? OR id = ?', (search_term, search_term))
            rows = cur.fetchall()
            conn.close()
            formatted_rows = [(f"Title: {row[0]}, Text: {row[1]}") for row in rows]
            return formatted_rows
        except Exception as e:
            print("An error occurred:", e)

    def update_data(self, search_term, new_title, new_text):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute('UPDATE texts SET title = ?, text = ? WHERE title = ? OR id = ?', (new_title, new_text, search_term, search_term))
            conn.commit()
            conn.close()
            print("Data has been updated.")
        except Exception as e:
            print("An error occurred:", e)

    def delete_data(self, search_term):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute('DELETE FROM texts WHERE title = ? OR id = ?', (search_term, search_term))
            conn.commit()
            conn.close()
            print("Data has been deleted.")
        except Exception as e:
            print("An error occurred:", e)

def main():
    handler = TextFileCRUD(dbname='FILE.db')
    handler.create_table()
    while True:
        operation = input("Please input the operation (C: Create, R: Read, U: Update, D: Delete, Q: Quit): ")

        if operation.upper() == "C":
            title = input("Please input the title: ")
            file_path = input("Please input the file path: ")
            handler.insert_data(title, file_path)

        elif operation.upper() == "R":
            search_term = input("Please input the title or ID to search: ")
            result = handler.read_data(search_term)
            print("\n".join(result))

        elif operation.upper() == "U":
            search_term = input("Please input the title or ID to update: ")
            new_title = input("Please input the new title: ")
            new_text = input("Please input the new text: ")
            handler.update_data(search_term, new_title, new_text)

        elif operation.upper() == "D":
            search_term = input("Please input the title or ID to delete: ")
            handler.delete_data(search_term)

        elif operation.upper() == "Q":
            break

        else:
            print("Invalid operation.")

if __name__ == "__main__":
    main()