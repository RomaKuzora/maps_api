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
spn = 0.005


# 0.001 min
# 75 max


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def get_image_map(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={lat},{lon}&spn={spn},{spn}&l=map"
        response = requests.get(map_request)
        self.map_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(Image.open(BytesIO(response.content)))))

    def keyPressEvent(self, event):
        global spn
        if event.key() == Qt.Key.Key_PageUp and spn > 0.001:
            if spn <= 1:
                spn -= 0.001
            else:
                spn -= 1
        if event.key() == Qt.Key.Key_PageDown and spn < 75:
            if spn <= 1:
                spn += 0.001
            else:
                spn += 1
        self.get_image_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
