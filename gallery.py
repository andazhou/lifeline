import sys

from photoimport import QImageButton

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Scale of entire app. 1: 360 X 270, 2: 720 X 540, 4: 1440 X 1080
scale = 3


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Lifeline: Tell Your Story'
        self.left = 100  # offset from monitor
        self.top = 100  # offset from monitor
        self.width = scale * 360
        self.height = scale * 270
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.addImageButton(40 * scale, -10 * scale, 40 * scale, 'annotate.png')
        self.show()


    def onImageClick(self):
        print('Image Clicked')


    #Given the coordinates and color, draw a rectangle
    def addRectangle(self, painter, left, top, width, height, red, green, blue):
        #Set the color, pen and brush
        color = QColor(red, green, blue)
        painter.setPen(color)
        painter.setBrush(color)
        #draw and end
        painter.drawRect(left, top, width, height)


    def paintEvent(self, event):
        #Make the painter and begin
        qp = QPainter()
        qp.begin(self)
        #Make the rectangles
        border1 = 21 * scale
        border2 = 54 * scale
        self.addRectangle(qp, 0, 0, self.width, border1 , 0, 0, 0)
        self.addRectangle(qp, 0, border1 , self.width, border2, 7, 187, 170)
        #Make the top-left text box
        border0 = 12 * scale
        formattedPoint = QPoint(border0, border0)
        formattedString = "Library"
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont("Lato-Bold"))
        qp.drawText(formattedPoint, formattedString)
        qp.end()

    def addImageButton(self, left, top, size, path):
        image = QPushButton(self)
        image.setGeometry(left, top, size, size)

        image.clicked.connect(self.onImageClick)




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    start = App()
    start.show()

    sys.exit(app.exec_())