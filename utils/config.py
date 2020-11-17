import pymssql as s

SERVER_NAME = r'DESKTOP-3KMSCN1\SQLEXPRESS'
DATABASE = 'Beauty_Salon_User5'
USERNAME = 'Python_User'
PASSWORD = '123'

def create_connection():
    connection_string = s.connect(server=SERVER_NAME, database=DATABASE, user=USERNAME, password=PASSWORD)
    cursor = connection_string.cursor()
    cursor.execute('SELECT * FROM Manufacturer')
    string = cursor.fetchone()

    while string:
        print(string)

    connection_string.close()
