__author__ = 'def'

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

