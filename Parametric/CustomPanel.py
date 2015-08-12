# create new Tab in ComboView
import os
import FreeCAD, FreeCADGui
from PySide import QtGui,QtCore
#from PySide import uic

def getMainWindow():
   "returns the main window"
   # using QtGui.qApp.activeWindow() isn't very reliable because if another
   # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
   # returned
   toplevel = QtGui.qApp.topLevelWidgets()
   for i in toplevel:
       if i.metaObject().className() == "Gui::MainWindow":
           return i
   raise Exception("No main window found")

def getComboView(mw):
   dw=mw.findChildren(QtGui.QDockWidget)
   for i in dw:
       if str(i.objectName()) == "Combo View":
           return i.findChild(QtGui.QTabWidget)
       elif str(i.objectName()) == "Python Console":
           return i.findChild(QtGui.QTabWidget)
   raise Exception ("No tab widget found")

mw = getMainWindow()
tab = getComboView(getMainWindow())
tab2 = FreeCADGui.PySideUic.loadUi(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'ParamModifier.ui'))
tab.addTab(tab2,"Parameter(s)")
tab2.show()
#tab.removeTab(2)