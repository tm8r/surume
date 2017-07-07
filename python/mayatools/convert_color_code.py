# -*- coding: utf-8 -*-
u"""カラーコードからMayaのUI用の色情報形式に変換する"""
from __future__ import absolute_import, division, print_function

from mayatools.utility.ui_utility import safe_delete_window

from maya import cmds


class ConvertColorCode(object):
    u"""カラーコードからMayaのUI用の色情報形式に変換する"""
    _WINDOW_NAME = "mayatools_utility_convert_color_code_window"
    _COLOR_FORMAT = "[{0}, {1}, {2}]"

    def __init__(self):
        u"""initialize."""
        self.color_code_field = None
        self.decimal_point_field = None
        self.result_field = None
        self.color_preview = None

    @staticmethod
    def show_ui(*args):
        u"""Windowを表示"""
        ConvertColorCode()._create_ui()

    def _create_ui(self):
        u"""UIを生成"""
        safe_delete_window(self._WINDOW_NAME)
        win = cmds.window(self._WINDOW_NAME, t="Convert Color Code", mb=True, w=480, h=128)
        cmds.menu(l="Option")
        cmds.menuItem(l="ColorEditor", c=self.get_color_from_editor)
        cmds.columnLayout(adj=True, rs=2)
        self.color_code_field = cmds.textFieldButtonGrp(l="Color code", bl="Convert", bc=self._convert)
        self.decimal_point_field = cmds.intFieldGrp(l="Decimal point", nf=1, v1=2)
        self.result_field = cmds.textFieldGrp(l="Result")

        cmds.setParent("..")

        cmds.columnLayout(adj=True)
        self.color_preview = cmds.text(l="", h=24)
        cmds.setParent("..")
        cmds.showWindow(win)

    def _convert(self, *args):
        u"""カラーコードを変換"""
        code = cmds.textFieldButtonGrp(self.color_code_field, q=True, tx=True)
        if len(code) == 7 and code.startswith("#"):
            code = code[1:]
        if len(code) != 6:
            return
        try:
            int(code, 16)
        except ValueError, e:
            print(e)
            return
        decimal_point = cmds.intFieldGrp(self.decimal_point_field, q=True, v1=True)
        r = round(int(code[0:2], 16) / 255, decimal_point)
        g = round(int(code[2:4], 16) / 255, decimal_point)
        b = round(int(code[4:6], 16) / 255, decimal_point)
        bgc = self._COLOR_FORMAT.format(str(r), str(g), str(b))
        cmds.textFieldGrp(self.result_field, e=True, tx=bgc)
        cmds.text(self.color_preview, e=True, bgc=[r, g, b])

    def get_color_from_editor(self, *args):
        u"""colorEditorから色を得る"""
        res = cmds.colorEditor()
        if "1" != res.split()[3]:
            return
        result = cmds.colorEditor(query=True, rgb=True)
        decimal_point = cmds.intFieldGrp(self.decimal_point_field, q=True, v1=True)
        r = round(result[0], decimal_point)
        g = round(result[1], decimal_point)
        b = round(result[2], decimal_point)
        bgc = self._COLOR_FORMAT.format(str(r), str(g), str(b))
        cmds.textFieldGrp(self.result_field, e=True, tx=bgc)
        cmds.text(self.color_preview, e=True, bgc=[r, g, b])
