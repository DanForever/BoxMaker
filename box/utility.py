
import adsk.core

def CreateComponent( parent, name ):
    # Create Component
    identityTransform = adsk.core.Matrix3D.create()
    occurrence = parent.occurrences.addNewComponent( identityTransform )
    
    component = occurrence.component
    component.name = name
    
    return component