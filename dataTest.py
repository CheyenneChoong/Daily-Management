import sqlite3

connect = sqlite3.connect("data/database.db")
cursor = connect.cursor()

while True:
    sql = input("Sql: ")
    data = cursor.execute(sql)
    print(data.fetchall())
