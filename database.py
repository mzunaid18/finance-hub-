import sqlite3


connection = sqlite3.connect("finance.db")

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    date TEXT,

    category TEXT,

    type TEXT,

    amount INTEGER

)
""")


connection.commit()

connection.close()


print("New Database Created")
connection.close()


print("New Database Created")