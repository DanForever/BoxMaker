import adsk.core

from . import create
from . import value

class Command():
    def __init__( self ):
        self.handlers = []
        
    def Start( self ):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        
        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = self.ui.commandDefinitions.itemById( value.command.id )
        if not cmdDef:
            cmdDef = self.ui.commandDefinitions.addButtonDefinition( value.command.id, value.command.name, value.command.tooltip )
        
        handler = create.Handler()
        cmdDef.commandCreated.add( handler )
        self.handlers.append( handler )
        
        # Get the ADD-INS panel in the model workspace. 
        addInsPanel = self.ui.allToolbarPanels.itemById( value.command.panelId )
        
        # Add the button to the bottom of the panel.
        addInsPanel.controls.addCommand( cmdDef )
        
        self.ui.messageBox( 'Box Maker Started!' )
        
    def Stop( self ):
        if self.ui:
            self.ui.messageBox( 'Stop box maker' )
        
            # Clean up the UI.
            cmdDef = self.ui.commandDefinitions.itemById( value.command.id )
            if cmdDef:
                cmdDef.deleteMe()

            addinsPanel = self.ui.allToolbarPanels.itemById( value.command.panelId )
            cntrl = addinsPanel.controls.itemById( value.command.id )
            if cntrl:
                cntrl.deleteMe()
