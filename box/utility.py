
import math

import adsk.core

def CreateComponent( parent, name ):
	# Create Component
	identityTransform = adsk.core.Matrix3D.create()
	occurrence = parent.occurrences.addNewComponent( identityTransform )

	component = occurrence.component
	component.name = name

	return component

def IsFloatInList( float, list ):
	for f in list:
		if math.isclose( float, f ):
			return True
	return False

def DoXYPairsMatch( xy1, xy2 ):
	for i in range( 2 ):
		if not math.isclose( xy1[ i ], xy2[ i ] ):
			return False
	return True

def IsXYInList( xy, list ):
	for xy2 in list:
		if DoXYPairsMatch( xy, xy2 ):
			return True
		
	return False
