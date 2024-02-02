import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from map_design import Ui_MainWindow
import requests
from PIL import Image, ImageQt
from io import BytesIO

lat = 37  # широта
lon = 48  # долгота
spn = 0.005


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={lat},{lon}&spn={spn},{spn}&l=map"
        response = requests.get(map_request)
        self.map_label.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(Image.open(BytesIO(response.content)))))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
