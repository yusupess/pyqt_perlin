from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QAbstractItemView, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2


INSERT = """insert into student ( f_fio, f_email, f_comment )
         values ( %s, %s, %s ) ;         
"""

SELECT_ONE = """select f_fio, f_email, f_comment
                from student
                where id = %s ;
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

    def add(self, fio, email, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (fio, email, comment)
        cursor.execute(INSERT, data)
        conn.commit()
        conn.close()
        self.obnovit()

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

class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        model = Model(parent=self)
        self.setModel(model)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QHeaderView.ResizeMode.Fixed) 
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio, dia.email, dia.comment)


    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        id_student = self.model().record(row).value(0)
        # подключаемся к базе данных
        conn = psycopg2.connect(**st.db_params)
        # создаем курсор
        cursor = conn.cursor()
        data = (id_student,)
        cursor.execute(SELECT_ONE, data)
        # считываем строку из базы даных и записываем в строки диалогового окна
        dia.fio, dia.email, dia.comment = cursor.fetchone()
        # после счиьываения обязательно закываем подключение к базе
        conn.close()
        if dia.exec():
            self.model().update(id_student, dia.fio,
                                dia.email, dia.comment
                                )

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_student = self.model().record(row).value(0)
        # при удалении выходит окно для подтверждения
        ans = QMessageBox.question(self, 'Ученик', 'ВЫ уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(id_student)


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Ученик')

        fio_lbl = QLabel('Фамилия И. О.', parent=self)
        self.__fio_edt = QLineEdit(parent=self)
        
        email_lbl = QLabel('e-mail', parent=self)
        self.__email_edt = QLineEdit(parent=self)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.setSpacing(15)

        lay_fam = QVBoxLayout()
        # наводим красоту. устанавливаем расстояние м\у элементами
        lay_fam.setSpacing(0)
        lay_fam.addWidget(fio_lbl)
        lay_fam.addWidget(self.__fio_edt)
        lay.addLayout(lay_fam)

        
        lay_em = QVBoxLayout()
        lay_em.setSpacing(0)
        lay_em.addWidget(email_lbl)
        lay_em.addWidget(self.__email_edt)
        lay.addLayout(lay_em)
        

        lay_com = QVBoxLayout()
        lay_com.setSpacing(0)
        lay_com.addWidget(comment_lbl)
        lay_com.addWidget(self.__comment_edt)
        lay.addLayout(lay_com)
        
        # горизонтальный слой для кнопок "ОК" и "Отмена"
        lay2 = QHBoxLayout()
        # доавляем пустое пространство чтобы кнопки ок и Отмена были в правом углу
        lay2.addStretch()
        lay2.addWidget(ok_btn)
        lay2.addWidget(cancel_btn)
        # добавляем горизонтальный слой кнопок(ОК и Отмена) в общий вертикальный слой
        lay.addLayout(lay2)
        #  подключаем кнопку "Отмена"
        cancel_btn.clicked.connect(self.reject)
        #  подключаем кнопку "Ок"
        ok_btn.clicked.connect(self.finish)

         #слот это в-ция которая реагирует на какоето событие
    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            return
        self.accept()       

    @property
    def fio(self):
        result = self.__fio_edt.text().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @fio.setter
    def fio(self, value):
        self.__fio_edt.setText(value)
    
    @property
    def comment(self):
        # toPlainText() выполняет ту же функцию что и text()
        result = self.__comment_edt.toPlainText().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @comment.setter
    def comment(self, value):
        self.__comment_edt.setPlainText(value)

    @property
    def email(self):
        result = self.__email_edt.text().strip()
        if result:
            return result
        
    @email.setter
    def email(self, value):
        self.__email_edt.setText(value)

        