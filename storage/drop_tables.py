import sqlite3

conn = sqlite3.connect('laundry.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE report_service
          ''')

conn.commit()
conn.close()

