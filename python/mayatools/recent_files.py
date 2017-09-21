# -*- coding: utf-8 -*-
u"""最近開いたファイルへのアクセス補助モジュール"""
from __future__ import absolute_import, division, print_function

from collections import OrderedDict
from functools import partial

import maya.cmds as cmds
import maya.mel as mel


class RecentFileWindow(object):
    u"""最近開いたファイルへのアクセス補助クラス"""

    _WINDOW_NAME = "mayatools_OpenRecentFiles"
    _WINDOW_TITLE = "OpenRecentFiles"

    @staticmethod
    def main():
        u"""ツール起動"""
        RecentFileWindow().show()

    def show(self):
        u"""Windowを表示"""
        self.safe_delete_ui(RecentFileWindow._WINDOW_NAME)

        cmds.window(RecentFileWindow._WINDOW_NAME, title=RecentFileWindow._WINDOW_TITLE)
        cmds.frameLayout(label="RecentFiles",
                         marginWidth=6,
                         marginHeight=6,
                         borderStyle="etchedIn")

        for file_path, file_type in get_recent_files().items():
            cmds.button(label=file_path, c=partial(self._open_file, file_path, file_type))
        cmds.showWindow(RecentFileWindow._WINDOW_NAME)

    def _open_file(self, file_path, file_type, *args):
        u"""指定されたファイルを開く"""
        open_file(file_path, file_type)
        self.safe_delete_ui(RecentFileWindow._WINDOW_NAME)

    def safe_delete_ui(self, ui_name):
        u"""指定されたUIの存在確認をした上で削除する"""
        if cmds.window(ui_name, exists=True):
            cmds.deleteUI(ui_name)


def get_recent_files():
    u"""最近開いたファイルの情報を返す

    :return: 最近開いたファイルパスをキー、ファイルタイプを値とする辞書
    :rtype: OrderedDict
    """
    files = cmds.optionVar(q="RecentFilesList")
    file_types = cmds.optionVar(q="RecentFilesTypeList")
    files.reverse()
    file_types.reverse()
    return OrderedDict(zip(files, file_types))


def open_file(file_path, file_type):
    u"""指定されたファイルを開く

    :param file_path: ファイルパス
    :type file_path: unicode
    :param file_type: ファイルタイプ
    :type file_type: unicode
    """
    cmds.file(force=True, new=True)
    mel.eval('openRecentFile("{0}", "{1}");'.format(file_path, file_type))
