## Set status bar helpers

cfg = {}

cfg['custBarEnabled'] = True

cfg['custBar'] = """[
    [sbwidget.visibilityTool, []]
#    ,[sbwidget.custParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection']]
#    ,[sbwidget.custParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection', lambda:Gui.runCommand('Std_ExportGraphviz',0)]]
    ,[sbwidget.custDockToggler, ['Report view','R', Gui.getMainWindow().findChild(QtGui.QTextEdit, 'Report view').clear]]
    ,[sbwidget.custDockToggler, ['Python console', 'Y', Gui.getMainWindow().findChild(QtGui.QPlainTextEdit, 'Python console').onClearConsole]]
    ,[sbwidget.custDockToggler, ['Combo View', 'C', fcinfo.getFCInfo]]
    ,[sbwidget.custDockToggler, ['Selection view', 'S']]
    ,[sbwidget.custDockToggler, ['Property view', 'P']]
    ,[sbwidget.custDockToggler, ['Tree view', 'T']]
    ,[sbwidget.custCmdRunner, ['D', ['Std_DependencyGraph',0]]]
]"""

## Set Dock widgets font sizers

cfg['fontSizerEnabled'] = False
