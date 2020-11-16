import mysql.connector

db_conn = mysql.connector.connect(
    host="mysbalab.eastus2.cloudapp.azure.com",
    user="" # RemoteDB username,
    password="" # RemoteDB password,
    database="events",
    auth_plugin="mysql_native_password",
)

db_cursor = db_conn.cursor()

db_cursor.execute(
    """
          CREATE TABLE report_service
          (id INT NOT NULL AUTO_INCREMENT, 
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
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT business_id_pk PRIMARY KEY (id))
          """
)

db_cursor.execute(
    """
          CREATE TABLE request_service
          (id INT NOT NULL AUTO_INCREMENT, 
           serviceType VARCHAR(250) NOT NULL,
           laundryType VARCHAR(250) NOT NULL,
           numberOfItems INTEGER NOT NULL,
           phoneNumber VARCHAR(15) NOT NULL,
           emailAddress VARCHAR(100) NOT NULL,
           streetNumber VARCHAR(250) NOT NULL,
           city VARCHAR(100) NOT NULL,
           province VARCHAR(100) NOT NULL,
           country VARCHAR(100) NOT NULL,
           postalCode VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT serviceType_pk PRIMARY KEY (id))
          """
)

db_conn.commit()
db_conn.close()
