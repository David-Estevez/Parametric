__author__ = 'def'

class ParametricWorkbench (Workbench):

    MenuText = "Parametric workbench"
    ToolTip = "Work with parameters in FreeCAD"
    Icon = FreeCAD.getResourceDir() + "Mod/Parametric/Resources/icons/parametric.svg"

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        import Parametric, AddParameter, RecomputeParameters # import here all the needed files that create your FreeCAD commands
        self.list = ["AddParameter", "RecomputeParameters"] # A list of command names created in the line above
        self.appendToolbar("Parametric Toolbar",self.list) # creates a new toolbar with your commands
        self.appendMenu("Parametric",self.list) # creates a new menu

    def Activated(self):
        "This function is executed when the workbench is activated"
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("Parametric",self.list) # add commands to the context menu

    def GetClassName(self):
        """Return the name of the associated C++ class."""
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"

Gui.addWorkbench(ParametricWorkbench())