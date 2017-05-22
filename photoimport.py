from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyicloud import *

from index import *


class iCloud(QWidget):

    def __init__(self, parent=None):
        super(iCloud, self).__init__(parent)

    def photoImport(albums):
        photo_layout = QVBoxLayout()
        album_names = list(albums.keys())
        for name in album_names:
            album_title = QLabel(name)
            photo_layout.addWidget(album_title)


