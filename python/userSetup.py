# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import maya.utils

from mayatools.startup import initialize_plugin

maya.utils.executeDeferred(initialize_plugin)
