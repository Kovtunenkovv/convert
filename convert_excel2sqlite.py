import openpyxl
import sqlite3
import os
import datetime

start_time = datetime.datetime.now()

try:
    db_connection = sqlite3.connect('db\\9.db')
    sql_query = '''CREATE TABLE IF NOT EXISTS alarm_daily (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                zip TEXT,
                                site TEXT,
                                hostname TEXT NOT NULL,
                                firstoccurrence DATE,
                                enddate DATE,
                                severity TEXT,
                                eventid TEXT,
                                additionalinfo1 text);'''

    sql_query2 = '''CREATE TABLE IF NOT EXISTS alarm_date (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 start_date DATE);'''

    sql_query1 = '''SELECT start_date
                      FROM alarm_date;'''

    db_cursor = db_connection.cursor()
    print("База данных подключена к SQLite")
    db_cursor.execute(sql_query)
    db_connection.commit()
    print("Таблица alarm_dailu создана")

    db_cursor.execute(sql_query2)
    db_connection.commit()

    db_cursor.execute(sql_query1)
    db_connection.commit()

    date_list = list()

    for result in db_cursor:
        date_list.append(result[0])
    
    print(date_list)

    path = "L:\\technical\\Эксплуатация_БС_UMTS\\Регламент_эксплуатация\\Распределение по группам\\Зона 3\\ЗИП\\!Ковтуненко\\Alarms Ericsson daily MOS\\"
    
    path_bs = "excel\\bs_reg.xlsx"

    dir_list = os.listdir(path)

    
    wb_bs = openpyxl.load_workbook(filename = path_bs, read_only = True)
    ws_bs = wb_bs.active

    bs_list = list()
    bs_dict = dict()

    for row in ws_bs.iter_rows():
        bs_list = list()
        for cell in row:
            bs_list.append(cell.value)
        bs_dict[bs_list[0]] = bs_list[1]

    for wb_dir in dir_list:
        
        wb = openpyxl.load_workbook(filename = path + wb_dir, read_only = True)
        print("Файл " + path + wb_dir + " открыт")
        ws = wb.active

        s_temp = ws.cell(2,4).value
        d_tepm = datetime.datetime.strptime(s_temp, "%Y/%m/%d %H:%M:%S")
        d_temp = d_tepm.strftime("%Y-%m-%d")
        if d_temp in date_list:
            print("Файл " + path + wb_dir + " добавлен ранее! ")
            continue 

        sql_query3 = f'''INSERT INTO alarm_date (start_date) VALUES ("{d_temp}");'''
        db_cursor.execute(sql_query3)
        db_connection.commit()

        sql_query = '''INSERT INTO alarm_daily (
                            zip, site, hostname, firstoccurrence, enddate, severity, eventid,
                            additionalinfo1)
                            VALUES (?,?,?,?,?,?,?,?);'''

        i = 0
        dbdata = list()
        for row in ws.iter_rows(min_row=2, max_col=8, max_row=100000):
            dblist = list()
                    
            for cell in row:
                dblist.append(cell.value)

            if dblist[3] != None:
                s_temp = dblist[3]
                d_tepm = datetime.datetime.strptime(s_temp, "%Y/%m/%d %H:%M:%S")
                dblist[3] = str(d_tepm.strftime("%Y-%m-%d %H:%M:%S"))
            if dblist[4] != None:
                s_temp = dblist[4]
                d_tepm = datetime.datetime.strptime(s_temp, "%Y/%m/%d %H:%M:%S")
                dblist[4] = str(d_tepm.strftime("%Y-%m-%d %H:%M:%S"))

            if dblist[2] != None:
                if len(dblist[2]) == 6:

                    if dblist[2] in bs_dict:
                        dblist[0] = bs_dict[dblist[2]]
                    else:
                        dblist[0] = "BS not use"

                    i = i + 1
                    dbdata.append(dblist)
                        
                    if i == 10000:
                        db_cursor.executemany(sql_query,dbdata)
                        db_connection.commit()
                        i = 0
                        dbdata = list()
                        
                elif str(dblist[2]).find("TCU_") != -1:
                    dblist[2] = str(dblist[2])[4:10]
                    if dblist[2] in bs_dict:
                        dblist[0] = bs_dict[dblist[2]]
                    else:
                        dblist[0] = "BS not use"
                        
                    i = i + 1
                    dbdata.append(dblist)
                    
                    if i == 10000:
                        db_cursor.executemany(sql_query,dbdata)
                        db_connection.commit()
                        i = 0
                        dbdata = list()
                else:
                    dblist[2] = str(dblist[2])[0:6]
                    if dblist[2] in bs_dict:
                        dblist[0] = bs_dict[dblist[2]]
                    else:
                        dblist[0] = "BS not use"
                    i = i + 1
                    dbdata.append(dblist)
                    if i == 10000:
                        db_cursor.executemany(sql_query,dbdata)
                        db_connection.commit()
                        i = 0
                        dbdata = list()
            else:
                pass

        wb.close()
        db_cursor.executemany(sql_query,dbdata)
        db_connection.commit()
        
    db_cursor.close()

except sqlite3.Error as error:
    print("Ошибка sqlite", error)
finally:
    if (db_connection):
        db_connection.close()
        print("Соединение с SQLite закрыто")

delta_time = datetime.datetime.now() - start_time
print(f"Время{delta_time}")
