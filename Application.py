import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlDatabase  # главный класс подключения к базам данных
import settings as st


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.__login = None
        self.__role = None

        db = QSqlDatabase.addDatabase('QPSQL') # QPSQL это если посгрессу
        db.setHostName(st.db_params['host'])
        db.setDatabaseName(st.db_params['dbname'])
        db.setPort(st.db_params['port'])
        db.setUserName(st.db_params['user'])
        db.setPassword(st.db_params['password'])
        ok = db.open()
        if ok:
            print('Connected to database', file=sys.stderr)
        else:
            print('Connection FAILED', file=sys.stderr)

    @property
    def login(self):
        return self.__login
    
    @property
    def role(self):
        return self.__role
    
    def set_authorized(self, login, role):
        self.__login = login
        self.__role = role

