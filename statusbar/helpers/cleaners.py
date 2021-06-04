from PySide2 import QtWidgets
import FreeCADGui as Gui

def cleanReportView():
    Gui.getMainWindow().findChild(QtWidgets.QTextEdit, 'Report view').clear()

def cleanPythonConsole():
    Gui.getMainWindow().findChild(QtWidgets.QPlainTextEdit, 'Python console').onClearConsole()
