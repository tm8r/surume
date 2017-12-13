# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from surume.vendor.Qt import QtCompat, QtCore, QtWidgets

from maya import cmds
import maya.OpenMayaUI as om


class SwatchDisplayPortDelegate(QtWidgets.QItemDelegate):
    u"""swatchDisplayPortを表示するDelegateクラス"""

    def __init__(self, parent, items, proxy_model):
        super(SwatchDisplayPortDelegate, self).__init__(parent)
        self.items = items
        self.proxy_model = proxy_model

    # override
    def paint(self, painter, option, index):
        item = self.items[self.proxy_model.mapToSource(index).row()]
        if not self.parent().indexWidget(index) and item.node:
            self.parent().setIndexWidget(
                index,
                _create_swatch_display_port_widget(item.node, self.parent())
            )

    # override
    def sizeHint(self, option, index):
        return QtCore.QSize(64, 64)


def _create_swatch_display_port_widget(file_node, parent):
    u"""swatchDisplayPortをQWidgetでラップしたオブジェクトを返す"""
    # swatchDisplayPortにはレイアウトが必要なので、一時的にwindowを作成して削除する
    tmp = cmds.window()
    cmds.columnLayout()
    sw = cmds.swatchDisplayPort(h=64, w=64, sn=file_node)
    ptr = om.MQtUtil.findControl(sw)
    sw_widget = QtCompat.wrapInstance(long(ptr), QtWidgets.QWidget)
    sw_widget.setParent(parent)
    sw_widget.resize(64, 64)
    cmds.deleteUI(tmp)
    return sw_widget
