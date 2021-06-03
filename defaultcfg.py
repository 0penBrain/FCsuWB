## Set status bar helpers

cfg = {}

cfg['clearNavIndictor'] = False

cfg['custBarEnabled'] = True

cfg['custBar'] = """[
    [sbwidget.VisibilityTool, []]
#    ,[sbwidget.ParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection']]
#    ,[sbwidget.ParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection', lambda:Gui.runCommand('Std_ExportGraphviz',0)]]
    ,[sbwidget.DockToggler, ['Report view','R', Gui.getMainWindow().findChild(QtWidgets.QTextEdit, 'Report view').clear]]
    ,[sbwidget.DockToggler, ['Python console', 'Y', Gui.getMainWindow().findChild(QtWidgets.QPlainTextEdit, 'Python console').onClearConsole]]
    ,[sbwidget.DockToggler, ['Combo View', 'C', fcinfo.getFCInfo]]
    ,[sbwidget.DockToggler, ['Selection view', 'S']]
    ,[sbwidget.DockToggler, ['Property view', 'P']]
    ,[sbwidget.DockToggler, ['Tree view', 'T']]
    ,[sbwidget.CmdRunner, ['D', ['Std_DependencyGraph',0]]]
]"""

## Set SubWindow splitter

cfg['windowSplitterEnabled'] = True

## Set Dock widgets font sizers

cfg['fontSizerEnabled'] = False
