import FreeCAD, FreeCADGui

__author__ = 'def'

class Parameter:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "Parameter"
        obj.addProperty("App::PropertyString", "Name", "Parametric", "Name of the parameter")
        obj.addProperty("App::PropertyQuantity", "Value", "Parametric", "Value currently assigned to the parameter")
        obj.addProperty("App::PropertyString", "ObjectLabel", "Parametric", "Label of the object assigned to this parameter")
        obj.addProperty("App::PropertyString", "ObjectProperty", "Parametric", "Label of the property assigned to this parameter")

    def onChanged(self, obj, prop):
        "'''Do something when a property has changed'''"
        # Get value that has changed
        changed_value = obj.getPropertyByName(prop)
        objects = FreeCAD.ActiveDocument.getObjectsByLabel(obj.ObjectLabel)
        if objects:
            for object in objects:
                setattr(object, obj.ObjectProperty, changed_value)

        FreeCAD.Console.PrintMessage("Changed property: " + str(prop) + " with value: " + str(changed_value) + "\n")


    def execute(self, obj):
        "'''Do something when doing a recomputation, this method is mandatory'''"
        if obj.ViewObject:
            obj.ViewObject.update()

    # def __getstate__(self):
    #     return self.Type
    #
    # def __setstate__(self,state):
    #     if state:
    #         self.Type = state
    #


class ViewProviderParameter:
    def __init__(self, obj):
        "'''Set this object to the proxy object of the actual view provider'''"
        obj.Proxy = self

    def attach(self, obj):
        "'''Setup the scene sub-graph of the view provider, this method is mandatory'''"
        pass

    def updateData(self, obj, prop):
        "'''If a property of the handled feature has changed we have the chance to handle this here'''"
        FreeCAD.Console.PrintMessage("Update data for property: " + str(prop) + "\n")

    def onChanged(self, obj, prop):
        "'''Here we can do something when a single property got changed'''"
        FreeCAD.Console.PrintMessage("Changed property: " + str(prop) + "\n")

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
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Parameter")
    Parameter(a)
    ViewProviderParameter(a.ViewObject)