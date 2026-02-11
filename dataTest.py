# import sqlite3

# connect = sqlite3.connect("data/database.db")
# cursor = connect.cursor()

# while True:
#     sql = input("Sql: ")
#     data = cursor.execute(sql)
#     print(data.fetchall())

from windows_toasts import WindowsToaster, Toast

toaster = WindowsToaster("Python App")
toast = Toast()
toast.text_fields = ["Hello", "Test"]
toast.on_activated = lambda _: print("Toast clciked")
toaster.show_toast(toast)
