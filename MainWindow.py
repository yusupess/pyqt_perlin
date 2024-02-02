from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot
from MainMenu import MainMenu
import Teacher, Student, StGroup
from Login import LoginPassword

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)
 
        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)
        main_menu.teacher_mode_request.connect(self.teacher_mode_on)
        main_menu.student_mode_request.connect(self.student_mode_on)
        main_menu.stgroup_mode_request.connect(self.stgroup_mode_on)

        allowed_flag = False
        dia = LoginPassword(self)
        if dia.exec():
            print("check login and password")
        if not allowed_flag:
            main_menu.lock()

    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = ('Программа для управления задачами\n' + 
                'и заданиями для учащихся школы')
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')

    @pyqtSlot()
    def teacher_mode_on(self):
        # сначала надо убрать старое окно
        # это как раз и есть то окно которое было раньше
        old = self.centralWidget()
        # теперь новое окно создаем
        v = Teacher.View(parent=self)
        self.setCentralWidget(v)
        # menu Bar выдает ссылку на главное меню
        self.menuBar().set_mode_teacher(v)
        # удаляем старое окно если оно было
        if old is not None:
            # deleteLater удаляет само окно после того
            # когда сигналы все выполнит
            old.deleteLater()

    @pyqtSlot()
    def student_mode_on(self):
        old = self.centralWidget()
        v = Student.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_student(v)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def stgroup_mode_on(self):
        old = self.centralWidget()
        v = StGroup.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_stgroup(v)
        if old is not None:
            old.deleteLater()
    
    

    


