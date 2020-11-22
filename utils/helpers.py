from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


# * Функция которая вызывает диалоговое окно
def show_popup(title, message, function):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setWindowIcon(QIcon('images/beauty_logo.ico'))
    msg.setText(title)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.No)
    msg.setInformativeText(message)

    msg.buttonClicked.connect(function)
    msg.exec_()


# ! Диалоговое окно для ошибок
def show_error_popup(detail, error_msg='По каким-то причинам произошла ошибка'):
    msg = QMessageBox()
    msg.setWindowTitle('Ошибка')
    msg.setWindowIcon(QIcon('images/beauty_logo.ico'))
    msg.setMinimumWidth(300)
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setText(error_msg + '\t\t\t\t')
    msg.setDetailedText(str(detail))

    msg.exec_()
