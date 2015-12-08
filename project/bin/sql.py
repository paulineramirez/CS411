import MySQLdb

users = {
        'user': 'mysql_user',
        'password': 'mysql_password',
        'host': '127.0.0.1',
        'database': 'riskitbiscuit'
        }
TABLES = {}

TABLES['startups'] = (
        "CREATE TABLE startups ("
        " startup_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        " startup_url varchar(255) NOT NULL,"
        " startup_twitter varchar(255) NOT NULL,"
        " startup_money INT NOT NULL,"
        " startup_name varchar(255) NOT NULL,"
        " contact_name varchar(255) NOT NULL,"
        " contact_email varchar(255) NOT NULL,"
        " contact_phone varchar(255) NOT NULL,"
        " startup_category varchar(4095) NOT NULL,"
        " startup_stage INT NOT NULL," 
        " startup_description varchar(4095) NOT NULL)"
        
        )

add_startupInfo = ("INSERT INTO startups "
            "(startup_name, startup_money, contact_name, contact_email, contact_phone, startup_stage, startup_url, startup_twitter, startup_description) "
            "VALUES (%(startup_name)s, %(startup_money)s, %(contact_name)s, %(contact_email)s, %(contact_phone)s, %(startup_stage)s, %(startup_url)s, %(startup_twitter)s, %(startup_description)s)")


global cnx
def DBConnect(config):
    global cnx
    try:
         cnx = MySQLdb.connect(host='127.0.0.1',user='mysql_user',passwd='mysql_password')
    except MySQLdb.Error,e:
        print "MYsql error: [%d]: %s" % (e.args[0], e.args[1])
def DBCreate(dbname):
    global cnx
    cursor = cnx.cursor()
    try:
        cursor.execute("Create database " + dbname)
        cursor.close()
    except MySQLdb.Error,e:
        print "error in creating db"
        print "MYsql error: [%d]: %s" % (e.args[0], e.args[1])
    else:
        print("ok")
def DBclose():
    global cnx
    cnx.close()


def DBCreateTable():
    cursor= cnx.cursor()
    cursor.execute("USE riskitbiscuit")
    for table in TABLES.iteritems():
        try:
            tablename,query = table
            print("Creating a table {}: " + query)
            cursor.execute(query)


        except MySQLdb.Error,e:
            print ("MYsql error:",e )
        else:
            print("OK")
    cursor.close()
'''
JUNK CODE
def DBInsert(table, data):
    cursor = cnx.cursor()
    cursor.execute(table, data)

    try:
        cursor.execute(table, data)
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
'''
