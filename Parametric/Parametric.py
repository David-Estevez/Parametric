__author__ = 'def'

import FreeCAD, FreeCADGui

class ScriptCmd:
   def Activated(self):
       # Here your write what your ScriptCmd does...
       FreeCAD.Console.PrintMessage('Hello, World!')
   def GetResources(self):
       return {'Pixmap' : 'path_to_an_icon/myicon.png', 'MenuText': 'Short text', 'ToolTip': 'More detailed text'}

FreeCADGui.addCommand('Script_Cmd', ScriptCmd())