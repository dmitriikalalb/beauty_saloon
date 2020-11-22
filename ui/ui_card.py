from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QPainter, QPen
from PyQt5 import QtCore
from ui.ui_add_edit import AddEditWindow
from utils import helpers, config


class ElementCard(QWidget):
    def __init__(self, title, cost, is_active, images):
        super().__init__()
        self.addEditWindow = AddEditWindow()
        self.imagenumber = 0
        self.title = title
        self.cost = cost
        self.is_active_d = is_active
        self.imagelist = images
        self.initUI()
        self.label.setMouseTracking(True)
        self.frame_color = QtCore.Qt.darkGray
        self.setMinimumHeight(400)
        self.setMaximumSize(250, 400)

    def initUI(self):

        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.rb_group = QButtonGroup()
        for img in range(0, len(self.imagelist)):
            radio = QRadioButton()
            self.rb_group.addButton(radio)
            self.rb_group.setId(radio, img)
            hbox.addWidget(radio)
        self.rb_group.button(0).setChecked(True)

        # self.radio0 = QRadioButton()
        # self.radio1 = QRadioButton()
        # self.radio2 = QRadioButton()
        # self.radio3 = QRadioButton()
        #
        # self.radio0.setChecked(True)
        #
        # self.rb_group.addButton(self.radio0)
        # self.rb_group.addButton(self.radio1)
        # self.rb_group.addButton(self.radio2)
        # self.rb_group.addButton(self.radio3)
        #
        # self.rb_group.setId(self.radio0, 0)
        # self.rb_group.setId(self.radio1, 1)
        # self.rb_group.setId(self.radio2, 2)
        # self.rb_group.setId(self.radio3, 3)
        #
        # hbox.addWidget(self.radio0)
        # hbox.addWidget(self.radio1)
        # hbox.addWidget(self.radio2)
        # hbox.addWidget(self.radio3)

        self.rb_group.buttonClicked.connect(self.rbPressEvent)

        self.name = QLabel(self.title)
        # * Обрезаем текст если он слишком длинный чтобы разметка карточки не ломалась
        txt = ''
        for text in self.title.split()[:4]:
            txt = txt + text
        if len(txt) >= 25:
            self.name.setText(self.title[:25] + '...')
            self.name.setToolTip(self.title)
        self.price = QLabel(str(int(self.cost)) + ' руб.')
        self.is_active = QLabel('Неактивен' if not self.is_active_d else '')

        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)
        self.price.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)
        self.is_active.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)

        self.name.setFont(QFont('Tahoma', 13, QFont.Normal))
        self.price.setFont(QFont('Tahoma', 15, QFont.Normal))

        self.setLayout(layout)
        self.label = QLabel()
        self.label.setText('Изображение отсутствует')
        self.label.setMouseTracking(True)
        layout.addWidget(self.label)
        layout.addLayout(hbox)
        layout.addWidget(self.name)
        layout.addWidget(self.price)
        layout.addWidget(self.is_active)

        self.resize(200, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showimage(0)

    def showimage(self, imagenumber):
        directory = "images/"
        pixmap = QPixmap(directory + self.imagelist[imagenumber])

        self.label.setPixmap(pixmap)
        self.label.setFixedHeight(220)
        self.label.setScaledContents(True)

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        step = self.label.width() / len(self.imagelist)
        width_step = 0
        res = {}
        counter = 0
        while counter < len(self.imagelist):
            width_step += step
            res.update({counter: width_step})
            counter += 1
            for i in res.keys():
                if res[i] < x:
                    self.rb_group.button(i).setChecked(True)
            self.rbPressEvent()

    def rbPressEvent(self):
        self.showimage(self.rb_group.checkedId())

    # ? Цвет рамки заднего фона карточки

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.is_active_d:
            painter.setBrush(QtCore.Qt.white)
        else:
            painter.setBrush(QtCore.Qt.gray)
        painter.setPen(QPen(self.frame_color, 5))

        painter.drawRect(self.rect())

    # ? Контекстное меню ПКМ
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        edit_action = contextMenu.addAction('Редактировать')
        delete_action = contextMenu.addAction('Удалить')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        # * Если нажали удалить
        if action == delete_action:
            helpers.show_popup('Удалить запить?', 'Вы уверены что хотите удалить данный товар?', self.popup_button)
        # * Если нажали редактировать
        elif action == edit_action:
            # * Передаем на форму редактирования нужные параметры
            self.addEditWindow.setWindowTitle('Редактировать товар')
            self.addEditWindow.type_of_window.setText(f'Редактировать товар \n"{self.title}"')
            # ? Достаем недостающие данные(Описание товара, уникальный идентификатор и свзяанные товары)
            missing_data = config.execute_query(f'SELECT Description, Guid, IsActive, Cost, ManufacturerID FROM Product'
                                                f' WHERE Title = \'{self.title}\'')
            self.addEditWindow.uuid.setDisabled(True)
            self.addEditWindow.title.setText(self.title)
            self.addEditWindow.old_title = str(self.title)
            for miss in missing_data:
                self.addEditWindow.uuid.setText('' if not miss[1] or miss[1] is None else str(miss[1]))
                self.addEditWindow.description.setText('' if not miss[0] or miss[0] is None else str(miss[0]))
                self.addEditWindow.is_active_checkbox.setChecked(bool(miss[2]))
                self.addEditWindow.cost.setText(str(int(miss[3])))
                index = self.addEditWindow.manufacturer.findText(str(miss[4]), QtCore.Qt.MatchFixedString)
                self.addEditWindow.manufacturer.setCurrentIndex(index)
                self.addEditWindow.photo.setPixmap(QPixmap('images/' + self.imagelist[0]))
                self.addEditWindow.photo_name.setText(str(self.imagelist[0]))
            attached_products = config.execute_query(f'SELECT Title, MainImagePath, Cost FROM Product '
                                                     f'INNER JOIN AttachedProduct '
                                                     f'ON AttachedProduct.AttachedProductID=Product.Title '
                                                     f'WHERE MainProductID = \'{self.title}\'')

            for product in attached_products:
                split_image = str(product[1]).split('\\')
                image = QLabel()
                image.setPixmap(QPixmap('images/' + split_image[1]))
                image.setScaledContents(True)
                image.setFixedSize(40, 40)
                title = QLabel()
                title.setText(str(product[0]) + ' - ' + str(int(product[2])) + ' руб.')
                title.setStyleSheet('font: 8pt Tahoma;')
                title.setWordWrap(True)
                self.addEditWindow.vbox.addRow(image, title)
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                self.addEditWindow.vbox.addRow(line)
            self.addEditWindow.displayInfo()

    # ? Функция которая принимает ответ с диалогового окна
    def popup_button(self, i):
        msg = i.text()
        if msg == '&Yes':
            # ! Удаляем товар
            try:
                query = f'DELETE FROM Product WHERE Title = \'{self.title}\''
                config.delete(query)
                self.close()
            except Exception as e:
                # / Если БД по каким-то причинам не разрешила удалить, вывожу ошибку
                print(e)
                helpers.show_error_popup(e)

    # ? Смена цвета рамки при нажатии на карточку
    def mousePressEvent(self, event):
        if self.frame_color == QtCore.Qt.darkGray:
            self.frame_color = QtCore.Qt.blue
        elif self.frame_color == QtCore.Qt.blue:
            self.frame_color = QtCore.Qt.darkGray
