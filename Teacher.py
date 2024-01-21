from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2

# команда для вставки новой строчки в базу данных
INSERT = """insert into teacher ( f_fio, f_phone, f_email, f_comment )
         values ( %s, %s, %s, %s ) ;         
"""


class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        sql = """select id, f_fio, f_phone, f_email,
                 f_comment from teacher;"""
        self.setQuery(sql)

    def add(self, fio, phone, email, comment):
        conn = psycopg2.connect(host=st.db_params['host'],
                                port=st.db_params['port'],
                                dbname=st.db_params['dbname'],
                                user=st.db_params['user'],
                                password=st.db_params['password'],
                                )
        # строчку выше можно записать следующим образом
        # так как поля в сеттингс и ключи совпадают по написанию
        # conn = psycopg2.connect(**st.db_params)
        # вспомогательный обект курсор которй непосредственно отправляет
        # команду в базу данных  и получает оттуда ответ
        cursor = conn.cursor()
        data = (fio, phone, email, comment)
        cursor.execute(INSERT, data)
        # чтобы сохранить данные в БД вызываем коммит
        conn.commit()
        self.obnovit()


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
    
    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio, dia.phone, dia.email, dia.comment)

    @pyqtSlot()
    def update(self):
        QMessageBox.information(self, 'Учитель', 'Редактирование')

    @pyqtSlot()
    def delete(self):
        QMessageBox.information(self, 'Учитель', 'Удаление')


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        fio_lbl = QLabel('Фамилия И. О.', parent=self)
        self.__fio_edt = QLineEdit(parent=self)

        phone_lbl = QLabel('Телефон', parent=self)
        self.__phone_edt = QLineEdit(parent=self)

        email_lbl = QLabel('e-mail', parent=self)
        self.__email_edt = QLineEdit(parent=self)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.addWidget(fio_lbl)
        lay.addWidget(self.__fio_edt)
        lay.addWidget(phone_lbl)
        lay.addWidget(self.__phone_edt)
        lay.addWidget(email_lbl)
        lay.addWidget(self.__email_edt)
        lay.addWidget(comment_lbl)
        lay.addWidget(self.__comment_edt)
        
        # горизонтальный слой для кнопок "ОК" и "Отмена"
        lay2 = QHBoxLayout()
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
    
    @property
    def phone(self):
        result = self.__phone_edt.text().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @property
    def comment(self):
        # toPlainText() выполняет ту же функцию что и text()
        result = self.__comment_edt.toPlainText().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @property
    def email(self):
        result = self.__email_edt.text().strip()
        if result:
            return result










