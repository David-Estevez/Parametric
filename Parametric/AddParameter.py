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
        task_panel = AddParameterTaskPanel()
        FreeCADGui.Control.showDialog(task_panel)
        # Parameter.createParameter()
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
        self.form.addPushButton.clicked.connect(self.onAdd)
        self.form.addPushButton.clicked.connect(self.form.nameLineEdit.clear)
        self.form.objectComboBox.currentIndexChanged.connect(self.onObjectSelected)
        self.form.propertyComboBox.currentIndexChanged.connect(self.onPropertySelected)

        self.default()


    def default(self):
        """ Sets the panel to its default state """
        # Default name:
        self.form.nameLineEdit.setText("")
        self.form.nameLineEdit.setPlaceholderText("(Optional)")

        # Default objects and properties:
        self.setAvailableObjects()

        # Default value:
        self.setPropertyValue()

    def setAvailableObjects(self):
        objectLabels = Parameter.Parameter.getAvailableObjectsLabels()
        if objectLabels:
            self.form.objectComboBox.clear()
            self.form.objectComboBox.addItems(objectLabels)

            self.setAvailableProperties()
        else:
            self.form.objectComboBox.setEditable(False)
            self.form.propertyComboBox.setEditable(False)

    def setAvailableProperties(self):
        propertyLabels = Parameter.Parameter.getAvailableProperties(self.form.objectComboBox.currentText())
        if propertyLabels:
            self.form.propertyComboBox.clear()
            self.form.propertyComboBox.addItems(propertyLabels)
        else:
            self.form.propertyComboBox.setEditable(False)

    def setPropertyValue(self):
        currentObject = self.form.objectComboBox.currentText()
        currentProperty = self.form.propertyComboBox.currentText()
        self.form.valueSpinBox.setValue(
            FreeCAD.ActiveDocument.getObjectsByLabel(currentObject)[0].getPropertyByName(currentProperty).Value)

    def update(self):
        FreeCAD.Console.PrintMessage(dir(self.form))

    def onAdd(self):
        if self.isFormValid():
            try:
                a = Parameter.createParameter()

                name = self.form.nameLineEdit.text()
                if name:
                    a.Name = name

                a.ObjectLabel = str(self.form.objectComboBox.currentText())
                a.ObjectProperty = str(self.form.propertyComboBox.currentText())

                FreeCAD.Console.PrintMessage("Value: " + str(self.form.valueSpinBox.value()) + "\n")
                a.Value = self.form.valueSpinBox.value()
            except Exception, e:
                FreeCAD.Console.PrintError(str(e)+ "\n")

            self.default()
        else:
            FreeCAD.Console.PrintError("Invalid data. Could not create parameter.\n")

    def onObjectSelected(self):
        """  When a different object is selected, properties have to be refreshed """
        FreeCAD.Console.PrintMessage("Changed object selection!\n")
        self.setAvailableProperties()

    def onPropertySelected(self):
        """ When a different property is selected, the value should be changed accordingly """
        FreeCAD.Console.PrintMessage("Changed property selection!\n")
        self.setPropertyValue()

    def isFormValid(self):
        return True

    def accept(self):
        FreeCADGui.Control.closeDialog()

    def reject(self):
        FreeCADGui.Control.closeDialog()