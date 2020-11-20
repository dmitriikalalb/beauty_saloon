from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from ui.ui_card import ElementCard
from utils import config, styleSheet


class TovarWindow(QWidget):
    def __init__(self, parent=None):
        super(TovarWindow, self).__init__(parent)
        # / Menu
        self.action_desc = QAction()
        self.action_asc = QAction()
        self.action_clear_filter = QAction()
        self.menu_filter = QMenu()
        self.menu_cost = QMenu(self.menu_filter)
        self.menu_manufacturers = QMenu(self.menu_filter)
        # / Scroll area
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea = QScrollArea()
        # / Card grid layout
        self.card_layout = QGridLayout(self.scrollAreaWidgetContents)
        # / Bottom label
        self.tovar_count = QLabel()
        # / Search & Filter area
        self.find_area = QLineEdit()
        self.find_area.textChanged.connect(self.onTextChanged)
        self.tool_button = QToolButton()
        # / Window
        self.setWindowIcon(QIcon('images/beauty_logo.ico'))
        self.setMinimumSize(1100, 840)
        self.setWindowTitle('Салон красоты')

        self.initUi()

    def initUi(self):
        # ? Контейнер с товарами
        vbox = QVBoxLayout()
        gbox = QHBoxLayout()
        self.scrollArea.setWidgetResizable(True)
        self.card_layout.setContentsMargins(2, 2, 2, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setStyleSheet('border: none;')

        # ? Создать товары
        self.create_tovar('SELECT Title, Cost, IsActive, MainImagePath FROM Product')

        # ? Стиль поля поиска
        self.find_area.setFixedHeight(50)
        self.find_area.setFont(QFont('Tahoma', 13, QFont.Normal))
        self.find_area.setPlaceholderText('Поиск...')
        self.find_area.setStyleSheet(styleSheet.TEXT_EDIT)

        # ? Стиль надписи с кол-вом товаров внизу окна
        self.tovar_count.setFont(QFont('Tahoma', 9, QFont.Normal))

        # ? Стиль кнопки фильтра
        # * Вкладка "по возрастанию"
        self.action_asc.setText('По возрастанию')
        self.action_asc.setCheckable(True)
        self.action_asc.triggered.connect(self.orderByAsc)
        # * Вкладка "по убыванию"
        self.action_desc.setText('По убыванию')
        self.action_desc.setCheckable(True)
        self.action_desc.triggered.connect(self.orderByDesc)
        # * Вкладка "Сортировать цену"
        self.menu_cost.setTitle('Сортировать цену...')
        self.menu_cost.addAction(self.action_desc)
        self.menu_cost.addAction(self.action_asc)
        # * Вкладка "Производители"
        self.menu_manufacturers.setTitle('Производители')
        manufacturers = config.execute_query('SELECT ManufacturerID FROM Product GROUP BY ManufacturerID')
        for manufacturer in manufacturers:
            self.menu_manufacturers.addAction(str(manufacturer[0]))
        self.menu_manufacturers.triggered.connect(self.orderByManufacturer)
        # * Вкладка "Очистить фильтры"
        self.action_clear_filter.setText('Очистить фильтры')
        self.action_clear_filter.triggered.connect(self.clear_filter)

        self.menu_filter.addAction(self.menu_cost.menuAction())
        self.menu_filter.addAction(self.menu_manufacturers.menuAction())
        self.menu_filter.addSeparator()
        self.menu_filter.addAction(self.action_clear_filter)

        self.tool_button.setIcon(QIcon('images/filter.png'))
        self.tool_button.setFixedSize(50, 50)
        self.tool_button.setStyleSheet('border: none; background: #c0dcf3')
        self.tool_button.setPopupMode(True)
        self.tool_button.setMenu(self.menu_filter)

        # ? Добавление виджетов на форму
        gbox.addWidget(self.find_area)
        gbox.addWidget(self.tool_button)
        vbox.addLayout(gbox)
        vbox.addWidget(self.scrollArea)
        vbox.addWidget(self.tovar_count)
        self.setLayout(vbox)

    def create_tovar(self, query):
        column = 0
        row = 0
        # ? Получаем все товары из БД
        data = config.execute_query(query)

        # ? Виджеты товаров
        for tovar in data:

            # ? Разметка GridLayout
            if column >= 4:
                column = 0
                row += 1
            # ? Достаем все изображения связанные с этим товаром
            images = config.execute_query(f'SELECT PhotoPath FROM ProductPhoto WHERE ProductID = \'{tovar[0]}\'')
            # * Тут будем хранить наши фотографии
            mass = []
            # * Разделяем название папки и самого изображения, чтобы в массив поместилось только название изображения
            main_photo = tovar[3].split('\\')
            # * Добавляем фотки
            for img in images:
                i = img[0].split('\\')
                # * Если фото совпадает с главным фото, помещаем ее в началае массива, чтобы на карточке она была первой
                if i[1] == main_photo[1]:
                    mass.insert(0, i[1])
                else:
                    mass.append(i[1])
            # * Если у товара нет больше чем 1 фотографии то просто в массив добавляем главное фото(MainImagePath)
            if not mass:
                mass.append(main_photo[1])
            # ! Вставляю карточку в грид
            card = ElementCard(tovar[0], tovar[1], tovar[2], mass)
            self.card_layout.addWidget(card, row, column)
            column += 1

        # ? Кол-во товаров
        self.tovar_count.setText(f'Количество товаров: {self.card_layout.count()} из {len(data)}')

    def orderByDesc(self):
        self.clear_layout()
        self.action_asc.setChecked(False)
        question = self.find_area.text()
        query = 'SELECT Title, Cost, IsActive, MainImagePath FROM Product '
        # ? Если поле поиска заполнено
        if question:
            self.create_tovar(query + f'WHERE Title LIKE \'%{question}%\''
                                      f' OR Description LIKE \'%{question}%\' ORDER BY Cost DESC')
        # ? Если поле поиска не заполнено
        else:
            self.create_tovar(query + 'ORDER BY Cost DESC')

    def orderByAsc(self):
        self.clear_layout()
        self.action_desc.setChecked(False)
        question = self.find_area.text()
        query = 'SELECT Title, Cost, IsActive, MainImagePath FROM Product '
        # ? Если поле поиска заполнено
        if question:
            self.create_tovar(query + f'WHERE Title LIKE \'%{question}%\''
                                      f' OR Description LIKE \'%{question}%\' ORDER BY Cost ASC')
        # ? Если поле поиска не заполнено
        else:
            self.create_tovar(query + 'ORDER BY Cost ASC')

    def clear_filter(self):
        self.clear_layout()
        self.action_desc.setChecked(False)
        self.action_asc.setChecked(False)
        self.create_tovar('SELECT Title, Cost, IsActive, MainImagePath FROM Product')

    @pyqtSlot(QAction)
    def orderByManufacturer(self, action):
        question = self.find_area.text()
        query = 'SELECT Title, Cost, IsActive, MainImagePath FROM Product'
        if question:
            query = query + f'WHERE Title LIKE \'%{question}%\' OR Description LIKE \'%{question}%\'' \
                            f' AND ManufacturerID = \'{action.text()}\''
        else:
            query = query + f' WHERE ManufacturerID = \'{action.text()}\''
        if self.action_asc.isChecked():
            query = query + ' ORDER BY Cost ASC'
        elif self.action_desc.isChecked():
            query = query + ' ORDER BY Cost DESC'

        self.clear_layout()
        self.create_tovar(query)

    def onTextChanged(self):
        self.clear_layout()
        question = self.find_area.text()
        # ? Если строка поиска пустая то после if нет смысла выполнять код
        if not question:
            return self.create_tovar('SELECT Title, Cost, IsActive, MainImagePath FROM Product ')
        self.create_tovar(f'SELECT Title, Cost, IsActive, MainImagePath FROM Product WHERE Title'
                          f' LIKE \'%{question}%\' OR Description LIKE \'%{question}%\'')

    def clear_layout(self):
        elements = self.card_layout.count()
        for i in range(elements - 1, -1, -1):
            layoutItem = self.card_layout.itemAt(i)
            w = layoutItem.widget()
            if w:
                self.card_layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
