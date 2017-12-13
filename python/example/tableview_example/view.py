# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from surume.vendor.Qt import QtCompat, QtCore, QtGui, QtWidgets
from example.tableview_example.constant import ICON_DIR
from example.tableview_example.model import FileTableModel
from example.tableview_example.swatch_display_delegate import SwatchDisplayPortDelegate

import maya.cmds as cmds

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin


class MenuButton(QtWidgets.QPushButton):
    u"""メニューのボタン"""

    def __init__(self, icon_name, stacked_layout, index, parent=None):
        u"""initialize

        :param icon_name: アイコンの名前
        :type icon_name: str
        :param stacked_layout: Qt
        :type stacked_layout: QtWidgets.QStackedLayout
        :param index: インデックス
        :type index: int
        :param parent: 親のWidget
        :type parent: QtWidgets.QtWidget
        """
        super(MenuButton, self).__init__(parent=parent)
        self.index = index
        self.setCheckable(True)
        self.setChecked(False)
        self.setFixedWidth(50)
        self.setFixedHeight(50)
        pix_map = QtGui.QPixmap(os.path.join(ICON_DIR, "menu_{0}.png".format(icon_name)))
        icon = QtGui.QIcon(pix_map)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(30, 30))
        self.stacked_layout = stacked_layout
        self.setStyleSheet("""
        MenuButton {background-color:#666;}
        MenuButton:checked {background-color:#4f4f4f;}
        """)
        self.checkStateSet()

    # override
    def mouseReleaseEvent(self, event):
        super(MenuButton, self).mouseReleaseEvent(event)
        if not self.isChecked() or not self.stacked_layout:
            return
        self.set_active()

    def set_active(self):
        u"""ボタンを選択状態にし、StackedLayoutのindexを切り替える"""
        self.setChecked(True)
        self.stacked_layout.setCurrentIndex(self.index)


