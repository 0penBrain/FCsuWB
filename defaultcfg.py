## Set status bar helpers

custBarEnabled = True

custBar = """[
    [visibilityTool, []]
#    ,[custParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection']]
#    ,[custParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection', lambda:Gui.runCommand('Std_ExportGraphviz',0)]]
    ,[custDockToggler, ['Report view','R', Gui.getMainWindow().findChild(QtGui.QTextEdit, 'Report view').clear]]
    ,[custDockToggler, ['Python console', 'Y', Gui.getMainWindow().findChild(QtGui.QPlainTextEdit, 'Python console').onClearConsole]]
    ,[custDockToggler, ['Combo View', 'C', getFCInfo]]
    ,[custDockToggler, ['Selection view', 'S']]
    ,[custDockToggler, ['Property view', 'P']]
    ,[custDockToggler, ['Tree view', 'T']]
    ,[custCmdRunner, ['D', ['Std_DependencyGraph',0]]]
]"""

## Set Dock widgets font sizers

fontSizerEnabled = False
