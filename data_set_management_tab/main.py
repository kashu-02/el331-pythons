import sqlite3
from datetime import datetime

# FILE.dbの中にいろいろなデータベースがある


class TextFileCRUD:
    name = ""
    case_number = 0
    case_name = ""
    isHistory = False
    def __init__(self, dbname="FILE.db"):
        self.dbname = dbname
        #   | id | tittle | text |

    def create_table(self):
        try:
            # ディスク上のデータベースへの接続
            conn = sqlite3.connect(self.dbname)
            # SQL文を実行し、クエリから結果を取得するために、データベースカーソルを使用
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS texts(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,text TEXT)",
            )
            # cur.execute(
            #     "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT)",
            # )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,case_number INTEGER,case_name TEXT,date TEXT)",
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("An error occurred:", e)

    def insert_data(self, title, file_name):
        text = ""
        try:
            file = open(file_name, encoding="utf8", errors='ignore')
            text = file.read()
            print(text)
        except Exception as e:
            print(e)
        finally:
            file.close()
        # file_name <= fileのpath
        # text <= fileの中身
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute("INSERT INTO texts(title, text) VALUES (?, ?)", (title, text))
            conn.commit()
            conn.close()
            print("Data has been added.")
        except Exception as e:
            print("An error occurred:", e)

    def read_data(self, search_term):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute(
                "SELECT title, text FROM texts WHERE title = ? OR id = ?",
                (search_term, search_term),
            )
            # rows = [[title, text], [title, text],...]
            rows = cur.fetchall()
            conn.close()
            formatted_rows = [(f"Title: {row[0]}, Text: {row[1]}") for row in rows]
            return formatted_rows
        except Exception as e:
            print("An error occurred:", e)

    def search_data(self, search_term, target):
        if self.isHistory:
            search_term = str(self.case_number)
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute(
                "SELECT title, text FROM texts WHERE title = ? OR id = ?",
                (search_term, search_term),
            )
            rows = cur.fetchall()

            title, sentence = rows[0]
            row = list(sentence.split())

            result = []
            l = len(row)
            #            print(row[3])
            for i in range(l):
                if row[i] == target and 0 <= (i - 5) and (i + 5) <= l:
                    result.append(row[i - 5 : i + 6])
                elif row[i] == target and (i - 5) < 0 and (i + 5) < l:
                    result.append(row[0 : i + 6])
                elif row[i] == target and 0 <= (i - 5) and l < (i + 5):
                    result.append(row[i - 5 : l])
            if self.name == "":
                name = input("Please input User Name: ")
                case_number = int(input("Please input Case Number: "))
                case_name = input("Please input Case Name: ")
                now = datetime.now()
                date = now.strftime("%d %b %Y")
                self.insert_setting(name, case_number, case_name, date)
            return title, result
        except Exception as e:
            print("An error occurred:", e)

    def update_data(self, search_term, new_title, new_text):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute(
                "UPDATE texts SET title = ?, text = ? WHERE title = ? OR id = ?",
                (new_title, new_text, search_term, search_term),
            )
            conn.commit()
            conn.close()
            print("Data has been updated.")
        except Exception as e:
            print("An error occurred:", e)

    def delete_data(self, search_term):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM texts WHERE title = ? OR id = ?",
                (search_term, search_term),
            )
            conn.commit()
            conn.close()
            print("Data has been deleted.")
        except Exception as e:
            print("An error occurred:", e)

    def read_setting(self, name):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, case_number, case_name, date FROM settings WHERE name = ?",
                (name,),
            )

            rows = cur.fetchall()

            conn.close()

            formatted_rows = [(f"ID: {row[0]}, Name: {row[1]}, Case Number: {row[2]}, Case Name: {row[3]}, Date: {row[4]}") for row in rows]
            self.name = rows[0][1]
            self.case_number = int(rows[0][2])
            self.case_name = rows[0][3]
            self.isHistory = True
            return formatted_rows
        except Exception as e:
            print("An error occurred:", e)

    def insert_setting(self, name, case_number, case_name, date):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute("INSERT INTO settings(name, case_number, case_name, date) VALUES (?, ?, ?, ?)", (name, case_number, case_name, date))
            conn.commit()
            conn.close()
            print("Data has been added.")
            self.isHistory = True
        except Exception as e:
            print("An error occurred:", e)



def main():
    handler = TextFileCRUD(dbname="FILE.db")
    handler.create_table()
    while True:
        operation = input(
            "Please input the operation (C: Create, R: Read, U: Update, D: Delete, Q: Quit, S: SearchWord, L: Login): "
        )

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

        elif operation.upper() == "S":
            search_term = input("Please input the title or ID to search: ")
            result = input("Please input the target word: ")
            title, ans = handler.search_data(search_term, result)
            print(title)
            for i in ans:
                print(i)

        elif operation.upper() == "Q":
            break

        elif operation.upper() == "L":
            name = input("Please input User Name. ")
            if name == "":
                continue
            result = handler.read_setting(name)
            print(result)
            print("Login Success!")

        else:
            print("Invalid operation.")


if __name__ == "__main__":
    main()
