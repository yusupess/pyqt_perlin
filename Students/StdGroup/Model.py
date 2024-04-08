from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSlot
import psycopg2
import settings as st
import db


# SELECT_ALL = """
#                 select st.pk,
#                        st.f_fio,
#                        st.f_comment
#                 from student_group as sg 
#                 inner join stgroup as gp
#                 on gp.id = sg.id_group
#                 where id_student = %s;
            #  """
SELECT_ALL = """
                select gp.id as pk,
                       gp.f_title,
                       gp.f_comment
                from student_group as sg 
                inner join stgroup as gp
                on gp.id = sg.id_group
                where id_student = %s;
             """

class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__groups = []
        self.refill(id_student=None)

    def rowCount(self, parent_index):
        if parent_index.isValid():
            return 0
        return len(self.__groups)

    def columnCount(self, parent_index):
        return 0 if parent_index.isValid() else 2
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            r = index.row()
            c = index.column()
            if c==0:
                return self.__groups[r][1]
            elif c==1:
                return self.__groups[r][2]
            else:
                return f'{r=}, {c=}'
        else:
            return None
        
    @pyqtSlot(int)
    def refill(self, id_student=None):
        self.beginResetModel()
        try:
            self.__groups = []
            if id_student is None:
                return
            conn = psycopg2.connect(**st.db_params)
            try:
                with conn:
                    with conn.cursor() as cursor:
                        cursor.execute(SELECT_ALL, (id_student,))
                        for id, title, comment in cursor:
                            data = (id, title, comment)
                            self.__groups.append(data)
            finally:
                conn.close()
        finally:
            self.endResetModel()