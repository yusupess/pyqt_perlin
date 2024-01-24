"""Зджесь мы создаем строку меню в нашем окне."""

from PyQt6.QtWidgets import QMenuBar

class MainMenu(QMenuBar):

    def __init__(self, parent):
        super().__init__(parent)

        help_menu = self.addMenu('Справка')

        self.__about = help_menu.addAction('О программе...')
        self.about_qt = help_menu.addAction('О библиотеке Qt...')

        help_menu1 = self.addMenu('Учитель')
        self.teacher_add = help_menu1.addAction('Добавить')
        self.teacher_edit = help_menu1.addAction('Редактировать')
        self.teacher_delete = help_menu1.addAction('Удалить')

    @property
    def about(self):
        return self.__about