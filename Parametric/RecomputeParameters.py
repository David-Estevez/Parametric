#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------#
#                                                                       #
# This file is part of the Parametric Workbench                         #
#                                                                       #
# Copyright (C) 2015 Mundo Reader S.L.                                  #
#                                                                       #
# Author: David Estévez Fernández <david.estevez@bq.com>                #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                       #
#-----------------------------------------------------------------------#

__author__ = "David Estévez Fernández <david.estevez@bq.com>"
__license__ = "GNU General Public License v3 http://www.gnu.org/licenses/gpl.html"


import os

import FreeCAD, FreeCADGui
import Parameter

class RecomputeParameters:
    """Creates a new parameter"""

    def GetResources(self):
        icon_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'Gui', 'Resources', 'icons', 'Force_Recompute.png')
        return {'Pixmap'  : icon_path, # the name of a svg file available in the resources
                'MenuText': 'Recompute parameters',
                'ToolTip' : 'Recompute all parameters in the document'}

    def Activated(self):
        for obj in Parameter.Parameter.getAvailableParameters():
            obj.touch()
        FreeCAD.ActiveDocument.recompute()
        return True

    def IsActive(self):
        """ Active only when there is a document, and Parameters have been created """
        if not FreeCAD.ActiveDocument:
            return False
        else:
            if Parameter.Parameter.getAvailableParameters():
                return True
            else:
                return False

FreeCADGui.addCommand('RecomputeParameters', RecomputeParameters())

