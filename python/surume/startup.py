# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

from surume.check_layout import CheckLayoutWindow
from surume.convert_color_code import ConvertColorCode


def initialize_plugin():
    cmds.setParent("MayaWindow")
    cmds.menu("surume", l=u"surume", to=True)
    cmds.menuItem(l=u"Check Layout",
                  c=CheckLayoutWindow.main)
    cmds.menuItem(l=u"Convert Color Code",
                  c=ConvertColorCode.show_ui)
    cmds.setParent("..")
