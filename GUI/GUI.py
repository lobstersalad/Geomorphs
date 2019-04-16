# Sources: http://zetcode.com/gui/pyqt5
#          https://riverbankcomputing.com/static/Docs/PyQt5
#          https://pythonprogramminglanguage.com/pyqt5-button/

import sys
sys.path.append('../Texturing/')

from downloader import download
from texturer import texture
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QLabel, QGridLayout, QComboBox, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        window = QWidget(self)
        self.setCentralWidget(window)
        grid = QGridLayout(window)

        dungeon_layout_label = QLabel("Dungeon Layout")
        self.dungeon_layout_dd = QtWidgets.QComboBox()
        options = ["Layout", "Square", "Rectangle", "Box", "Cross", "Dagger", "Saltire", "Keep", "Hexagon", "Round", "Cavernous"]
        self.dungeon_layout_dd.addItems(options)
        grid.addWidget(dungeon_layout_label, 1, 0)
        grid.addWidget(self.dungeon_layout_dd, 1, 1)

        dungeon_size_label = QLabel("Dungeon Size")
        self.dungeon_size_dd = QtWidgets.QComboBox()
        options = ["Fine", "Diminiutive", "Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"]
        # dungeon_size_dd.addItem("Custom") would need to open new dimension text boxes
        self.dungeon_size_dd.addItems(options)
        grid.addWidget(dungeon_size_label, 2, 0)
        grid.addWidget(self.dungeon_size_dd, 2, 1)

        peripheral_egress_label = QLabel("Peripheral Egress")
        self.peripheral_egress_dd = QtWidgets.QComboBox()
        options = ["No", "Yes", "Tiling"]
        self.peripheral_egress_dd.addItems(options)
        grid.addWidget(peripheral_egress_label, 3, 0)
        grid.addWidget(self.peripheral_egress_dd, 3, 1)

        add_stairs_label = QLabel("Stairs")
        self.add_stairs_dd = QtWidgets.QComboBox()
        options = ["No", "Yes", "Many"]
        self.add_stairs_dd.addItems(options)
        grid.addWidget(add_stairs_label, 4, 0)
        grid.addWidget(self.add_stairs_dd, 4, 1)

        room_layout_label = QLabel("Room Layout")
        self.room_layout_dd = QtWidgets.QComboBox()
        options = ["Sparse", "Scattered", "Dense", "Symmetric", "Complex"]
        self.room_layout_dd.addItems(options)
        grid.addWidget(room_layout_label, 5, 0)
        grid.addWidget(self.room_layout_dd, 5, 1)

        room_size_label = QLabel("Room Size")
        self.room_size_dd = QtWidgets.QComboBox()
        options = ["Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"]
        self.room_size_dd.addItems(options)
        grid.addWidget(room_size_label, 6, 0)
        grid.addWidget(self.room_size_dd, 6, 1)

        door_set_label = QLabel("Doors")
        self.door_set_dd = QtWidgets.QComboBox()
        options = ["None", "Basic", "Secure", "Standard", "Deathtrap"]
        self.door_set_dd.addItems(options)
        grid.addWidget(door_set_label, 7, 0)
        grid.addWidget(self.door_set_dd, 7, 1)

        corridor_layout_label = QLabel("Corridors")
        self.corridor_layout_dd = QtWidgets.QComboBox()
        options = ["Labyrinth", "Errant", "Straight"]
        self.corridor_layout_dd.addItems(options)
        grid.addWidget(corridor_layout_label, 8, 0)
        grid.addWidget(self.corridor_layout_dd, 8, 1)

        remove_deadends_label = QLabel("Remove Deadends")
        self.remove_deadends_dd = QtWidgets.QComboBox()
        options = ["None", "Some", "All"]
        self.remove_deadends_dd.addItems(options)
        grid.addWidget(remove_deadends_label, 9, 0)
        grid.addWidget(self.remove_deadends_dd, 9, 1)

        construct = QPushButton("Download")
        construct.clicked.connect(self.download_button)
        grid.addWidget(construct, 10, 0)

        construct = QPushButton("Texture")
        construct.clicked.connect(texture)
        grid.addWidget(construct, 10, 1)

    def download_button(self):
        download(self.dungeon_layout_dd.currentText(),
                 self.dungeon_size_dd.currentText(),
                 self.peripheral_egress_dd.currentText(),
                 self.add_stairs_dd.currentText(),
                 self.room_layout_dd.currentText(),
                 self.room_size_dd.currentText(),
                 self.door_set_dd.currentText(),
                 self.corridor_layout_dd.currentText(),
                 self.remove_deadends_dd.currentText())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
