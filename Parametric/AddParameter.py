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


import os, sys
from PySide.QtGui import QRegExpValidator
from PySide.QtCore import QRegExp

import FreeCAD, FreeCADGui
import Parameter

class AddParameter:
    """Creates a new parameter"""

    def GetResources(self):
        return {'Pixmap'  : os.path.join(os.path.realpath(os.path.dirname(__file__)), 'Gui', 'Resources', 'icons', 'AddParameter.svg'), # the name of a svg file available in the resources
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
        rx = QRegExp("^([a-zA-Z][]a-zA-Z0-9_]*)$")
        self.form.nameLineEdit.setValidator(QRegExpValidator(rx))

        # Connect Signals and Slots
        self.form.addPushButton.clicked.connect(self.onAdd)
        self.form.addPushButton.clicked.connect(self.form.nameLineEdit.clear)
        self.form.objectComboBox.currentIndexChanged.connect(self.onObjectSelected)
        self.form.propertyComboBox.currentIndexChanged.connect(self.onPropertySelected)
        self.form.minRangeCheckBox.stateChanged.connect(self.onMinRangeToggled)
        self.form.minRangeSpinBox.valueChanged.connect(self.onMinRangeValueChanged)
        self.form.maxRangeCheckBox.stateChanged.connect(self.onMaxRangeToggled)
        self.form.maxRangeSpinBox.valueChanged.connect(self.onMaxRangeValueChanged)

        # Set default state
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
        """ Sets in the combobox the objects that can be parametric """
        objectLabels = Parameter.Parameter.getAvailableObjectsLabels()
        if objectLabels:
            self.form.objectComboBox.clear()
            self.form.objectComboBox.addItems(objectLabels)

            self.setAvailableProperties()
        else:
            self.form.objectComboBox.setEditable(False)
            self.form.propertyComboBox.setEditable(False)

    def setAvailableProperties(self):
        """ Sets in the combobox the properties that can be parametric """
        propertyLabels = Parameter.Parameter.getAvailableProperties(self.form.objectComboBox.currentText())
        if propertyLabels:
            self.form.propertyComboBox.clear()
            self.form.propertyComboBox.addItems(propertyLabels)
        else:
            self.form.propertyComboBox.setEditable(False)

    def setPropertyValue(self):
        """ Sets the default property value to be the current value from the part property """
        # Get current object and property
        currentObjectText = self.form.objectComboBox.currentText()
        currentPropertyText = self.form.propertyComboBox.currentText()
        currentProperty = FreeCAD.ActiveDocument.getObjectsByLabel(currentObjectText)[0].getPropertyByName(currentPropertyText)

        # Set spinbox range
        self.form.minRangeSpinBox.setEnabled(False)
        self.form.minRangeSpinBox.setValue(0)
        self.setMinValueLimits(None)
        self.form.maxRangeSpinBox.setEnabled(False)
        self.form.maxRangeSpinBox.setValue(0)
        self.setMaxValueLimits(None)

        # Set current object value
        self.form.valueSpinBox.setValue(currentProperty.Value)

    def update(self):
        FreeCAD.Console.PrintMessage(dir(self.form))

    def onAdd(self):
        if self.isFormValid():
            a = Parameter.createParameter()

            name = self.form.nameLineEdit.text()
            if name:
                a.Name = name

            a.ObjectLabel = str(self.form.objectComboBox.currentText())
            a.ObjectProperty = str(self.form.propertyComboBox.currentText())

            if self.form.minRangeCheckBox.isChecked():
                a.MinRangeEnabled = True
                a.MinRange = self.form.minRangeSpinBox.value()

            if self.form.maxRangeCheckBox.isChecked():
                a.MaxRangeEnabled = True
                a.MaxRange = self.form.maxRangeSpinBox.value()

            a.Value = self.form.valueSpinBox.value()

            # Reset default widget
            self.default()
        else:
            FreeCAD.Console.PrintError("Invalid data. Could not create parameter.\n")

    def onObjectSelected(self):
        """  When a different object is selected, properties have to be refreshed """
        self.setAvailableProperties()

    def onPropertySelected(self):
        """ When a different property is selected, the value should be changed accordingly """
        self.setPropertyValue()

    def onMaxRangeToggled(self):
        """ When the max range checkbox is toggled, this enables/disables the corresponding spinBox """
        if self.form.maxRangeCheckBox.isChecked():
            self.form.maxRangeSpinBox.setEnabled(True)
            self.form.maxRangeSpinBox.setValue(self.form.valueSpinBox.value())
        else:
            self.form.maxRangeSpinBox.setEnabled(False)
            self.form.maxRangeSpinBox.setValue(0)
            self.setMaxValueLimits(None)

    def onMaxRangeValueChanged(self):
        """ Updates the value spinbox limits """
        self.setMaxValueLimits(self.form.maxRangeSpinBox.value())

    def onMinRangeToggled(self):
        """ When the min range checkbox is toggled, this enables/disables the corresponding spinBox """
        if self.form.minRangeCheckBox.isChecked():
            self.form.minRangeSpinBox.setEnabled(True)
            self.form.minRangeSpinBox.setValue(self.form.valueSpinBox.value())
            self.onMinRangeValueChanged()
        else:
            self.form.minRangeSpinBox.setEnabled(False)
            self.form.minRangeSpinBox.setValue(0)
            self.setMinValueLimits(None)

    def onMinRangeValueChanged(self):
        """ Updates the value spinbox limits """
        self.setMinValueLimits(self.form.minRangeSpinBox.value())

    def setMaxValueLimits(self, max_limit=None):
        """ Sets the max values of the value spin box """
        if not max_limit:
            float_max = sys.float_info.max
            self.form.valueSpinBox.setMaximum(float_max)
        else:
            self.form.valueSpinBox.setMaximum(max_limit)

    def setMinValueLimits(self, min_limit=None):
        """ Sets the max values of the value spin box """
        # Get current object and property
        currentObjectText = self.form.objectComboBox.currentText()
        currentPropertyText = self.form.propertyComboBox.currentText()
        currentProperty = FreeCAD.ActiveDocument.getObjectsByLabel(currentObjectText)[0].getPropertyByName(currentPropertyText)

        # Set spinbox range
        if not min_limit:
            if currentProperty.Unit.Type == 'Angle':
                float_max = sys.float_info.max
                self.form.valueSpinBox.setMinimum(-float_max)
            else:
                self.form.valueSpinBox.setMinimum(0)
        else:
            self.form.valueSpinBox.setMinimum(min_limit)

    def isFormValid(self):
        """ Checks the information in the form (in this case, if the name is already set in other parameter """
        # Check if name is already set
        params = [obj.Name for obj in Parameter.Parameter.getAvailableParameters()]
        if self.form.nameLineEdit.text() in params:
            FreeCAD.Console.PrintError("Parameter name already in use\n")
            return False

        return True

    def accept(self):
        FreeCADGui.Control.closeDialog()

    def reject(self):
        FreeCADGui.Control.closeDialog()