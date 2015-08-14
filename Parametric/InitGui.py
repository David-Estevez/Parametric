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