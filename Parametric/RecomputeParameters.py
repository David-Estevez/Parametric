__author__ = 'def'

import os

import FreeCAD, FreeCADGui

class RecomputeParameters:
    """Creates a new parameter"""

    def GetResources(self):
        icon_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'Gui', 'Resources', 'icons', 'Force_Recompute.png')
        return {'Pixmap'  : icon_path, # the name of a svg file available in the resources
                'MenuText': 'Recompute parameters',
                'ToolTip' : 'Recompute all parameters in the document'}

    def Activated(self):
        for obj in FreeCAD.ActiveDocument.Objects:
            FreeCAD.Console.PrintMessage(obj.TypeId+'\n')
            try:
                if obj.Proxy.TypeId == 'Parameter':
                    obj.touch()
            except AttributeError:
                pass

        FreeCAD.ActiveDocument.recompute()

        return True

    def IsActive(self):
        """ Active only when there is a document, and Parameters have been created """
        if not FreeCAD.ActiveDocument:
            return False
        else:
            return True
            for obj in FreeCAD.ActiveDocument.Objects:
                try:
                    if obj.Proxy.TypeId == 'Parameter':
                        return True
                except AttributeError:
                    pass

            return False

FreeCADGui.addCommand('RecomputeParameters', RecomputeParameters())

