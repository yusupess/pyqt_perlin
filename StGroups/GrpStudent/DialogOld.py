"""
В этом диалоге список всех студенот которые
   не входят в опрежедленную группу.
"""

from PyQt6.QtWidgets import QDialog, QTableView, QDialogButtonBox
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout


id_group = 1

_SELECT = """select st.pk, st.f_fio
             from v_student as st
             where st.pk not in (
                  select id_student
                  from student_group
                  where id_group = 1
             );
             """

class _Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setQuery(_SELECT)


class _View(QTableView):
    """_ потому чо за пределами этого диалогового окна этот
    клааа не используем."""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setModel(_Model(parent=self))
        


class DialogOld(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(300, 300)
        self.setWindowTitle('Список студентов для добавления')
        self.setStyleSheet('border: 1px solid black')

        lay = QVBoxLayout(self)

        view = _View(parent=self)
        lay.addWidget(view)
        btn = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                               | QDialogButtonBox.StandardButton.Cancel,
                               parent=self)
        lay.addWidget(btn)
        
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)

    


