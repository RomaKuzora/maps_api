import sys
from pprint import pprint

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow
import requests
from PyQt6.QtCore import Qt
from PIL import Image
from io import BytesIO
from geocoder import get_ll_span, geocode


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.initUi()

    def initUi(self):
        self.type_map = 'map'
        self.lon = 39.558881  # широта
        self.lat = 50.199912  # долгота
        self.z = 16
        self.spn_lon = 0.005
        self.spn_lat = 0.005
        self.pt_lon = 0
        self.pt_lat = 0
        self.flag_point = False
        self.get_image_map()
        self.radio_button_map.setChecked(1)
        self.restart_button.clicked.connect(self.restart)
        for radio_button in self.map_group.buttons():
            radio_button.toggled.connect(self.set_map)
        self.find_button.clicked.connect(self.get_coord)

    def restart(self):
        self.type_map = 'map'
        self.lon = 39.558881  # широта
        self.lat = 50.199912  # долгота
        self.z = 16
        self.spn_lon = 0.005
        self.spn_lat = 0.005
        self.pt_lon = 0
        self.pt_lat = 0
        self.radio_button_map.setChecked(1)
        self.flag_point = False
        self.edit_name.setText('')
        self.get_image_map()
        self.adress_label.setText('')

    def get_coord(self):
        if self.edit_name.text():
            _object_ = get_ll_span(self.edit_name.text())
            self.spn_lon, self.spn_lat = list(map(float, _object_[1].split(',')))
            self.lon, self.lat = list(map(float, _object_[0].split(',')))
            self.pt_lon, self.pt_lat = list(map(float, _object_[0].split(',')))
            self.flag_point = True
            self.get_image_map(flag=False)
            adress = geocode(self.edit_name.text())['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
            adress = "\n".join(adress.split(', '))
            self.adress_label.setText(adress)

    def set_map(self):
        sender = self.sender().text()
        if sender == 'карта':
            self.type_map = 'map'
        elif sender == 'гибрид':
            self.type_map = 'sat,skl'
        elif sender == 'спутник':
            self.type_map = 'sat'
        self.get_image_map()

    def get_image_map(self, flag=True):
        if flag:
            if self.flag_point:
                map_request = (f"https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&"
                               f"l={self.type_map}&z={self.z}&pt={self.pt_lon},{self.pt_lat},pm2rdl")
            else:
                map_request = (f"https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&"
                               f"l={self.type_map}&z={self.z}")
        else:
            map_request = (f"https://static-maps.yandex.ru/1.x/?ll={self.lon},{self.lat}&"
                           f"l={self.type_map}&z={self.z}&spn={self.spn_lon},{self.spn_lat}&"
                           f"pt={self.lon},{self.lat},pm2rdl")
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
                self.lon -= 2 / (self.z ** 2)
            if event.key() == Qt.Key.Key_Right:
                self.lon += 2 / (self.z ** 2)
            if event.key() == Qt.Key.Key_Up:
                self.lat += 2 / (self.z ** 2)
            if event.key() == Qt.Key.Key_Down:
                self.lat -= 2 / (self.z ** 2)
        self.get_image_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
