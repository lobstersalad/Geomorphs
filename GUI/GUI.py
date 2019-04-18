# Sources: http://zetcode.com/gui/pyqt5
#          https://riverbankcomputing.com/static/Docs/PyQt5
#          https://pythonprogramminglanguage.com/pyqt5-button/

'''
ToDo
 - Tiling / transparency floor options
 - Floor tileset / single image options with image previews
 - Progress bars
 - Test downloader on eduroam
'''

import sys
sys.path.append('../Texturing/')

from downloader import download
from texturer import texture
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QFileDialog
from PyQt5.QtWidgets import QGridLayout, QComboBox, QPushButton, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        window = QWidget(self)
        self.setCentralWidget(window)
        grid = QGridLayout(window)

        dungeon_name_label = QLabel("Dungeon Name")
        self.dungeon_name_box = QtWidgets.QLineEdit()
        grid.addWidget(dungeon_name_label, 0, 0)
        grid.addWidget(self.dungeon_name_box, 0, 1)

        random_seed_label = QLabel("Random Seed")
        self.random_seed_box = QtWidgets.QLineEdit()
        grid.addWidget(random_seed_label, 1, 0)
        grid.addWidget(self.random_seed_box, 1, 1)

        dungeon_layout_label = QLabel("Dungeon Layout")
        self.dungeon_layout_dd = QtWidgets.QComboBox()
        options = ["Square", "Rectangle", "Box", "Cross", "Dagger",
                   "Saltire", "Keep", "Hexagon", "Round", "Cavernous"]
        self.dungeon_layout_dd.addItems(options)
        grid.addWidget(dungeon_layout_label, 2, 0)
        grid.addWidget(self.dungeon_layout_dd, 2, 1)

        dungeon_size_label = QLabel("Dungeon Size")
        self.dungeon_size_dd = QtWidgets.QComboBox()
        options = ["Fine", "Diminiutive", "Tiny", "Small", "Medium", "Large",
                   "Huge", "Gargantuan", "Colossal"]
        # dungeon_size_dd.addItem("Custom") would need to open new dimension text boxes
        self.dungeon_size_dd.addItems(options)
        grid.addWidget(dungeon_size_label, 3, 0)
        grid.addWidget(self.dungeon_size_dd, 3, 1)

        peripheral_egress_label = QLabel("Peripheral Egress")
        self.peripheral_egress_dd = QtWidgets.QComboBox()
        options = ["No", "Yes", "Tiling"]
        self.peripheral_egress_dd.addItems(options)
        grid.addWidget(peripheral_egress_label, 4, 0)
        grid.addWidget(self.peripheral_egress_dd, 4, 1)

        add_stairs_label = QLabel("Stairs")
        self.add_stairs_dd = QtWidgets.QComboBox()
        options = ["No", "Yes", "Many"]
        self.add_stairs_dd.addItems(options)
        grid.addWidget(add_stairs_label, 5, 0)
        grid.addWidget(self.add_stairs_dd, 5, 1)

        room_layout_label = QLabel("Room Layout")
        self.room_layout_dd = QtWidgets.QComboBox()
        options = ["Sparse", "Scattered", "Dense", "Symmetric", "Complex"]
        self.room_layout_dd.addItems(options)
        grid.addWidget(room_layout_label, 6, 0)
        grid.addWidget(self.room_layout_dd, 6, 1)

        room_size_label = QLabel("Room Size")
        self.room_size_dd = QtWidgets.QComboBox()
        options = ["Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"]
        self.room_size_dd.addItems(options)
        grid.addWidget(room_size_label, 7, 0)
        grid.addWidget(self.room_size_dd, 7, 1)

        door_set_label = QLabel("Doors")
        self.door_set_dd = QtWidgets.QComboBox()
        options = ["None", "Basic", "Secure", "Standard", "Deathtrap"]
        self.door_set_dd.addItems(options)
        grid.addWidget(door_set_label, 8, 0)
        grid.addWidget(self.door_set_dd, 8, 1)

        corridor_layout_label = QLabel("Corridors")
        self.corridor_layout_dd = QtWidgets.QComboBox()
        options = ["Labyrinth", "Errant", "Straight"]
        self.corridor_layout_dd.addItems(options)
        grid.addWidget(corridor_layout_label, 9, 0)
        grid.addWidget(self.corridor_layout_dd, 9, 1)

        remove_deadends_label = QLabel("Remove Deadends")
        self.remove_deadends_dd = QtWidgets.QComboBox()
        options = ["None", "Some", "All"]
        self.remove_deadends_dd.addItems(options)
        grid.addWidget(remove_deadends_label, 10, 0)
        grid.addWidget(self.remove_deadends_dd, 10, 1)

        tiled_floors_label = QLabel("Tiled Floors")
        self.tiled_floors_dd = QtWidgets.QComboBox()
        options = ["Yes", "No"]
        self.tiled_floors_dd.addItems(options)
        grid.addWidget(tiled_floors_label, 11, 0)
        grid.addWidget(self.tiled_floors_dd,  11, 1)

        download_label = QLabel("Download Path")
        self.download_path = QLineEdit()
        download_browse_button = QPushButton("Browse")
        download_browse_button.clicked.connect(self.set_download_path)
        download_button = QPushButton("Download")
        download_button.clicked.connect(self.download_button_action)
        grid.addWidget(download_label, 12, 0)
        grid.addWidget(self.download_path, 12, 1)
        grid.addWidget(download_browse_button, 12, 2)
        grid.addWidget(download_button, 12, 3)

        texture_label = QLabel("Texture Path")
        self.texture_path = QLineEdit()
        texture_browse_button = QPushButton("Browse")
        texture_browse_button.clicked.connect(self.set_texture_path)
        texture_button = QPushButton("Texture")
        texture_button.clicked.connect(self.texture_button_action)
        grid.addWidget(texture_label, 13, 0)
        grid.addWidget(self.texture_path, 13, 1)
        grid.addWidget(texture_browse_button, 13, 2)
        grid.addWidget(texture_button, 13, 3)

    def set_download_path(self):
        options = QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        path = QFileDialog.getExistingDirectory(self, "Download Path", "", options = options)
        self.download_path.setText(path)

    def download_button_action(self):
        download(self.download_path.text(),
                 self.dungeon_name_box.text(),
                 self.random_seed_box.text(),
                 self.dungeon_layout_dd.currentText(),
                 self.dungeon_size_dd.currentText(),
                 self.peripheral_egress_dd.currentText(),
                 self.add_stairs_dd.currentText(),
                 self.room_layout_dd.currentText(),
                 self.room_size_dd.currentText(),
                 self.door_set_dd.currentText(),
                 self.corridor_layout_dd.currentText(),
                 self.remove_deadends_dd.currentText())

    def set_texture_path(self):
        options = QFileDialog.DontUseNativeDialog
        path, filter = QFileDialog.getOpenFileName(self, "Texture Path", "", "PNG (*.PNG *.png);; JPEG (*.JPEG *.jpeg *.JPG *.jpg)", options = options)
        self.texture_path.setText(path)

    def texture_button_action(self):
        if self.tiled_floors_dd.currentText() == "Yes":
            texture(self.texture_path.text(), True)
        else:
            texture(self.texture_path.text(), False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
