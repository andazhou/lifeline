from PyQt5.QtWidgets import *


def errorMessage(msgText):
    error = QMessageBox()
    error.setText(msgText)
    error.exec_()


