from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSlot
import psycopg2
import settings as st
import db


SELECT_ALL = """select st.pk,
                       st.f_fio,
                       st.f_comment
                from student_group as sg 
                inner join v_student as st
                on st.pk = sg.id_student
                where id_group = %s;
             """



class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__students = []
        self.refill(id_group=None)
        self.__id_group = None

    @property
    def id_group(self):
        return self.__id_group

    def rowCount(self, parent_index) -> int:
        if parent_index.isValid():
            return 0
        return len(self.__students)
    
    def columnCount(self, parent_index) -> int:
        return 0 if parent_index.isValid() else 2
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            r = index.row()
            c = index.column()
            if c==0:
                return self.__students[r].fio
            elif c==1:
                return self.__students[r].comment
            else:
                return f'{r=}, {c=}'
        else:
            return None
    
    @pyqtSlot(int)
    def refill(self, id_group=None):
        self.beginResetModel()
        self.__id_group = id_group
        try:
            self.__students = []
            if id_group is None:
                return
            conn = psycopg2.connect(**st.db_params)
            try:
                with conn:
                    with conn.cursor() as cursor:
                        cursor.execute(SELECT_ALL, (id_group,))
                        for pk, fio, comment in cursor:
                            # data = (pk, fio, comment)
                            data = db.Student(pk=pk, fio=fio, comment=comment)
                            self.__students.append(data) 
            finally:
                conn.close()
        finally:
            self.endResetModel()

    def add_students(self, new_students):
        self.beginResetModel()
        try:
            for id_student, fname in new_students:
                data = db.Student(pk=id_student, fio=fname)
                self.__students.insert(0, data)
        finally:
            self.endResetModel()
        
