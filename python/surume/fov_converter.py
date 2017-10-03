# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import math

from surume.utility.ui_utility import safe_delete_window

import maya.cmds as cmds


class FovConverter(object):
    _WINDOW_NAME = "surume_fov_converter_window"
    _MARGIN = 8

    def __init__(self):
        self.text_scroll = None
        self.text_field = None

    @staticmethod
    def show_ui():
        win = FovConverter()
        win._create_ui()

    def _create_ui(self):
        safe_delete_window(self._WINDOW_NAME)

        win = cmds.window(self._WINDOW_NAME)

        form = cmds.formLayout()
        field_group = cmds.columnLayout(adj=True, cal="center", rs=self._MARGIN)
        cmds.text(u"指定したカメラのfocalLengthを入力したUnityのFOVをもとに算出、適用します。", al="left")
        self.text_scroll = cmds.textScrollList(append=self._get_cameras(), ams=False, dcc=self._select)
        self.text_field = cmds.textFieldGrp(l=u"FOV", ad2=2, cl2=["left", "left"], cw=[1, 60])
        self.result_field = cmds.textFieldGrp(l=u"Result", ad2=2, cl2=["left", "left"], cw=[1, 60])
        cmds.setParent("..")

        button_group = cmds.columnLayout(adj=True, cal="center")
        cmds.button(l="Apply", c=self._apply)
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

        cmds.showWindow(win)

    def _select(self, *args):
        selected = cmds.textScrollList(self.text_scroll, q=True, si=True)
        if not selected:
            return
        camera = selected[0]
        cmds.select(camera)

    @staticmethod
    def _get_cameras():
        return cmds.ls(type="camera")

    def _apply(self, *args):
        selected = cmds.textScrollList(self.text_scroll, q=True, si=True)
        fov = cmds.textFieldGrp(self.text_field, q=True, tx=True)
        if not selected or not fov:
            return
        camera = selected[0]
        vfa = cmds.getAttr(camera + ".verticalFilmAperture")

        focal_length = 0.5 * vfa / math.tan(float(fov) / 2.0 / 57.29578) / 0.03937

        cmds.setAttr(camera + ".focalLength", focal_length)
        cmds.textFieldGrp(self.result_field, e=True, tx=round(focal_length, 3))
