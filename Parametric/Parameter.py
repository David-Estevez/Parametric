import FreeCAD, FreeCADGui
import math

__author__ = 'def'

class Parameter:
    def __init__(self, obj):
        obj.Proxy = self
        self.TypeId = "Parameter"
        obj.addProperty("App::PropertyString", "Name", "Parameter", "Name of the parameter")
        obj.addProperty("App::PropertyQuantity", "Value", "Parameter", "Value currently assigned to the parameter")
        obj.addProperty("App::PropertyEnumeration", "ObjectLabel", "Parameter", "Label of the object assigned to this parameter")
        obj.addProperty("App::PropertyEnumeration", "ObjectProperty", "Parameter", "Label of the property assigned to this parameter")
        obj.addProperty("App::PropertyBool", "MaxRangeEnabled", "Range", "True if maximum range limit is enabled")
        obj.addProperty("App::PropertyQuantity", "MaxRange", "Range", "Max value for the parameter")
        obj.addProperty("App::PropertyBool", "MinRangeEnabled", "Range", "True if minimum range limit is enabled")
        obj.addProperty("App::PropertyQuantity", "MinRange", "Range", "Min value for the parameter")

        obj.setEditorMode("ObjectLabel", 0)
        obj.setEditorMode("ObjectProperty", 0)

        # Set default values:
        obj.Name = obj.Label
        obj.ObjectLabel = self.getAvailableObjectsLabels()
        obj.ObjectProperty = self.getAvailableProperties(obj.ObjectLabel)
        self.onObjectLabelChanged(obj)

        # Default range:
        obj.MaxRangeEnabled=False
        obj.setEditorMode("MaxRange", 2)
        obj.MinRangeEnabled=False
        obj.setEditorMode("MinRange", 2)

    def onChanged(self, obj, prop):
        "'''Do something when a property has changed'''"
        if prop == 'Name':
            self.onNameChanged(obj)
        elif prop == 'Value':
            self.onValueChanged(obj)
        elif prop == 'MaxRangeEnabled' or prop == 'MinRangeEnabled':
            self.onRangeToggled(obj, prop)
        elif prop == 'MaxRange' or prop == 'MinRange':
            self.onRangeChanged(obj)
        elif prop == 'ObjectProperty':
            self.onObjectPropertyChanged(obj)
        elif prop == 'ObjectLabel':
            self.onObjectLabelChanged(obj)

    def execute(self, obj):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        if obj.ViewObject:
            obj.ViewObject.update()

        FreeCAD.Console.PrintMessage("Recomputing object: " + str(obj.Label) + "\n")
        obj.ObjectLabel = self.getAvailableObjectsLabels()
        self.onObjectLabelChanged(obj)

    # def __getstate__(self):
    #     return self.Type
    #
    # def __setstate__(self,state):
    #     if state:
    #         self.Type = state
    #

    # Functions to update things when something is changed
    def onNameChanged(self, obj):
        """ Things to do when the name of this object is changed. In the future, this should update all references to this object by name."""
        # To be implemented
        pass

    def onValueChanged(self, obj):
        """ Things to do when the value of the parameter is changed. Checks range and recalculates all objects that depend on this value"""
        self.onRangeChanged(obj)
        return self.updateReferencedObjects(obj)

    def onRangeToggled(self, obj, prop):
        """ Things to do when the range of the parameter is enabled/disabled. Enables the range properties."""
        if prop == 'MaxRangeEnabled':
            if obj.MaxRangeEnabled:
                obj.setEditorMode("MaxRange", 0)
                obj.MaxRange=obj.Value.Value
                self.onRangeChanged(obj)
            else:
                obj.setEditorMode("MaxRange", 2)
        elif prop == 'MinRangeEnabled':
            if obj.MinRangeEnabled:
                obj.setEditorMode("MinRange", 0)
                obj.MinRange=obj.Value.Value
                self.onRangeChanged(obj)
            else:
                obj.setEditorMode("MinRange", 2)


    def onRangeChanged(self, obj):
        """ Things to do when the range of the parameter is modified. Crops value to be within the new range"""
        if obj.MaxRangeEnabled:
            if obj.Value.Value > obj.MaxRange:
                obj.Value.Value = obj.MaxRange.Value

        if obj.MinRangeEnabled:
            if obj.Value.Value < obj.MinRange:
                obj.Value.Value = obj.MinRange.Value

    def onObjectPropertyChanged(self, obj):
        """ Things to do when a different object property is selected. Checks the units and recomputes dependencies"""
        # Get the value currently assigned to the reference
        obj.Value.Value  = self.getReferencedValue(obj)
        self.onValueChanged(obj)

    def onObjectLabelChanged(self, obj):
        """ Things to do when the object label of the parameter is changed."""
        # Get previous state and try to restore it
        previous_property = obj.ObjectProperty
        obj.ObjectProperty = self.getAvailableProperties(obj.ObjectLabel)
        try:
            obj.ObjectProperty = previous_property
        except:
            self.onObjectPropertyChanged(obj)


    def updateData(self, obj, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        previous_label = obj.ObjectLabel
        previous_property = obj.ObjectProperty

        obj.ObjectLabel = self.getAvailableObjectsLabels()
        obj.ObjectProperty = self.getAvailableProperties(obj.ObjectLabel)

        try:
            obj.ObjectLabel = previous_label

            try:
                obj.ObjectProperty = previous_property
            except:
                pass
        except:
            pass

    @staticmethod
    def getReferencedValue(obj):
        if '.' not in obj.ObjectProperty:
            return FreeCAD.ActiveDocument.getObjectsByLabel(obj.ObjectLabel)[0].getPropertyByName(obj.ObjectProperty).Value
        else:
            object = FreeCAD.ActiveDocument.getObjectsByLabel(obj.ObjectLabel)[0]
            if 'Placement.' in obj.ObjectProperty:
                placement = getattr(object, "Placement")
                if 'Placement.Base.' in obj.ObjectProperty:
                    base = getattr(placement, "Base")
                    v = getattr(base, obj.ObjectProperty.split('.')[-1])
                    return v
                elif 'Placement.Rotation.' in obj.ObjectProperty:
                    rotation = getattr(placement, "Rotation")
                    if 'Placement.Rotation.Angle' in obj.ObjectProperty:
                        return math.degrees(rotation.Angle)
                    elif 'Placement.Rotation.Axis.' in obj.ObjectProperty:
                        axis = getattr(rotation, 'Axis')
                        v = getattr(axis, obj.ObjectProperty.split('.')[-1])
                        return v

    @staticmethod
    def updateReferencedObjects(obj):
            objects = FreeCAD.ActiveDocument.getObjectsByLabel(obj.ObjectLabel)

            if objects:
                for object in objects:
                    if '.' not in obj.ObjectProperty:
                        try:
                            setattr(object, obj.ObjectProperty, obj.Value)
                            FreeCAD.Console.PrintMessage("Changed property: " + str(obj.ObjectProperty) + " with value: " + str(obj.Value) + "\n")
                        except:
                            FreeCAD.Console.PrintError("Could not change property: " + str(obj.ObjectProperty) + " with value: " + str(obj.Value) + "\n")
                    else:
                        if 'Placement.' in obj.ObjectProperty:
                            placement = getattr(object, "Placement")
                            if 'Placement.Base.' in obj.ObjectProperty:
                                base = getattr(placement, "Base")
                                setattr(base, obj.ObjectProperty.split('.')[-1], obj.Value.Value)
                            elif 'Placement.Rotation.' in obj.ObjectProperty:
                                rotation = getattr(placement, "Rotation")
                                if 'Placement.Rotation.Angle' in obj.ObjectProperty:
                                    value_radians =  math.radians(obj.Value.Value)
                                    setattr(rotation, "Angle", value_radians)
                                elif 'Placement.Rotation.Axis.' in obj.ObjectProperty:
                                    axis = getattr(rotation, 'Axis')
                                    setattr(axis, obj.ObjectProperty.split('.')[-1], obj.Value.Value)

                        FreeCAD.Console.PrintError("Update reference for this property is not implemented yet\n")


    @staticmethod
    def getAvailableObjects():
        """ Get all objects in the active document that can be parametric"""
        return [ obj for obj in FreeCAD.ActiveDocument.Objects if 'Part::' in obj.TypeId ]

    @staticmethod
    def getAvailableObjectsLabels():
        """ Get the labels for all objects in the active document that can be parametric"""
        return [ str(obj.Label) for obj in Parameter.getAvailableObjects()]

    @staticmethod
    def getAvailableProperties(obj_label):
        """ Get all the properties in an object that can be assigned to a parameter"""
        obj = FreeCAD.ActiveDocument.getObjectsByLabel(obj_label)[0]
        if obj:
            properties = [ property_name  for property_name in obj.PropertiesList if isinstance(getattr(obj, property_name), FreeCAD.Units.Quantity) ]
            try:
                if isinstance(getattr(obj, 'Placement'), FreeCAD.Base.Placement):
                    properties.append('Placement.Base.x')
                    properties.append('Placement.Base.y')
                    properties.append('Placement.Base.z')
                    properties.append('Placement.Rotation.Angle')
                    properties.append('Placement.Rotation.Axis.x')
                    properties.append('Placement.Rotation.Axis.y')
                    properties.append('Placement.Rotation.Axis.z')
            except AttributeError:
                pass

            return properties
        else:
            return []

    @staticmethod
    def getAvailableParameters():
        """ Get all parameters on the document """
        parameters = []
        for obj in FreeCAD.ActiveDocument.Objects:
            try:
                if obj.Proxy.TypeId == 'Parameter':
                    parameters.append(obj)
            except AttributeError:
                pass
        return parameters

    # Things to do when there are changes in the document
    @staticmethod
    def slotCreatedObject(obj):
        """ Recomputes the available objects enum for all parameters. """
        for param in Parameter.getAvailableParameters():
            param.touch()
        FreeCAD.ActiveDocument.recompute()

    @staticmethod
    def slotDeletedObject(obj):
        """
        Checks if an existing parameter depends on the object deleted and, if so, deletes the parameter.
        For the rest of the parameters, recomputes the available objects enum.
        """
        for param in Parameter.getAvailableParameters():
            if param.ObjectLabel == obj.Label:
                FreeCAD.ActiveDocument.removeObject(param.Label)
                continue
            param.touch()
        FreeCAD.ActiveDocument.recompute()

    @staticmethod
    def slotChangedObject(obj, prop):
        """ Sync to be implemented. Needs to be careful to avoid entering in a loop. """
        pass
        # FreeCAD.Console.PrintMessage("Modified: %s from  %s\n"%(prop, obj.Label))
        # for param in Parameter.getAvailableParameters():
        #     param.touch()
        # FreeCAD.ActiveDocument.recompute()





class ViewProviderParameter:
    def __init__(self, obj):
        "'''Set this object to the proxy object of the actual view provider'''"
        obj.Proxy = self

    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        # FreeCAD.Console.PrintMessage("[View] Attaching\n")
        pass

    def execute(self, obj):
        "'''Do something when doing a recomputation'''"
        # FreeCAD.Console.PrintMessage("[View] Recomputing\n")
        pass

    def updateData(self, obj, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        # FreeCAD.Console.PrintMessage("[View] Update data for property: " + str(prop) + "\n")
        if prop == 'MaxRangeEnabled' or prop == 'MinRangeEnabled':
            currentSelection = FreeCADGui.Selection.getSelection(FreeCAD.ActiveDocument.Label)
            FreeCADGui.Selection.clearSelection()
            FreeCAD.Console.PrintMessage("Note: reselection is not implemented because of issue #1941\n")
            # for selected in currentSelection:
            #     FreeCADGui.Selection.addSelection(selected)

    def onChanged(self, obj, prop):
        "'''Here we can do something when a single property got changed'''"
        # FreeCAD.Console.PrintMessage("[View] Changed property: " + str(prop) + "\n")
        pass

    # def getIcon(self):
    #     "'''Return the icon in XPM format which will appear in the tree view. This method is\'''
    #             '''optional and if not defined a default icon is shown.'''"
    #     return """
    #         /* XPM */
    #         static const char * ViewProviderBox_xpm[] = {
    #         "16 16 6 1",
    #         "   c None",
    #         ".  c #141010",
    #         "+  c #615BD2",
    #         "@  c #C39D55",
    #         "#  c #000000",
    #         "$  c #57C355",
    #         "        ........",
    #         "   ......++..+..",
    #         "   .@@@@.++..++.",
    #         "   .@@@@.++..++.",
    #         "   .@@  .++++++.",
    #         "  ..@@  .++..++.",
    #         "###@@@@ .++..++.",
    #         "##$.@@$#.++++++.",
    #         "#$#$.$$$........",
    #         "#$$#######      ",
    #         "#$$#$$$$$#      ",
    #         "#$$#$$$$$#      ",
    #         "#$$#$$$$$#      ",
    #         " #$#$$$$$#      ",
    #         "  ##$$$$$#      ",
    #         "   #######      "};
    #         """

    # DisplayModes - This does not have much sense, since a parameter is not shown in view
    def getDisplayModes(self,obj):
        "'''Return a list of display modes.'''"
        modes=[]
        modes.append("None")
        return modes

    def getDefaultDisplayMode(self):
        """Return the name of the default display mode. It must be defined in getDisplayModes."""
        return "None"

    def setDisplayMode(self,mode):
        """Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done. This method is optional"""
        return mode

    def __getstate__(self):
        """ When saving the document this object gets stored using Python's json module.\'
            Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\'
            to return a tuple of all serializable objects or None."""
        return None

    def __setstate__(self,state):
        """ When restoring the serialized object from document we have the chance to set some internals here.\'
            Since no data were serialized nothing needs to be done here."""
        return None

FreeCAD.addDocumentObserver(Parameter)

def createParameter():
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Parameter")
    Parameter(a)
    ViewProviderParameter(a.ViewObject)
    return a

def makeParameter():
    FreeCAD.newDocument()
    FreeCADGui.activateWorkbench("PartWorkbench")
    FreeCAD.ActiveDocument.addObject("Part::Box","Box")

    createParameter()
