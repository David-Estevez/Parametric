__author__ = 'def'

import os

import FreeCAD, FreeCADGui
import Parameter

class AddParameter:
    """Creates a new parameter"""

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'MenuText': 'Add parameter',
                'ToolTip' : 'Create a new parameter associated to an object'}

    def Activated(self):
        FreeCAD.Console.PrintMessage("AddParameter() called!")
        task_panel = AddParameterTaskPanel()
        # FreeCADGui.Control.showDialog(task_panel)
        Parameter.createParameter()
        return

    def IsActive(self):
        """ Only active when there is a document """
        if not FreeCAD.ActiveDocument:
            return False

        return True

FreeCADGui.addCommand('AddParameter', AddParameter())

class AddParameterTaskPanel:
    """ UI for adding Parameters"""

    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'AddParameter.ui'))

        # Connect Signals and Slots

        self.update()

    def update(self):
        FreeCAD.Console.PrintMessage(dir(self.form))
        labels = [ obj.Label for obj in FreeCAD.activeDocument().Objects]
        if labels:
            self.form.comboBox_2.addItems(labels)

    def accept(self):
        FreeCADGui.Control.closeDialog()

    def reject(self):
        FreeCADGui.Control.closeDialog()