import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlDatabase  # главный класс подключения к базам данных
import settings as st
# логгинг отевчает за журналирование
# добавляем это для мониторинга ошибок которые не описываются
import logging
LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)

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
            LOG.info(f'Connected to database{st.db_params["dbname"]}')
        else:
            LOG.error('Connection FAILED')

    @property
    def login(self):
        return self.__login
    
    @property
    def role(self):
        return self.__role
    
    def set_authorized(self, login, role):
        self.__login = login
        self.__role = role

