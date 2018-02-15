# -*- coding: utf-8 -*-
u"""post-deformationになっているblendshapeをpre-deformationに変換"""
from __future__ import absolute_import, division, print_function

from maya import cmds


def collect_post_deformation_node():
    u"""post-deformationになっているノードを収集

    Returns:
        list of unicode: post-deformationになっているノードのリスト
    """
    result = []
    blendshapes = cmds.ls(type="blendShape")
    for b in blendshapes:
        target = cmds.blendShape(b, q=True, g=True)[0]
        histories = cmds.listHistory(target, gl=True, pdo=True, lf=True, f=False, il=2)
        skin_cluster_found = False
        for h in histories:
            object_type = cmds.objectType(h)
            if object_type == "skinCluster":
                skin_cluster_found = True
                continue
            if object_type == "blendShape" and not skin_cluster_found:
                result.append(target)
                break
    return result


def convert_pre_deformation(target):
    u"""指定ノードをpre-deformationに変換する

    Args:
        target (unicode): 対象のノード
    """
    histories = cmds.listHistory(target, gl=True, pdo=True, lf=True, f=False, il=2)
    last_blend_shape = None
    for h in histories:
        object_type = cmds.objectType(h)
        if object_type == "skinCluster":
            last_skin_cluster = h
            continue
        if object_type == "blendShape":
            last_blend_shape = h

    cmds.reorderDeformers(last_skin_cluster, last_blend_shape, target)


def convert_all_pre_deformation(*args):
    u"""post-deformationになっている全ノードをpre-deformationに変換する

    Args:
        target (unicode): 対象のノード
    """
    res = collect_post_deformation_node()
    if not res:
        cmds.confirmDialog(t="Complete", m=u"Post-deformationになっているノードは含まれていませんでした。")
        return
    for r in res:
        convert_pre_deformation(r)
    cmds.confirmDialog(t="Complete", m=u"Post-deformationに変換しました。")