"""
В этом диалоге список всех студенот которые
   не входят в опрежедленную группу.
"""

from PyQt6.QtWidgets import QDialog, QTableView, QDialogButtonBox, QHeaderView
from PyQt6.QtSql import QSqlQueryModel, QSqlQuery
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QVBoxLayout
from exceptions import MyQtSqlModelError

import logging


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.ERROR)

_SELECT = '''
select st.pk, st.f_fio 
    from v_student as st
    where st.pk not in ( 
        select id_student
        from student_group
        where id_group = :IDGROUP
    );
'''

class _Model(QSqlQueryModel):

    def __init__(self, id_group, parent=None):
        super().__init__(parent)
        
        qry = QSqlQuery()
        qry.prepare(_SELECT)
        # if qry.lastError().isValid():
        #     err_text = self.lastError().text()
        #     LOG.error(err_text)
        #     raise MyQtSqlModelError(err_text)
        qry.bindValue(':IDGROUP', id_group)
        qry.exec()
        # if qry.lastError().isValid():
        #     err_text = self.lastError().text()
        #     LOG.error(err_text)
        #     raise MyQtSqlModelError(err_text)

        self.__selected_ids = set()
        self.setQuery(qry)

    
    def flags(self, index):
        """чтоб сделать возможным наличие флагов,
        но флагов после этого еще не будет видно"""
        fl = super().flags(index)
        if index.column() == 1:
            fl |= Qt.ItemFlag.ItemIsUserCheckable
        return fl
    
    def data(self, index: QModelIndex, role):
        
        """Чтоб было видно флаги"""
        # print(f'index - {index}')
        # print(f"role - {role}")
        # print(f'Qt.ItemDataRole.UserRole - {Qt.ItemDataRole.UserRole}')
        # print(f'Qt.ItemDataRole.DisplayRole - {Qt.ItemDataRole.DisplayRole}')
        # print(f'Qt.ItemDataRole.CheckStateRole - {Qt.ItemDataRole.CheckStateRole}')
        # print(index.row(), index.column())
        # print(dir(index))
        # print(f"index.parent()  - {index.parent()}")
        # id = index.data(Qt.ItemDataRole.UserRole+0)
        # print(f'id  -- {id}')
        if role == (Qt.ItemDataRole.UserRole + 0):
            print(role)
            print('pk')
            try:
                print('pk2')
                return self.query().value('pk')
            except BaseException as err:
                print(err)
                print(type(err))
        elif role == Qt.ItemDataRole.CheckStateRole:
            if index.column() ==0: #!= 1:
                return super().data(index, role)
            else:
                print('1')
                a = Qt.ItemDataRole.UserRole+0
                print(f'a  - {a}')
                id = index.data(a)
                print(f'id  -- {id}')
                if id in self.__selected_ids:
                    return Qt.CheckState.Checked
                else:
                    return Qt.CheckState.Unchecked
        else:
            return super().data(index, role)
        # if self.lastError().isValid():
        #     err_text = self.lastError().text()
        #     LOG.error(err_text)
        #     raise MyQtSqlModelError(err_text)
        # else:
        #     LOG.info("Student query OK")


class _View(QTableView):
    """_ потому чо за пределами этого диалогового окна этот
    клааа не используем."""
    def __init__(self, id_group, parent=None):
        try:
            super().__init__(parent)

            self.setModel(_Model(id_group, parent=self))

           # self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
           # self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            # self.hideColumn(0)
        #    # self.setWordWrap(False)
        #    # self.hideRow(0)
        # self.setWordWrap(False)
        # vh = self.verticalHeader()
        # vh.setSectionResizeMode(QHeaderView.ResizeMode.Fixed) 
        # hh = self.horizontalHeader()
        # hh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        except Exception as error:
            print('!!!!!!!!!!!!')
            print(error)

        


class DialogOld(QDialog):

    def __init__(self, id_group, parent=None):
        
        super().__init__(parent)

        self.setMinimumSize(300, 300)
        self.setWindowTitle('Список студентов для добавления')
        self.setStyleSheet('border: 1px solid black')

        lay = QVBoxLayout(self)

        view = _View(id_group, parent=self)
        lay.addWidget(view)
        btn = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                               | QDialogButtonBox.StandardButton.Cancel,
                               parent=self)
        lay.addWidget(btn)
        
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)
