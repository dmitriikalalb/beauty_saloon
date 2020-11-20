from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *

from utils import styleSheet, config


class AddEditWindow(QWidget):
    def __init__(self):
        super().__init__()
        # / Тип окна(редактирование или добавление)
        self.type_of_window = QLabel()
        # / Необходимые поля
        self.title = QLineEdit()
        self.cost = QLineEdit()
        self.description = QTextEdit()
        self.manufacturer = QComboBox()
        self.is_active = QCheckBox('Товар активен')
        # / Window
        self.setWindowIcon(QIcon('images/beauty_logo.ico'))
        self.setMinimumSize(1100, 840)
        self.setWindowTitle('Салон красоты')

        self.initUi()

    def initUi(self):
        # ? Контейнер с товарами
        main_layout = QVBoxLayout()
        # ? Контейнер где слева будут поля для ввода а справа фотография
        gbox = QHBoxLayout()

        # / Интерфейс (Появиться позже)

        # ? Стиль надписи сверху с типом окна
        self.type_of_window.setFixedHeight(50)
        self.type_of_window.setFont(QFont('Tahoma', 13, QFont.Bold))
        self.type_of_window.setAlignment(QtCore.Qt.AlignHCenter)

        # ? Добавление виджетов на форму
        main_layout.addWidget(self.type_of_window)
        main_layout.addLayout(gbox)
        self.setLayout(main_layout)

    def displayInfo(self):
        self.show()
