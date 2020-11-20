from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *

from utils import styleSheet, config


class AddEditWindow(QWidget):
    def __init__(self):
        super().__init__()
        # / Card grid layout
        self.card_layout = QHBoxLayout()
        # / Bottom label
        self.tovar_count = QLabel()
        # / Search & Filter area
        self.find_area = QLineEdit()
        # / Window
        self.setWindowIcon(QIcon('images/beauty_logo.ico'))
        self.setMinimumSize(1100, 840)
        self.setWindowTitle('Салон красоты')

        self.initUi()

    def initUi(self):
        # ? Контейнер с товарами
        vbox = QVBoxLayout()
        gbox = QHBoxLayout()
        self.card_layout.setContentsMargins(2, 2, 2, 2)

        # ? Создать товары
        # self.create_tovar('SELECT Title, Cost, IsActive, MainImagePath FROM Product')

        # ? Стиль поля поиска
        self.find_area.setFixedHeight(50)
        self.find_area.setFont(QFont('Tahoma', 13, QFont.Normal))
        self.find_area.setPlaceholderText('Поиск...')
        self.find_area.setStyleSheet(styleSheet.TEXT_EDIT)

        # ? Стиль надписи с кол-вом товаров внизу окна
        self.tovar_count.setFont(QFont('Tahoma', 9, QFont.Normal))

        # ? Добавление виджетов на форму
        gbox.addWidget(self.find_area)
        vbox.addLayout(gbox)
        vbox.addLayout(self.card_layout)
        vbox.addWidget(self.tovar_count)
        self.setLayout(vbox)

    def displayInfo(self):
        self.show()
