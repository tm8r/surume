# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class Column(object):
    u"""カラム情報"""

    def __init__(self, index, value):
        u"""initialize

        :param index: カラムのインデックス
        :type index: int
        :param value: 任意の値
        :type value: object
        """
        self.index = index
        self.value = value


class Columns(object):
    u"""インスタンス変数からColumnクラスのものを抽出してcolumnsメソッドで取得できるクラス"""

    def __init__(self):
        u"""initialize"""
        self._columns = None

    @property
    def columns(self):
        u"""カラムのリストを返す

        :return: カラムのリスト
        :rtype: list of Column
        """
        if self._columns is None:
            self._columns = self._get_columns()
        return self._columns

    def _get_columns(self):
        u"""インスタンス変数からColumnクラスのものを抽出して返す

        :return: カラムのリスト
        :rtype: list of Column
        """
        tmp_columns = []
        for k, v in self.__dict__.items():
            if type(v) == Column:
                tmp_columns.append(v)
        return sorted(tmp_columns, key=lambda x: x.index)
