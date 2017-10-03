# -*- coding: utf-8 -*-
u"""UI関連ユーティリティモジュール"""
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds


def safe_delete_window(win, *args):
    u"""既に存在するウィンドウを削除する"""
    if cmds.window(win, q=True, ex=True):
        cmds.deleteUI(win)
