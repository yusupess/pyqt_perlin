from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QAbstractItemView, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from exceptions import MyQtSqlModelError
import settings as st
import psycopg2

import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

SELECT_ALL = """select pk, f_fio, f_phone, f_email,
                 f_comment from v_teacher;"""

# команда для вставки новой строчки в базу данных
# INSERT = """insert into teacher ( f_fio, f_phone, f_email, f_comment )
#          values ( %s, %s, %s, %s ) ;         
# """

SELECT_ONE = """select f_fio, f_phone, f_email, f_comment
                from teacher
                where id = %s ;
            """

UPDATE = """
            update teacher set
            f_fio = %s,
            f_phone = %s,
            f_email = %s,
            f_comment = %s
            where id = %s ;
"""

DELETE = """
            delete from teacher where id = %s ;
"""

class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        self.setQuery(SELECT_ALL)
        if self.lastError().isValid():
            err_text = self.lastError().text()
            LOG.error(err_text)
            raise MyQtSqlModelError(err_text)
        else:
            LOG.info("Teacher query OK")


    # def add(self, fio, phone, email, comment):
    #     conn = psycopg2.connect(host=st.db_params['host'],
    #                             port=st.db_params['port'],
    #                             dbname=st.db_params['dbname'],
    #                             user=st.db_params['user'],
    #                             password=st.db_params['password'],
    #                             )
    #     # строчку выше можно записать следующим образом
    #     # так как поля в сеттингс и ключи совпадают по написанию
    #     # conn = psycopg2.connect(**st.db_params)
    #     # вспомогательный обект курсор которй непосредственно отправляет
    #     # команду в базу данных  и получает оттуда ответ
    #     cursor = conn.cursor()
    #     data = (fio, phone, email, comment)
    #     cursor.execute(INSERT, data)
    #     # чтобы сохранить данные в БД вызываем коммит
    #     conn.commit()
    #     conn.close()
    #     self.obnovit()

    def update(self, id_teacher, fio, phone, email, comment):
        conn = psycopg2.connect(**st.db_params)
        # вспомогательный обект курсор которй непосредственно отправляет
        # команду в базу данных  и получает оттуда ответ
        cursor = conn.cursor()
        data = (fio, phone, email, comment, id_teacher)
        cursor.execute(UPDATE, data)
        # чтобы сохранить данные в БД вызываем коммит
        conn.commit()
        conn.close()
        self.obnovit()

    def delete(self, id_teacher):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_teacher,)
        cursor.execute(DELETE, data)
        conn.commit()
        conn.close()
        self.obnovit()
