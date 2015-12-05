__author__ = 'def'

# Limit h axis to 260px min

if __name__ == '__main__':
    from PySide import QtCore, QtGui
    from PySide import QtUiTools
    import os, sys
    import random

    class Dummy:
        paths = ['WidgetStdParameter.ui', 'WidgetBoundedParameter.ui', 'WidgetAngleParameter.ui']

        def __init__(self, widget):
            self.widget = widget
        def print_width(self):
            print self.widget.geometry()
        def add(self):
            newWidget = load_ui(random.choice(self.paths))
            self.widget.scrollAreaWidgetContents.layout().insertWidget(0, newWidget)

    def load_ui(file_name):
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile( os.path.join(os.path.realpath(os.path.dirname(__file__)), file_name))
        ui_file.open(QtCore.QFile.ReadOnly)
        myWidget = loader.load(ui_file, None)
        ui_file.close()
        return myWidget



    # Create the window
    import sys
    app = QtGui.QApplication(sys.argv)

    # Load ui file
    window = load_ui('ParamModifier.ui')
    widget1 = load_ui('WidgetStdParameter.ui')
    widget2 = load_ui('WidgetBoundedParameter.ui')
    widget3 = load_ui('WidgetAngleParameter.ui')

    # Show the widget as main window
    # window.scrollAreaWidgetContents.layout().insertWidget(0, widget1)
    # window.scrollAreaWidgetContents.layout().insertWidget(0, widget2)
    # window.scrollAreaWidgetContents.layout().insertWidget(0, widget3)


    foo = Dummy(window)
    window.pushButton.clicked.connect(foo.print_width)
    window.pushButton.clicked.connect(foo.add)
    window.show()
    sys.exit(app.exec_())