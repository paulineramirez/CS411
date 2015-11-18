import mysql

users = {
        'user': 'mysql_user',
        'password': 'mysql_password',
        'host': '127.0.0.1'
        'database': 'riskitbiscuit'
        }
TABLES = {}
TABLES['users'] = (
        "CREATE TABLE `users` ("
        " `user_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY"
        " `username` varchar(255) NOT NULL"
        " `password` password(255) NOT NULL"
        )
TABLES['startups'] = (
        "CREATE TABLE `startups` ("
        " `startup_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY"
        " `startup_name` varchar(255) NOT NULL"
        " `startup_money` INT NOT NULL"
        " `contact_name` varchar(255) NOT NULL"
        " `contact_email` varchar(255) NOT NULL"
        " `contact_phone` varchar(255) NOT NULL"
        " `startup_stage` INT NOT NULL"
        " `startup_url` varchar(255) NOT NULL"
        " `startup_twitter` varchar(255) NOT NULL"
        " `startup_description` varchar(4095) NOT NULL"
        )

add_startupInfo = ("INSERT INTO startups "
            "(startup_name, startup_money, contact_name, contact_email, contact_phone, startup_stage, startup_url, startup_twitter, startup_description) "
            "VALUES (%(startup_name)s, %(startup_money)s, %(contact_name)s, %(contact_email)s, %(contact_phone)s, %(startup_stage)s, %(startup_url)s, %(startup_twitter)s, %(startup_description)s)")


global cnx
def DBconnect(config):
    global cnx
    try:
         cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno = errorcode.ER_ACCESS_DENIED:
            print("Something is wrong with your username/password")
        elif err.errn= errorcode.ER_BAD_DB_ERROR:
            print("DB does not exist")
        else:
            print(err)
    else:
        cnx.close()

def DBclose():
    global cnx
    cnx.close()


def DBCreateTable():
    cursor= cnx.cursor()
    for table in TABLES.iteritems():
        try:
            print("Creating a table {}: ".format(table), end='')
            cursor.execute(table)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists")
            else:
                print(err.msg)

        else:
            print("OK")
    cursor.close()

def DBInsert(table, data):
    cursor = cnx.cursor()
    try:
        cursor.execute(table, data):
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Successfully inserted")
    cnx.commit()

def DBQuery(query, info):
    #pass in a query into the DB in the form 
    #SELECT FROM riskitbiscuit WHERE startup=$s
    #should be called when we make a get request to the startup pages in main possibly add row for # of twitter followers and then get max
    cursor = cnx.cursor()
    try:
     cursor.execute(query, info)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Successfully queried")
    cursor.close()