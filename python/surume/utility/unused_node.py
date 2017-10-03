# -*- coding: utf-8 -*-
u"""未使用ノード関連"""
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

_DEFAULT_SHADING_ENGINES = ["initialParticleSE", "initialShadingGroup"]


def get_unused_utility_nodes():
    u"""未使用のユーティリティノードのリストを返す

    :return: 未使用のユーティリティノードのリスト
    :rtype: list of unicode
    """
    utility_node_types = cmds.listNodeTypes("utility")
    utility_nodes = []
    for ul in utility_node_types:
        nodes = cmds.ls(type=ul)
        if not nodes:
            continue
        utility_nodes.extend(nodes)

    unused = []
    for u in utility_nodes:
        if not [x for x in cmds.listConnections(u) if x != "defaultRenderUtilityList1"]:
            unused.append(u)
    return unused


def get_unused_shading_engines():
    u"""未使用のShadingEngineのリストを返す

    :return: 未使用のShadingEngineのリスト
    :rtype: list of unicode
    """
    shading_engines = cmds.ls(type="shadingEngine")

    unused_shading_engines = []
    for s in shading_engines:
        if s in _DEFAULT_SHADING_ENGINES:
            continue
        unused = True
        for c in cmds.listConnections(s):
            node_type = cmds.nodeType(c)
            if "shader" in cmds.getClassification(node_type)[0]:
                unused = False
                break
        if unused:
            unused_shading_engines.append(s)
    return unused_shading_engines


import pymel.core as pm

import time


def get_vertexes():
    sl = cmds.ls(sl=True)
    for s in sl:
        uvs = cmds.polyListComponentConversion(s, tuv=True)
        if not uvs:
            continue
        res = cmds.ls(uvs, fl=True)
        # print(res)


def get_vertexes_pymel():
    sl = pm.ls(sl=True)
    for s in sl:
        uvs = s.map
        if not uvs:
            continue
        res = [x.name() for x in pm.ls(uvs, fl=True)]
        # print(res)


count = 100000
start = time.time()
for i in xrange(0, count):
    get_vertexes()
end = time.time()
print("cmd", end - start)

start = time.time()
for i in xrange(0, count):
    get_vertexes_pymel()
end = time.time()
print("pym", end - start)
