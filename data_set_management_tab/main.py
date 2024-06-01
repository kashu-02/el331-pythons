import re
import os
import datetime
import sqlite3
from datetime import datetime


def record_option(func):
    def wrapper(*args, **kwargs):
        option_name = func.__name__
        with open("option_record.txt", "a") as file:
            try:
                file.write(option_name + " ")
                for i in args[1:]:
                    try:
                        file.write(i + " ")
                    except:
                        file.write(str(i) + " ")
            except:
                file.write("error")
            file.write("\n")
            file.close()
        return func(*args, **kwargs)

    return wrapper


class TextFileCRUD:
    name = ""
    case_number = 0
    case_name = ""
    isHistory = False

    @classmethod
    @record_option
    def __init__(self, dbname="FILE.db"):
        self.dbname = dbname
        #   | id | tittle | text |

    @classmethod
    @record_option
    def create_table(self):
        try:
            conn = sqlite3.connect(self.dbname)
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

    @classmethod
    @record_option
    def insert_data(self, title, file_name):
        text = ""
        try:
            file = open(file_name, encoding="utf8", errors="ignore")
            text = file.read()
            print(text)
        except Exception as e:
            print(e)
        finally:
            file.close()
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute("INSERT INTO texts(title, text) VALUES (?, ?)", (title, text))
            conn.commit()
            conn.close()
            print("Data has been added.")
        except Exception as e:
            print("An error occurred:", e)

    @classmethod
    @record_option
    def read_data(self, search_term):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            cur.execute(
                "SELECT title, text FROM texts WHERE title = ? OR id = ?",
                (search_term, search_term),
            )
            rows = cur.fetchall()
            conn.close()
            formatted_rows = [(f"Title: {row[0]}, Text: {row[1]}") for row in rows]
            return formatted_rows
        except Exception as e:
            print("An error occurred:", e)


    @classmethod
    @record_option
    def search_data(self, search_term, target):
        if self.isHistory:
            search_term = str(self.case_number)
        try:
            conn = sqlite3.connect(self.dbname)

            def trace_callback(statement):
                print(f"Query executed: {statement}")

            conn.set_trace_callback(trace_callback)  # 追加された部分
            cur = conn.cursor()
            cur.execute("SELECT id, title, text FROM texts WHERE title = ? OR id = ?", (search_term, search_term))
            rows = cur.fetchall()
            conn.close()

            if not rows:
                print(f"No results found for '{search_term}'.")
                return

            file_id, title, sentence = rows[0]
            row = list(sentence.split())
            result = []
            l = len(row)
            for i in range(l):
                if row[i] == target and 0 <= (i - 5) and (i + 5) <= l:
                    result.append(' '.join(row[i - 5 : i + 6]))
                elif row[i] == target and (i - 5) < 0 and (i + 5) < l:
                    result.append(' '.join(row[0 : i + 6]))
                elif row[i] == target and 0 <= (i - 5) and l < (i + 5):

                    result.append(' '.join(row[i - 5 : l]))

            if result:
                self.save_search_result(file_id, title, target, result)
                print(f"Search results for '{target}' in '{title}' have been saved.")
            else:
                print(f"No occurrences of '{target}' found in '{title}'.")
        except Exception as e:
            print("An error occurred:", e)

    @classmethod
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

    @classmethod
    @record_option
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

    @classmethod
    @record_option
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

        elif operation.upper() == "S":
            search_term = input("Please input the title or ID to search: ")
            target = input("Please input the target word: ")
            handler.search_data(search_term, target)

        elif operation.upper() == "D":
            search_term = input("Please input the title or ID to delete: ")
            handler.delete_data(search_term)

        elif operation.upper() == "S":
            search_term = input("Please input the title or ID to search: ")
            target = input("Please input the target word: ")
            title, ans = handler.search_data(search_term, target)
            if title == None:
                continue
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
