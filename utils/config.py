from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

SERVER_NAME = 'DESKTOP-3KMSCN1\SQLEXPRESS'
DATABASE = 'Beauty_Salon'
USERNAME = 'Python_User'
PASSWORD = '123'


def create_connection():
    conn_string = f'DRIVER={{SQL Server}};' \
                  f'SERVER={SERVER_NAME};' \
                  f'UID={USERNAME};' \
                  f'PWD={PASSWORD};' \
                  f'DATABASE={DATABASE};'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(conn_string)

    if db.open():
        print('Успешно подключено к БД')
        return True
    else:
        print('Не удалось подключится к БД')
        return False


def display_data(query):
    print('processing query...')
    qry = QSqlQuery(db)
    qry.exec(query)

    model = QSqlQueryModel()
    model.setQuery(qry)

    return model
