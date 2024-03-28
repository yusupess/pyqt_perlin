from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2

import logging
# __name__ это имя текущего модуля
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


INSERT = """insert into student ( f_fio, f_email, f_comment )
         values ( %s, %s, %s ) ;         
"""

UPDATE = """
            update student set
            f_fio = %s,
            f_email = %s,
            f_comment = %s
            where id = %s ;
"""

DELETE = """
            delete from student where id = %s ;
"""

class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        sql = """select id, f_fio, f_email,
                 f_comment from student;"""
        self.setQuery(sql)
        if self.lastError().isValid():
            err_text = self.lastError().text()
            LOG.error(err_text)
        else:
            LOG.info("Studentd qeery OK")

    # def add(self, fio, email, comment):
    #     conn = psycopg2.connect(**st.db_params)
    #     cursor = conn.cursor()
    #     data = (fio, email, comment)
    #     cursor.execute(INSERT, data)
    #     conn.commit()
    #     conn.close()
    #     self.obnovit()

    def update(self, id_student, fio, email, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (fio, email, comment, id_student)
        cursor.execute(UPDATE, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def delete(self, id_student):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_student,)
        cursor.execute(DELETE, data)
        conn.commit()
        conn.close()
        self.obnovit()
