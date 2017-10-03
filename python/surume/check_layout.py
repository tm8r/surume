# -*- coding: utf-8 -*-
u"""レイアウトに対して背景色を指定し、各レイアウトの範囲を可視化する"""
from __future__ import absolute_import, division, print_function

import random

import maya.cmds as cmds

# maya自体のレイアウトの階層数
_NATIVE_WINDOW_LENGTH = 2
_COLOR_BASE = 0.7
_RANDOM_MIN = 0
_RANDOM_MAX = 0.2


def _check_layout(root_name):
    u"""指定した名前を含むレイアウトに対して背景色を指定し、各レイアウトの範囲を可視化する"""
    layouts = cmds.lsUI(cl=True, long=True)
    targets = [x for x in layouts if root_name in x]
    if not targets:
        return
    max_nested = 0
    for x in targets:
        tmp = len(x.split("|"))
        if max_nested < tmp:
            max_nested = tmp
    max_nested -= _NATIVE_WINDOW_LENGTH

    one = _COLOR_BASE / max_nested
    for target in targets:
        nested = len(target.split("|")) - _NATIVE_WINDOW_LENGTH
        r1 = random.uniform(_RANDOM_MIN, _RANDOM_MAX)
        r2 = random.uniform(_RANDOM_MIN, _RANDOM_MAX)
        r3 = random.uniform(_RANDOM_MIN, _RANDOM_MAX)
        bgc_tmp = 1 - one * (max_nested - nested)
        bgc = (bgc_tmp - r1, bgc_tmp - r2, bgc_tmp - r3)

        cmds.layout(target, e=True, bgc=bgc)


class CheckLayoutWindow(object):
    u"""レイアウトチェックウィンドウ"""

    _WINDOW_TITLE = "CheckLayout"
    _WINDOW_NAME = "surume_check_layout_window"
    _EXCLUDE_WINDOWS = ["scriptEditorPanel", "MayaWindow", "nexFloatWindow", "outlinerPanel", "graphEditor",
                        "clipEditorPanel", "namespaceEditor", "hyperGraphPanel", "connectWindow"]
    _MARGIN = 8

    @staticmethod
    def main(*args):
        u"""起動メソッド"""
        win = CheckLayoutWindow()
        win.show_ui()
        return win

    def __init__(self):
        u"""initialize"""
        self.window = None
        self.text_field = None
        self.text_scroll = None

    def show_ui(self):
        u"""Windowを生成"""
        if cmds.window(self._WINDOW_NAME, exists=True):
            cmds.deleteUI(self._WINDOW_NAME)

        self.window = cmds.window(self._WINDOW_NAME,
                                  t=self._WINDOW_TITLE,
                                  width=340,
                                  maximizeButton=False, minimizeButton=False)

        form = cmds.formLayout()
        field_group = cmds.columnLayout(adj=True, cal="center", rs=self._MARGIN)
        cmds.text(u"""レイアウトに背景色を適用して、レイアウトの範囲を確認できます。
確認するウィンドウの名前を入力、または選択してください。""", al="left")
        self.text_scroll = cmds.textScrollList(append=self.get_windows(), ams=False, dcc=self.check_execute)
        self.text_field = cmds.textFieldGrp(l=u"直接入力", ad2=2, cl2=["left", "left"], cw=[1, 60])
        cmds.setParent("..")

        button_group = cmds.columnLayout(adj=True, cal="center")
        cmds.button(l="Check", c=self.check_execute)
        cmds.setParent("..")

        cmds.formLayout(form, e=True,
                        attachForm=[(field_group, "top", self._MARGIN),
                                    (field_group, "left", self._MARGIN),
                                    (field_group, "right", self._MARGIN),
                                    (button_group, "bottom", self._MARGIN),
                                    (button_group, "left", self._MARGIN),
                                    (button_group, "right", self._MARGIN)],
                        attachControl=[(button_group, "top", self._MARGIN, field_group)])
        cmds.setParent("..")

        cmds.showWindow(self.window)

    def check_execute(self, *args):
        u"""チェックを実行"""
        inputted = cmds.textFieldGrp(self.text_field, q=True, tx=True)
        selected = cmds.textScrollList(self.text_scroll, q=True, si=True)
        if not inputted and not selected:
            return

        # テキストフィールドへの入力を優先
        if inputted:
            target = inputted
        else:
            target = selected[0]
        _check_layout(target)

    def get_windows(self):
        u"""Maya標準のものを除くウィンドウのリストを返す"""
        windows = cmds.lsUI(windows=True)
        return [x for x in windows if not any(y for y in self._EXCLUDE_WINDOWS if x.startswith(y))]
