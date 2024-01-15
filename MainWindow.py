from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot
from MainMenu import MainMenu

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)

    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = ('Программа для управления задачами\n' + 
                'и заданиями для учащихся школы')
        QMessageBox.about(self, title, text)
        

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')

    

    


