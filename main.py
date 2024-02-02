import sys

from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow
from map_design import Ui_MainWindow
import requests
from PyQt6.QtCore import Qt
from PIL import Image
from io import BytesIO


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.type_map = 'map'
        self.lon = 39.558881  # широта
        self.lat = 50.199912  # долгота
        self.z = 16
        self.get_image_map()
        for radio_button in self.map_group.buttons():
            radio_button.toggled.connect(self.set_map)

    def set_map(self):
        sender = self.sender().text()
        if sender == 'карта':
            self.type_map = 'map'
        elif sender == 'гибрид':
            self.type_map = 'sat,skl'
        elif sender == 'спутник':
            self.type_map = 'sat'
        self.get_image_map()

    def get_image_map(self):
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&l={self.type_map}&z={self.z}"
        response = requests.get(map_request)
        image = Image.open(BytesIO(response.content))
        image.save('image.png')
        image = QImage('image.png')
        pixmap = QPixmap(image)
        self.map_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.z < 19:
            self.z += 1
        if event.key() == Qt.Key.Key_PageDown and self.z > 0:
            self.z -= 1
        if self.z != 0:
            if event.key() == Qt.Key.Key_Left:
                self.lat -= 2 / (self.z ** 2)
            if event.key() == Qt.Key.Key_Right:
                self.lat += 2 / (self.z ** 2)
            if event.key() == Qt.Key.Key_Up:
                self.lon += 2 / (self.z ** 2)
            if event.key() == Qt.Key.Key_Down:
                self.lon -= 2 / (self.z ** 2)
        self.get_image_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
