from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot
from MainMenu import MainMenu
import Teacher, Student, StGroup

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)
        
        v = StGroup.View(parent=self)
        self.setCentralWidget(v)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)

        # main_menu.teacher_add.triggered.connect(v.add)
        # main_menu.teacher_delete.triggered.connect(v.delete)
        # main_menu.teacher_edit.triggered.connect(v.update)

        # main_menu.student_add.triggered.connect(v.add)
        # main_menu.student_delete.triggered.connect(v.delete)
        # main_menu.student_edit.triggered.connect(v.update)

        main_menu.set_mode_stgroup(v)

    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = ('Программа для управления задачами\n' + 
                'и заданиями для учащихся школы')
        QMessageBox.about(self, title, text)
        

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')

    

    


