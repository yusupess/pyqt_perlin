from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QAbstractItemView, QHeaderView
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
        conn.close()
        self.obnovit()

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



class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
        
        # чтобы выбирать всю строку, а не одну ячейку
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # чтобы убатть возможность выбора нескольких строк
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # чтобы скрыть колонку id
        self.hideColumn(0)
        # запретить перенос по пробелу хотя у меня итак не переносилось
        self.setWordWrap(False)
        # чтобы нельзя было изменять высоту строк
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QHeaderView.ResizeMode.Fixed) 
        # чтобы длина солбцов подбиралась под содержимое ячеек
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # чтобы таблица растянулась по горизонтали за счет четвертой колонки
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio, dia.phone, dia.email, dia.comment)

    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        # подключаемся к базе данных
        conn = psycopg2.connect(**st.db_params)
        # создаем курсор
        cursor = conn.cursor()
        data = (id_teacher,)
        cursor.execute(SELECT_ONE, data)
        # считываем строку из базы даных и записываем в строки диалогового окна
        dia.fio, dia.phone, dia.email, dia.comment = cursor.fetchone()
        # после счиьываения обязательно закываем подключение к базе
        conn.close()
        if dia.exec():
            self.model().update(id_teacher, dia.fio,
                                dia.phone, dia.email,
                                dia.comment
                                )

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        # при удалении выходит окно для подтверждения
        ans = QMessageBox.question(self, 'Учитель', 'ВЫ уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(id_teacher)


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Учитель')

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
        lay.setSpacing(15)

        lay_fam = QVBoxLayout()
        # наводим красоту. устанавливаем расстояние м\у элементами
        lay_fam.setSpacing(0)
        lay_fam.addWidget(fio_lbl)
        lay_fam.addWidget(self.__fio_edt)
        lay.addLayout(lay_fam)

        lay3 = QHBoxLayout()
        
        lay_phn = QVBoxLayout()
        lay_phn.setSpacing(0)
        lay_phn.addWidget(phone_lbl)
        lay_phn.addWidget(self.__phone_edt)
        lay3.addLayout(lay_phn)
        
        lay_em = QVBoxLayout()
        lay_em.setSpacing(0)
        lay_em.addWidget(email_lbl)
        lay_em.addWidget(self.__email_edt)
        lay3.addLayout(lay_em)
        
        lay.addLayout(lay3)

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
    def phone(self):
        result = self.__phone_edt.text().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
        
    @phone.setter
    def phone(self, value):
        self.__phone_edt.setText(value)
    
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










