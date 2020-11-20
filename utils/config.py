import pyodbc

SERVER_NAME = r'DESKTOP-3KMSCN1\SQLEXPRESS'
DATABASE = 'Beauty_Salon_User5'
USERNAME = 'Python_User'
PASSWORD = '123'

connection_string = f'DRIVER={{SQL Server}};' \
                    f'SERVER={SERVER_NAME};' \
                    f'UID={USERNAME};' \
                    f'PWD={PASSWORD};' \
                    f'DATABASE={DATABASE};' \
                    f'Trusted_connection=yes;'
connect = pyodbc.connect(connection_string)


def execute_query(query):
    cursor = connect.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
