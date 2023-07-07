import sqlite3
import csv

print('start')
conn = sqlite3.connect('/Users/a/Downloads/9.db')
cursor = conn.cursor()
cursor.execute("select * from alarm_daily;")
with open("out.csv", 'w',newline='') as csv_file: 
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) 
    csv_writer.writerows(cursor)
conn.close()
print('finish')
