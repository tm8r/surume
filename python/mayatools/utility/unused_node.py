# -*- coding: utf-8 -*-
u"""未使用ノード関連"""
from __future__ import absolute_import, division, print_function

import maya.cmds as cmds

_DEFAULT_SHADING_ENGINES = ["initialParticleSE", "initialShadingGroup"]


def get_unused_utility_nodes():
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
