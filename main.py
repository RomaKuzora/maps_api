import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from map_design import Ui_MainWindow
import requests
from PyQt6.QtCore import Qt
from PIL import Image, ImageQt
from io import BytesIO

lat = 39.558881  # широта
lon = 50.199912  # долгота
z = 19
x = None


# 0.001 min
# 75 max


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.get_image_map()

    def get_image_map(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={lat},{lon}&z={z}&l=map"
        response = requests.get(map_request)
        self.map_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(Image.open(BytesIO(response.content)))))

    def keyPressEvent(self, event):
        global z, lat, lon
        if event.key() == Qt.Key.Key_PageUp and z < 19:
            z += 1
        if event.key() == Qt.Key.Key_PageDown and z > 0:
            z -= 1
        if event.key() == Qt.Key.Key_Left:
            lat -= 0
        if event.key() == Qt.Key.Key_Right:
            lat += 0
        if event.key() == Qt.Key.Key_Up:
            lon += 0
        if event.key() == Qt.Key.Key_Down:
            lon -= 0
        self.get_image_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
