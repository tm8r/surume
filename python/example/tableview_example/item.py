# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from example.tableview_example.columns import Column, Columns

from maya import cmds


class FileInfo(Columns):
    u"""ファイル情報"""
    header = ["Thumb", "Name", "Path"]
    row_count = len(header)

    def __init__(self, node):
        u"""initialize

        :param path: ファイルパス
        :type path: unicode
        """
        super(FileInfo, self).__init__()
        self.node = node
        self.thumbnail = Column(0, "")
        self.name = Column(1, node)
        self.file_type = Column(2, cmds.getAttr(node + ".fileTextureName").replace("a11889", "tm8r"))
