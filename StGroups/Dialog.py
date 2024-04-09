from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSlot


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Группа')

        title_lbl = QLabel('Название группы', parent=self)
        self.__title_edt = QLineEdit(parent=self)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.setSpacing(15)

        lay_fam = QVBoxLayout()
        # наводим красоту. устанавливаем расстояние м\у элементами
        lay_fam.setSpacing(0)
        lay_fam.addWidget(title_lbl)
        lay_fam.addWidget(self.__title_edt)
        lay.addLayout(lay_fam)        

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
        if self.title is None:
            return
        self.accept()       

    @property
    def title(self):
        result = self.__title_edt.text().strip()
        if result:
            return result
    
    @title.setter
    def title(self, value):
        self.__title_edt.setText(value)
    
    @property
    def comment(self):
        result = self.__comment_edt.toPlainText().strip()
        if result:
            return result
    
    @comment.setter
    def comment(self, value):
        self.__comment_edt.setPlainText(value)

        