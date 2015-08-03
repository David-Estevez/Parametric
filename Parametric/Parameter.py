import FreeCAD, FreeCADGui

__author__ = 'def'

class Parameter:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "Parameter"
        obj.addProperty("App::PropertyString", "Name", "Parametric", "Name of the parameter")
        obj.addProperty("App::PropertyQuantity", "Value", "Parametric", "Value currently assigned to the parameter")
        obj.addProperty("App::PropertyEnumeration", "ObjectLabel", "Parametric", "Label of the object assigned to this parameter")
        obj.addProperty("App::PropertyEnumeration", "ObjectProperty", "Parametric", "Label of the property assigned to this parameter")
        obj.setEditorMode("ObjectLabel", 0)
        obj.setEditorMode("ObjectProperty", 0)

        # Set default values:
        obj.Name = obj.Label
        obj.ObjectLabel = self.getAvailableObjectsLabels()
        obj.ObjectProperty = self.getAvailableLabels(obj.ObjectLabel)
        obj.Value  = FreeCAD.ActiveDocument.getObjectsByLabel(obj.ObjectLabel)[0].getPropertyByName(obj.ObjectProperty)


    def onChanged(self, obj, prop):
        "'''Do something when a property has changed'''"
        # Get value that has changed
        if prop == 'Value':
            self.update_referenced_objects(obj)
        elif prop == 'ObjectLabel':
            previous_property = obj.ObjectProperty
            obj.ObjectProperty = self.getAvailableLabels(obj.ObjectLabel)
            try:
                obj.ObjectProperty = previous_property
            except:
                pass

            self.update_referenced_objects(obj)

    def execute(self, obj):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        if obj.ViewObject:
            obj.ViewObject.update()

        #obj.ObjectLabel = self.getAvailableObjectsLabels()
        #obj.ObjectProperty = self.getAvailableLabels(obj.ObjectLabel)


    # def __getstate__(self):
    #     return self.Type
    #
    # def __setstate__(self,state):
    #     if state:
    #         self.Type = state
    #

    def updateData(self, obj, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        previous_label = obj.ObjectLabel
        previous_property = obj.ObjectProperty

        obj.ObjectLabel = self.getAvailableObjectsLabels()
        obj.ObjectProperty = self.getAvailableLabels(obj.ObjectLabel)

        try:
            obj.ObjectLabel = previous_label

            try:
                obj.ObjectProperty = previous_property
            except:
                pass
        except:
            pass

    def update_referenced_objects(self, obj):
            objects = FreeCAD.ActiveDocument.getObjectsByLabel(obj.ObjectLabel)

            if objects:
                for object in objects:
                    try:
                        setattr(object, obj.ObjectProperty, obj.Value)
                        FreeCAD.Console.PrintMessage("Changed property: " + str(obj.ObjectProperty) + " with value: " + str(obj.Value) + "\n")
                    except:
                        FreeCAD.Console.PrintError("Could not change property: " + str(obj.ObjectProperty) + " with value: " + str(obj.Value) + "\n")

    @staticmethod
    def getAvailableObjects():
        return [ obj for obj in FreeCAD.ActiveDocument.Objects if 'Part::' in obj.TypeId ]

    @staticmethod
    def getAvailableObjectsLabels():
        return [ str(obj.Label) for obj in Parameter.getAvailableObjects()]

    @staticmethod
    def getAvailableLabels(obj_label):
        obj = FreeCAD.ActiveDocument.getObjectsByLabel(obj_label)
        if obj:
            return [ property_name  for property_name in obj[0].PropertiesList if isinstance(getattr(obj[0], property_name), FreeCAD.Units.Quantity) ]
        else:
            return []



class ViewProviderParameter:
    def __init__(self, obj):
        "'''Set this object to the proxy object of the actual view provider'''"
        obj.Proxy = self

    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        pass

    def updateData(self, obj, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        FreeCAD.Console.PrintMessage("[View] Update data for property: " + str(prop) + "\n")

    def onChanged(self, obj, prop):
        "'''Here we can do something when a single property got changed'''"
        FreeCAD.Console.PrintMessage("[View] Changed property: " + str(prop) + "\n")

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

    def __getstate__(self):
        """ When saving the document this object gets stored using Python's json module.\'
            Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\'
            to return a tuple of all serializable objects or None."""
        return None

    def __setstate__(self,state):
        """ When restoring the serialized object from document we have the chance to set some internals here.\'
            Since no data were serialized nothing needs to be done here."""
        return None

def makeParameter():
    FreeCAD.newDocument()
    FreeCADGui.activateWorkbench("PartWorkbench")
    FreeCAD.ActiveDocument.addObject("Part::Box","Box")
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Parameter")
    Parameter(a)
    ViewProviderParameter(a.ViewObject)