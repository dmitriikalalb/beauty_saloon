from PyQt5.QtWidgets import QMessageBox


# * Функция которая вызывает диалоговое окно
def show_popup(title, message, function):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(title)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.No)
    msg.setInformativeText(message)

    msg.buttonClicked.connect(function)
    msg.exec_()
