"""Зджесь мы создаем строку меню в нашем окне."""

from PyQt6.QtWidgets import QMenuBar

class MainMenu(QMenuBar):

    def __init__(self, parent):
        super().__init__(parent)

        teacher_menu = self.addMenu('Учитель')
        self.teacher_add = teacher_menu.addAction('Добавить')
        self.teacher_edit = teacher_menu.addAction('Редактировать')
        self.teacher_delete = teacher_menu.addAction('Удалить')

        student_menu = self.addMenu('Студент')
        self.student_add = student_menu.addAction('Добавить')
        self.student_edit = student_menu.addAction('Редактировать')
        self.student_delete = student_menu.addAction('Удалить')

        stgroup_menu = self.addMenu('Группа')
        self.stgroup_add = stgroup_menu.addAction('Добавить')
        self.stgroup_edit = stgroup_menu.addAction('Редактировать')
        self.stgroup_delete = stgroup_menu.addAction('Удалить')

        help_menu = self.addMenu('Справка')
        self.__about = help_menu.addAction('О программе...')
        self.about_qt = help_menu.addAction('О библиотеке Qt...')

    @property
    def about(self):
        return self.__about