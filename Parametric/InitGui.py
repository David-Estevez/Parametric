__author__ = 'def'

class ParametricWorkbench (Workbench):
    MenuText = "Parametric"
    ToolTip = "Work with parameters in FreeCAD"
    Icon =  """
            /* XPM */
            static char * Parameter_64_xpm[] = {
            "64 64 16 1",
            " 	c None",
            ".	c #000000",
            "+	c #005FFF",
            "@	c #0060FF",
            "#	c #005EFF",
            "$	c #000714",
            "%	c #000B1E",
            "&	c #000103",
            "*	c #000918",
            "=	c #000D23",
            "-	c #00050D",
            ";	c #000001",
            ">	c #000917",
            ",	c #000D22",
            "'	c #000102",
            ")	c #000101",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                 ...    ..                      ",
            "                               ...........                      ",
            "                             ..... ......                       ",
            "                            ....    .....                       ",
            "                           ....     .....                       ",
            "                          ....      .....                       ",
            "                          ....      ....                        ",
            "                         ....       ....                        ",
            "                         ....       ....                        ",
            "                        ....       ....                         ",
            "                        ....       ....                         ",
            "                        ....      .....                         ",
            "                        ...      ......                         ",
            "                       ....      .....                          ",
            "                       .....    ...... ..                       ",
            "                        ....  ...........                       ",
            "                        ........  ......                        ",
            "   ...                  .......   .....                    ..   ",
            "   ...                    ...     ...                     ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...        ++                                @+        ...   ",
            "   ...     #+++                                  +++      ...   ",
            "   ...   ++@+++                                  +++@++   ...   ",
            "   ... +#++++++                                  ++++++#+ ...   ",
            "   ..$++++++++####################################++++++++%..   ",
            "   &.*++++++++++++++++++++++++++++++++++++++++++++++++++++=.-   ",
            "   ;.>++++++++####################################++++++++,.'   ",
            "   ..) ++++++++                                  ++++++++ '..   ",
            "   ...   +++++#                                  ++++++   ...   ",
            "   ...     @#++                                  @+#+     ...   ",
            "   ...       +@+                                +@+       ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "   ...                                                    ...   ",
            "                                                          ...   ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                ",
            "                                                                "};
            """
    # Icon ="/home/def/Repositories/Parametric/Parametric/Gui/Resources/icons/Parametric.svg"

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