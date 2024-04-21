from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtSql import QSqlQueryModel
import settings as st
import psycopg2
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

INSERT = """insert into stgroup ( f_title, f_comment )
         values ( %s, %s ) ;         
"""

SELECT_ONE = """select f_title, f_comment
                from stgroup
                where id = %s ;
            """

UPDATE = """
            update stgroup set
            f_title = %s,
            f_comment = %s
            where id = %s ;
"""

DELETE = """
            delete from stgroup where id = %s ;
"""

class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        sql = """select id, f_title, f_comment
                 from stgroup;"""
        self.setQuery(sql)

    def add(self, title, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (title, comment)
        cursor.execute(INSERT, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def update(self, id_stgroup, title, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (title, comment, id_stgroup)
        cursor.execute(UPDATE, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def delete(self, id_stgroup):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_stgroup,)
        cursor.execute(DELETE, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def data(self, index: QModelIndex, role):
        # отвеяает за предоставление даты модели

        # если роль зарезервирована то менять мы ничего не будем
        if role != Qt.ItemDataRole.UserRole + 0:
            return super().data(index, role)
        r = index.row()
        rec = self.record(r)
        return rec.value(0)
