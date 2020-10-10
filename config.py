from PyQt5.QtSql import QSqlDatabase

SERVER_NAME = ''
DATABASE = ''
USERNAME = ''
PASSWORD = ''


def create_connection():
    conn_string = f'DRIVER={{SQL DRIVER}};' \
                 f'SERVER={SERVER_NAME};' \
                 f'DATABASE={DATABASE}'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(conn_string)

    if db.open():
        print('Успешно подключено к БД')
        return True
    else:
        print('Не удалось подключится к БД')
        return False
