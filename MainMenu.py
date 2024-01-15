"""Зджесь мы создаем строку меню в нашем окне."""

from PyQt6.QtWidgets import QMenuBar

class MainMenu(QMenuBar):

    def __init__(self, parent):
        super().__init__(parent)

        help_menu = self.addMenu('Справка')

        self.__about = help_menu.addAction('О программе...')
        self.about_qt = help_menu.addAction('О библиотеке Qt...')
    
    @property
    def about(self):
        return self.__about