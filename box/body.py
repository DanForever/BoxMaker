
import adsk.core

class Body():
	def __init__( self ):
		self.parent = None
		
	def Extrude( self, parent, sketch, materialThickness ):
		self.parent = parent
		
		# Create an extrusion input for the profile.
		features = self.parent.features
		extrudes = features.extrudeFeatures
		extInput = extrudes.createInput( sketch.GetProfilesToExtrude(), adsk.fusion.FeatureOperations.NewBodyFeatureOperation )
		
		# Define the extent of the extrusion
		distance = adsk.core.ValueInput.createByReal( materialThickness )
		extInput.setDistanceExtent( False, distance )
		
		# Create the extrusion.
		extrudes.add( extInput )