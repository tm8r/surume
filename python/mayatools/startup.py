# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

from mayatools.check_layout import CheckLayoutWindow
from mayatools.convert_color_code import ConvertColorCode


def initialize_plugin():
    cmds.setParent("MayaWindow")
    cmds.menu("tm8r_mayatools", l=u"MayaTools", to=True)
    cmds.menuItem(l=u"Check Layout",
                  c=CheckLayoutWindow.main)
    cmds.menuItem(l=u"Convert Color Code",
                  c=ConvertColorCode.show_ui)
    cmds.setParent("..")
