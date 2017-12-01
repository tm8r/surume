# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from surume.vendor.Qt import QtGui, QtWidgets

from surume.utility.keyboard_command import KeyboardCommandWindow

from maya import cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


class KeyboardCommandExampleWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    _UI_WINDOW_NAME = "CreateCube"

    _UI_ID = "surume_keyboard_command_example"

    _DEFAULT_SEQUENCE = [u"↑", u"↑", u"↓", u"↓", u"←", u"→", u"←", u"→", "B", "A"]

    def __init__(self, parent=None):
        super(KeyboardCommandExampleWindow, self).__init__(parent=parent)
        self.setWindowTitle(self._UI_WINDOW_NAME)
        self.setObjectName(self._UI_ID)

    @staticmethod
    def show_ui(*args):
        u"""UIを表示"""
        win = KeyboardCommandExampleWindow()
        win._create_ui()

    def _create_ui(self):
        rootWidget = QtWidgets.QWidget(self)
        rootLayout = QtWidgets.QVBoxLayout(self)
        rootWidget.setLayout(rootLayout)

        button = QtWidgets.QPushButton("Create Cube")
        button.clicked.connect(self._create_cube_callback)
        rootLayout.addWidget(button)

        self.setCentralWidget(rootWidget)

        self.show()

    def _create_cube_callback(self):
        KeyboardCommandWindow.show_ui(callback=self._create_cube)

    def _create_cube(self):
        cmds.polyCube()