class QHLine(QtWidgets.QFrame):
    u"""水平線表示要のWidget"""

    def __init__(self):
        u"""initialize"""
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class TableViewExampleWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    u"""TableViewExampleWindow"""

    _UI_WINDOW_NAME = "TableViewExampleWindow"

    _UI_ID = "surume_example_TableViewExampleWindow"

    def __init__(self, parent=None):
        u"""initialize

        :param parent: 親のウィンドウ
        :type parent: QtWidgets.QWidget
        """
        super(TableViewExampleWindow, self).__init__(parent=parent)
        self.setWindowTitle(self._UI_WINDOW_NAME)
        self.setObjectName(self._UI_ID)
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet("QFrame#header {background-color:#222}")
        self.table_view = QtWidgets.QTableView()
        self.model = FileTableModel(self)

        # 検索、ソート用のプロキシモデル
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.proxy_model)

    @staticmethod
    def show_ui(*args):
        u"""UIを表示"""
        win = TableViewExampleWindow()
        win._create_ui()

    def _create_ui(self, *args):
        u"""UIを生成"""

        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu("Edit")
        refresh_action = QtWidgets.QAction("Refresh", self)
        refresh_action.triggered.connect(self._refresh)
        edit_menu.addAction(refresh_action)

        root_widget = QtWidgets.QFrame(self)
        root_layout = QtWidgets.QGridLayout(root_widget)
        root_widget.setLayout(root_layout)
        root_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QtWidgets.QFrame(self)
        header_widget.setObjectName("header")
        header_widget.setMinimumHeight(60)

        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(12, 6, 6, 6)
        title_image = QtWidgets.QLabel()
        title_pix = QtGui.QPixmap(os.path.join(ICON_DIR, "logo.png"))
        title_image.setPixmap(title_pix)
        title_image.setScaledContents(True)
        title_image.setFixedSize(30, 30)
        header_layout.addWidget(title_image)

        title_label = QtWidgets.QLabel("TableView Example")
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        root_layout.addWidget(header_widget, 0, 0, 1, 1)

        content_layout = QtWidgets.QHBoxLayout(self)
        content_layout.setContentsMargins(6, 6, 6, 6)

        self.content_stacked_layout = QtWidgets.QStackedLayout(self)

        # QStackedLayoutを切り替えるメニューを生成
        content_layout.addWidget(self._create_menu_ui())

        root_layout.addLayout(content_layout, 1, 0, 1, 1)

        # QStackedLayoutにホームとファイルノードリストのWidgetを追加
        self.content_stacked_layout.addWidget(self._create_home_ui())
        self.content_stacked_layout.addWidget(self._create_file_nodes_ui())

        content_layout.addLayout(self.content_stacked_layout)

        self.setCentralWidget(root_widget)
        self.resize(1020, 600)
        self.show()

    def _create_menu_ui(self):
        u"""メニューのWidgetを生成して返す

        :return: メニューのWidget
        :rtype: QtWidget
        """
        menu_group = QtWidgets.QButtonGroup(self)

        menu_widget = QtWidgets.QFrame(self)
        menu_layout = QtWidgets.QVBoxLayout(menu_widget)

        info_button = MenuButton("home", self.content_stacked_layout, 0)
        menu_layout.addWidget(info_button)
        menu_group.addButton(info_button)
        info_button.set_active()

        nodes_button = MenuButton("filer", self.content_stacked_layout, 1)
        menu_layout.addWidget(nodes_button)
        menu_group.addButton(nodes_button)

        menu_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        return menu_widget

    def _create_home_ui(self):
        u"""ホームのWidgetを生成して返す

        :return: メニューのWidget
        :rtype: QtWidget
        """
        info_widget = QtWidgets.QFrame(self)
        info_layout = QtWidgets.QVBoxLayout(info_widget)
        info_label = QtWidgets.QLabel("Home")
        title_font = QtGui.QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        info_label.setFont(title_font)
        info_layout.addWidget(info_label)
        info_layout.addWidget(QHLine())
        info_layout.addWidget(QtWidgets.QLabel(u"簡単なTableViewのサンプルです。"))

        info_layout.addItem(
            QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        return info_widget
        self.content_stacked_layout.addWidget(info_widget)

    def _create_file_nodes_ui(self):
        u"""ファイルノードリストのWidgetを生成して返す

        :return: ファイルノードリストのWidget
        :rtype: QtWidget
        """
        file_nodes_root = QtWidgets.QFrame(self)
        file_nodes_layout = QtWidgets.QVBoxLayout(file_nodes_root)

        search_layout = QtWidgets.QHBoxLayout(self)
        search_label = QtWidgets.QLabel("Search")
        search_layout.addWidget(search_label)
        self.search_text = QtWidgets.QLineEdit(self)
        self.search_text.textChanged.connect(self._change_filter)
        search_layout.addWidget(self.search_text)
        file_nodes_layout.addLayout(search_layout)

        self.table_view.clicked.connect(self._select_file_node)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_view.setItemDelegateForColumn(0,
                                                 SwatchDisplayPortDelegate(self.table_view, self.model.items,
                                                                           self.proxy_model))

        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()
        self.table_view.verticalHeader().setDefaultSectionSize(64)

        file_nodes_layout.addWidget(self.table_view)
        return file_nodes_root

    def _refresh(self, *args):
        u"""viewをリフレッシュ"""
        self.table_view.clearSelection()
        self.table_view.clearFocus()
        self.model.refresh(refresh_items=True)
        self.table_view.setItemDelegateForColumn(0,
                                                 SwatchDisplayPortDelegate(self.table_view, self.model.items,
                                                                           self.proxy_model))
        # visibleの切替を行うことでカラムのサイズの意図しない変更を回避
        self.table_view.setVisible(False)
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()
        self.table_view.verticalHeader().setDefaultSectionSize(64)
        self.table_view.setVisible(True)

    def _change_filter(self, *args):
        u"""検索フィルターの変更"""
        reg_exp = QtCore.QRegExp(self.search_text.text(),
                                 QtCore.Qt.CaseSensitive,
                                 QtCore.QRegExp.RegExp)
        self.proxy_model.setFilterKeyColumn(2)
        self.proxy_model.setFilterRegExp(reg_exp)

    def _select_file_node(self, index):
        u"""indexをもとに対象のファイルノードを選択

        :param index: TableViewで選択されたindex
        :type index: QModelIndex
        """
        index = self.proxy_model.mapToSource(index)
        if not index.isValid():
            return
        model = self.model.items[index.row()]
        cmds.select(model.node)


TableViewExampleWindow.show_ui()
