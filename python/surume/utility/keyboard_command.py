# -*- coding: utf-8 -*-
u"""コマンド入力"""
from __future__ import absolute_import, division, print_function

import time

from surume.vendor.Qt import QtGui, QtWidgets

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


class KeyboardCommandWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    _UI_WINDOW_NAME = "CommandInput"

    _UI_ID = "surume_command_input"

    _DEFAULT_SEQUENCE = [u"↑", u"↑", u"↓", u"↓", u"←", u"→", u"←", u"→", u"B", u"A"]

    def __init__(self, parent=None, command_sequence=[], callback=None):
        super(KeyboardCommandWindow, self).__init__(parent=parent)
        self.setWindowTitle(self._UI_WINDOW_NAME)
        self.setObjectName(self._UI_ID)
        self.setProperty("saveWindowPref", True)
        self.command_field = None
        self.result_label = None
        self.prev_time = time.time()
        self.reset_threshold = 2
        self.current_command = []
        self.command_sequence = command_sequence
        if not self.command_sequence:
            self.command_sequence = self._DEFAULT_SEQUENCE

        self.command_sequence_length = len(self.command_sequence)
        self.callback = callback
        self.unlocked = False
        self.button = None

    @staticmethod
    def show_ui(command_sequence=[], callback=None, *args):
        u"""UIを表示"""
        win = KeyboardCommandWindow(command_sequence=command_sequence, callback=callback)
        win._create_ui()

    def _create_ui(self):
        rootWidget = QtWidgets.QWidget(self)
        rootLayout = QtWidgets.QVBoxLayout(self)
        rootWidget.setLayout(rootLayout)

        label = QtWidgets.QLabel(u"Please enter the command.")
        rootLayout.addWidget(label)

        command_layout = QtWidgets.QVBoxLayout()
        self.command_field = QtWidgets.QLineEdit()
        self.command_field.setEnabled(False)
        command_layout.addWidget(self.command_field)

        self.button = QtWidgets.QPushButton("Locked")
        self.button.setEnabled(False)
        self.button.clicked.connect(self._button_clicked)
        command_layout.addWidget(self.button)

        rootLayout.addLayout(command_layout)
        self.setCentralWidget(rootWidget)

        self.show()

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        if self.unlocked:
            return

        pressed = QtGui.QKeySequence(event.key()).toString(QtGui.QKeySequence.NativeText)

        if self.current_command and time.time() - self.prev_time > self.reset_threshold:
            self._reset_command()
            self.current_command.append(pressed)
            self._reflect_keys(self.current_command)
            self.command_field.setStyleSheet("background-color:none")
            return

        self.current_command.append(pressed)
        self.prev_time = time.time()
        if len(self.current_command) < self.command_sequence_length:
            self._reflect_keys(self.current_command)
            return

        target_command = self.current_command[-self.command_sequence_length:]
        self._reflect_keys(target_command)
        if target_command != self.command_sequence:
            self.command_field.setStyleSheet("background-color:#ff0000")
            return

        self.command_field.setStyleSheet("background-color:#00ff00")

        self.unlocked = True
        self.button.setEnabled(True)
        self.button.setText("Unlock")

    def _button_clicked(self):
        if self.callback:
            self.callback()

        self.close()

    def _reflect_keys(self, keys):
        self.command_field.setText(",".join(keys))

    def _reset_command(self):
        self.current_command = []
        self.prev_time = time.time()
