# Sources: http://zetcode.com/gui/pyqt5
#          https://riverbankcomputing.com/static/Docs/PyQt5

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QComboBox, QPushButton

app = QApplication([])
window = QWidget()
grid = QGridLayout()

dungeon_layout_label = QLabel("Dungeon Layout")
dungeon_layout_dd = QtWidgets.QComboBox()
options = ["Layout", "Square", "Rectangle", "Box", "Cross", "Dagger", "Saltire", "Keep", "Hexagon", "Round", "Cavernous"]
dungeon_layout_dd.addItems(options)
grid.addWidget(dungeon_layout_label, 1, 0)
grid.addWidget(dungeon_layout_dd, 1, 1)

dungeon_size_label = QLabel("Dungeon Size")
dungeon_size_dd = QtWidgets.QComboBox()
options = ["Fine", "Diminiutive", "Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"]
# dungeon_size_dd.addItem("Custom") needs to open new dimension text boxes
dungeon_size_dd.addItems(options)
grid.addWidget(dungeon_size_label, 2, 0)
grid.addWidget(dungeon_size_dd, 2, 1)

peripheral_egress_label = QLabel("Peripheral Egress")
peripheral_egress_dd = QtWidgets.QComboBox()
options = ["No", "Yes", "Tiling"]
peripheral_egress_dd.addItems(options)
grid.addWidget(peripheral_egress_label, 3, 0)
grid.addWidget(peripheral_egress_dd, 3, 1)

add_stairs_label = QLabel("Stairs")
add_stairs_dd = QtWidgets.QComboBox()
options = ["No", "Yes", "Many"]
add_stairs_dd.addItems(options)
grid.addWidget(add_stairs_label, 4, 0)
grid.addWidget(add_stairs_dd, 4, 1)

room_layout_label = QLabel("Room Layout")
room_layout_dd = QtWidgets.QComboBox()
options = ["Sparse", "Scattered", "Dense", "Symmetric", "Complex"]
room_layout_dd.addItems(options)
grid.addWidget(room_layout_label, 5, 0)
grid.addWidget(room_layout_dd, 5, 1)

room_size_label = QLabel("Room Size")
room_size_dd = QtWidgets.QComboBox()
options = ["Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"]
room_size_dd.addItems(options)
grid.addWidget(room_size_label, 6, 0)
grid.addWidget(room_size_dd, 6, 1)

door_set_label = QLabel("Doors")
door_set_dd = QtWidgets.QComboBox()
options = ["None", "Basic", "Secure", "Standard", "Deathtrap"]
door_set_dd.addItems(options)
grid.addWidget(door_set_label, 7, 0)
grid.addWidget(door_set_dd, 7, 1)

corridor_layout_label = QLabel("Corridors")
corridor_layout_dd = QtWidgets.QComboBox()
options = ["Labyrinth", "Errant", "Straight"]
corridor_layout_dd.addItems(options)
grid.addWidget(corridor_layout_label, 8, 0)
grid.addWidget(corridor_layout_dd, 8, 1)

remove_deadends_label = QLabel("Remove Deadends")
remove_deadends_dd = QtWidgets.QComboBox()
options = ["None", "Some", "All"]
remove_deadends_dd.addItems(options)
grid.addWidget(remove_deadends_label, 9, 0)
grid.addWidget(remove_deadends_dd, 9, 1)

construct = QPushButton("Construct")
construct.clicked.connect()

window.setLayout(grid)
window.show()

app.exec_()
