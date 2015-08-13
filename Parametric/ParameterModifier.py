__author__ = 'def'

# Limit h axis to 260px min

if __name__ == '__main__':
    from PySide import QtCore, QtGui
    from PySide import QtUiTools
    import os, sys

    class Dummy:
        def __init__(self, widget):
            self.widget = widget
        def print_width(self):
            print self.widget.geometry()

    # Create the window
    import sys
    app = QtGui.QApplication(sys.argv)

    # Load ui file
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile( os.path.join(os.path.realpath(os.path.dirname(__file__)), 'ParamModifier.ui'))
    ui_file.open(QtCore.QFile.ReadOnly)
    myWidget = loader.load(ui_file, None)
    ui_file.close()

    # Show the widget as main window
    window = myWidget
    foo = Dummy(window)
    window.pushButton.clicked.connect(foo.print_width)
    window.show()
    sys.exit(app.exec_())