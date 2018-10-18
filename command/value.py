
class default():
    unit = "cm"

class command():
    id = "boxMakerCmdId"
    name = "Box Maker"
    tooltip = "Create simple containers ready for laser cutting"
    panelId = "SolidScriptsAddinsPanel"
    
class Inputs():
    
    class RootComponentName():
        id = "idRootCompName"
        name = "Component Name"
        
    class MaterialThickness():
        id = "idMatThick"
        name = "Material Thickness"
        unit = default.unit
        default = 1
        
    class BoxWidth():
        id ="idBoxWidth"
        name = "Width"
        unit = default.unit
        default = 10
        
    class BoxLength():
        id = "idBoxLength"
        name = "Length"
        unit = default.unit
        default = 10
        
    class BoxHeight():
        id = "idBoxHeight"
        name = "Height"
        unit = default.unit
        default = 10
    