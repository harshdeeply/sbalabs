import sqlite3

conn = sqlite3.connect('laundry.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE report_service
          (id INTEGER PRIMARY KEY ASC, 
           businessID VARCHAR(250) NOT NULL,
           serviceOffered VARCHAR(250) NOT NULL,
           openingHours VARCHAR(100) NOT NULL,
           closingHours VARCHAR(100) NOT NULL,
           phoneNumber VARCHAR(100) NOT NULL,
           streetNumber VARCHAR(250) NOT NULL,
           city VARCHAR(100) NOT NULL,
           province VARCHAR(100) NOT NULL,
           country VARCHAR(100) NOT NULL,
           postalCode VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE request_service
          (id INTEGER PRIMARY KEY ASC, 
           serviceType VARCHAR(250) NOT NULL,
           laundryType VARCHAR(250) NOT NULL,
           numberOfItems INTEGER NOT NULL,
           phoneNumber VARCHAR(15) NOT NULL,
           emailAddress VARCHAR(15) NOT NULL,
           streetNumber VARCHAR(250) NOT NULL,
           city VARCHAR(100) NOT NULL,
           province VARCHAR(100) NOT NULL,
           country VARCHAR(100) NOT NULL,
           postalCode VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()

