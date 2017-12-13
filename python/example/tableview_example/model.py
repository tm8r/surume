# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from example.tableview_example.item import FileInfo
from surume.vendor.Qt import QtCore, QtWidgets

from maya import cmds


class FileTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        u"""initialize

        :param parent: parent
        :type parent: QtCore.QObject
        """
        super(FileTableModel, self).__init__(parent)
        self.items = []
        self.refresh()

    def refresh(self, refresh_items=True):
        u"""情報を更新

        :param refresh_items: ファイルパスのリスト
        :type refresh_items: bool
        """
        if refresh_items:
            file_nodes = cmds.ls(type="file")
            self.set_items(file_nodes)

        self.layoutAboutToBeChanged.emit()
        self.modelAboutToBeReset.emit()
        self.modelReset.emit()
        self.layoutChanged.emit()

    def set_items(self, nodes):
        u"""itemsを更新

        :param items: ファイルパスのリスト
        :type items: list of unicode
        """
        self.items = []
        for node in nodes:
            self.items.append(FileInfo(node))

    # override
    def headerData(self, col, orientation, role):
        u"""見出しを返す"""
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return FileInfo.header[col]
        return None

    # override
    def rowCount(self, parent):
        u"""行数を返す"""
        return len(self.items)

    # override
    def columnCount(self, parent):
        u"""カラム数を返す"""
        return FileInfo.row_count

    # override
    def data(self, index, role):
        u"""カラムのデータを返す"""
        if not index.isValid():
            return None

        item = self.items[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return item.columns[index.column()].value
        elif role == QtCore.Qt.TextAlignmentRole:
            return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        return None
