import os
import shutil
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QFont, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import *
from utils import styleSheet, config, helpers


class AddEditWindow(QWidget):
    def __init__(self):
        super().__init__()
        # / Тип окна(редактирование или добавление)
        self.imagePath = ''
        self.type_of_window = QLabel()
        self.type_of_window.setObjectName('main_label')
        # / Необходимые поля и контейнеры
        self.vbox = QFormLayout()
        self.manufacturer = QComboBox()
        self.description_label = QLabel('Описание товара:')
        self.cost_label = QLabel('Стоимость товара:')
        self.title_label = QLabel('Название товара:')
        self.uuid_label = QLabel('Уникальный идентификатор (GUID):')
        self.attached = QLabel('Связанные товары:')
        self.uuid = QLineEdit()
        self.photo_name = QLabel()
        self.photo = QLabel()
        self.title = QLineEdit()
        self.cost = QLineEdit()
        self.description = QTextEdit()
        self.manufacturer = QComboBox()
        self.is_active_checkbox = QCheckBox('Товар активен')
        self.btn_ok = QPushButton('Сохранить')
        self.btn_cancel = QPushButton('Отмена')
        self.btn_change_image = QPushButton('Сменить изображение')
        self.btn_add_attached = QPushButton('Добавить связанный товар')
        self.old_title = ''
        # / Window
        self.setWindowIcon(QIcon('images/beauty_logo.ico'))
        self.setFixedSize(1100, 840)
        self.setStyleSheet(f'QLineEdit, QTextEdit, QComboBox{{{styleSheet.TEXT_EDIT}\nfont: 13pt Tahoma;}}\n'
                           f'QLabel, QCheckBox, QComboBox{{{styleSheet.LABEL}}}\n'
                           f'#main_label{{ font-weight: bold;}}'
                           f'#btn_ok{{{styleSheet.BTN_SUCCESS}}}'
                           f'#btn_cancel{{{styleSheet.BTN_WARNING}}}')
        self.initUi()

    def initUi(self):
        # ? Контейнер с товарами
        main_layout = QVBoxLayout()
        # ? Контейнер где слева будут поля для ввода а справа фотография
        gboxwidget = QWidget()
        gbox = QFormLayout(gboxwidget)
        # ? Контейнер с полями для ввода
        rightwidget = QWidget()
        rightwidget.setFixedWidth(750)
        rightvbox = QVBoxLayout(rightwidget)
        # ? Контейнер с фото
        leftwidget = QWidget()
        leftwidget.setFixedWidth(300)
        leftvbox = QVBoxLayout(leftwidget)
        scrollwidget = QWidget()
        scrollwidget.setLayout(self.vbox)
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(scrollwidget)
        self.scrollarea.setFixedHeight(300)

        # / Интерфейс
        # * Справо
        self.uuid.setPlaceholderText('Уникальный идентификатор')
        self.title.setPlaceholderText('Название товара')
        self.cost.setPlaceholderText('Стоимость товара')
        rx = QtCore.QRegExp('[0-9]+\.[0-9]{2}')
        validator = QRegExpValidator(rx)
        self.cost.setValidator(validator)
        self.description.setPlaceholderText('Описание товара')

        manufacturers = config.execute_query('SELECT Name FROM Manufacturer')
        for man in manufacturers:
            self.manufacturer.addItem(str(man[0]))

        # * Слево
        self.photo.setStyleSheet('border: 1px solid;')
        self.photo.setFixedHeight(280)
        self.photo.setScaledContents(True)
        self.photo_name.setText('Название фото.png')
        self.photo_name.setWordWrap(True)
        self.photo_name.setAlignment(QtCore.Qt.AlignHCenter)
        self.btn_change_image.setFont(QFont('Tahoma', 12, QFont.Normal))
        self.btn_change_image.setFixedHeight(40)
        self.btn_change_image.setObjectName('btn_ok')
        self.btn_change_image.clicked.connect(self.btn_img_clicked)
        self.btn_add_attached.setFont(QFont('Tahoma', 12, QFont.Normal))
        self.btn_add_attached.setFixedHeight(40)
        self.btn_add_attached.setObjectName('btn_ok')
        self.btn_add_attached.clicked.connect(self.btn_attached_clicked)

        # * Bottom
        btn_box = QHBoxLayout()
        self.btn_ok.setObjectName('btn_ok')
        self.btn_ok.setFont(QFont('Tahoma', 12, QFont.Normal))
        self.btn_ok.setFixedHeight(40)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.setObjectName('btn_cancel')
        self.btn_cancel.setFont(QFont('Tahoma', 12, QFont.Normal))
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

        # ? Стиль надписи сверху с типом окна
        self.type_of_window.setFixedHeight(60)
        self.type_of_window.setWordWrap(True)
        self.type_of_window.setAlignment(QtCore.Qt.AlignHCenter)

        # ? Добавление виджетов на форму
        btn_box.addWidget(self.btn_ok)
        btn_box.addWidget(self.btn_cancel)
        rightvbox.addWidget(self.uuid_label)
        rightvbox.addWidget(self.uuid)
        rightvbox.addWidget(self.title_label)
        rightvbox.addWidget(self.title)
        rightvbox.addWidget(self.cost_label)
        rightvbox.addWidget(self.cost)
        rightvbox.addWidget(self.description_label)
        rightvbox.addWidget(self.description)
        rightvbox.addWidget(self.manufacturer)
        rightvbox.addWidget(self.is_active_checkbox)
        rightvbox.addLayout(btn_box)
        leftvbox.addWidget(self.photo)
        leftvbox.addWidget(self.photo_name)
        leftvbox.addWidget(self.btn_change_image)
        leftvbox.addWidget(self.attached)
        leftvbox.addWidget(self.scrollarea)
        leftvbox.addWidget(self.btn_add_attached)
        gbox.addRow(leftwidget, rightwidget)

        main_layout.addWidget(self.type_of_window)
        main_layout.addWidget(gboxwidget)
        self.setLayout(main_layout)

    def displayInfo(self):
        print(self.uuid.text())
        self.show()

    def btn_ok_clicked(self):
        self.sender_msg = self.sender()
        helpers.show_popup('Подтвердите действие\t\t\t', 'Сохранить изменения?', self.popup_button)

    def btn_cancel_clicked(self):
        self.sender_msg = self.sender()
        helpers.show_popup('Подтвердите действие\t\t\t', 'Выйти без сохранения?', self.popup_button)

    def popup_button(self, i):
        msg = i.text()
        sender = self.sender_msg
        if msg == '&Yes':
            uuid = self.uuid.text()
            title = self.title.text()
            cost = float(self.cost.text()) if self.cost.text() else ''
            mainImage = f' Товары салона красоты\\{self.photo_name.text()}' \
                if self.photo_name.text() != 'Название фото.png' else ''
            isActive = int(self.is_active_checkbox.isChecked())
            manufacturer = self.manufacturer.currentText()
            desc = self.description.toPlainText()
            if sender.text() == 'Сохранить':
                try:
                    query = f"UPDATE Product SET Title='{title}', Cost={cost}, MainImagePath='{mainImage}'," \
                            f" IsActive={isActive}, ManufacturerID='{manufacturer}', Description='{desc}'" \
                            f" WHERE Title='{self.old_title}'"
                    config.update(query)
                    self.old_title = self.title.text()
                    if self.imagePath:
                        # ? Копируем изображение в нашу директорию с изображениями
                        destination = os.path.abspath('./images')
                        shutil.copy(self.imagePath, destination)
                    self.close()
                except Exception as e:
                    helpers.show_error_popup(e)
            elif sender.text() == 'Добавить':
                try:
                    query = f"INSERT INTO Product(Guid, Title, Cost, MainImagePath," \
                            f" IsActive, ManufacturerID, Description)" \
                            f" VALUES ('{uuid}','{title}',{cost},'{mainImage}',{isActive},'{manufacturer}','{desc}')"
                    config.update(query)
                    self.close()
                except Exception as e:
                    helpers.show_error_popup(e)
            elif sender.text() == 'Отмена':
                try:
                    self.close()
                except Exception as e:
                    print(e)

    def btn_img_clicked(self):
        fname = QFileDialog.getOpenFileName(self, 'Выберите изображение', 'C:/', "Image files (*.jpg *.png)")
        try:
            self.imagePath = fname[0]
            if self.imagePath:
                # ? Если картинка меньше 2мб, добавляем. Иначе выдаем ошибку
                image_size = os.path.getsize(self.imagePath) / 1024 / 1024
                if image_size <= 2:
                    image_name = str(self.imagePath).split('/')[-1]
                    pixmap = QPixmap(self.imagePath)
                    self.photo.setPixmap(pixmap)
                    self.photo_name.setText(image_name)
                else:
                    self.imagePath = ''
                    helpers.show_error_popup(f'Максимальный вес: 2мб\nВес вашего изображения: {round(image_size, 2)}мб',
                                             'Загруженное вами изображение весит больше 2мб')
        except Exception as e:
            print(e)

    def btn_attached_clicked(self):
        pass
