import math

import adsk.core

def FindCurvesOnAxis( occurrence, axis ):
	edges = []
	
	for iB in range( occurrence.bRepBodies.count ):
		body = occurrence.bRepBodies.item( iB )
		
		for iE in range( body.edges.count ):
			edge = body.edges.item( iE )
			
			xIsClose = math.isclose( edge.startVertex.geometry.x, edge.endVertex.geometry.x )
			yIsClose = math.isclose( edge.startVertex.geometry.y, edge.endVertex.geometry.y )
			zIsClose = math.isclose( edge.startVertex.geometry.z, edge.endVertex.geometry.z )

			x = ( axis.x > 0 and not xIsClose ) or ( axis.x == 0 and xIsClose )
			y = ( axis.y > 0 and not yIsClose ) or ( axis.y == 0 and yIsClose )
			z = ( axis.z > 0 and not zIsClose ) or ( axis.z == 0 and zIsClose )
			
			if x and y and z:
				edges.append( edge )

	return edges

def CalcMidPoint( edge ):
	x = ( edge.startVertex.geometry.x + edge.endVertex.geometry.x ) / 2
	y = ( edge.startVertex.geometry.y + edge.endVertex.geometry.y ) / 2
	z = ( edge.startVertex.geometry.z + edge.endVertex.geometry.z ) / 2
	
	return x, y, z
	
def AreMidPointsEqual( a, b ):
	midA = adsk.core.Point3D.create( *CalcMidPoint( a ) )
	midB = adsk.core.Point3D.create( *CalcMidPoint( b ) )
	
	return midA.isEqualTo( midB )

def CalculateEdgeDirection( edge ):
	return edge.startVertex.geometry.vectorTo( edge.endVertex.geometry )

def AreEdgesInTheSameDirection( a, b ):
	dirA = CalculateEdgeDirection( a )
	dirB = CalculateEdgeDirection( b )
	
	dirA.normalize()
	dirB.normalize()
	
	dp = dirA.dotProduct( dirB )
	
	return math.isclose( 1, dp )

def VectorToString( vector ):
	return "X:{0} Y:{1} Z:{2}".format( vector.x, vector.y, vector.z )

def EdgeToString( edge ):
	output  = "Start: " + VectorToString( edge.startVertex.geometry )
	output += "\n"
	output += "End  : " + VectorToString( edge.endVertex.geometry )
	
	return output

def Join( parent, partA, partB, axis, offset = 0 ):
	
	print( "Joining {} -> {}".format( partA.occurrence.name, partB.occurrence.name ) )
	
	occurrenceA = partA.occurrence
	occurrenceB = partB.occurrence
	
	edgesA = FindCurvesOnAxis( occurrenceA, axis )
	edgesB = FindCurvesOnAxis( occurrenceB, axis )
	
	print( "Found {} edges on {} as potential joint targets".format( len( edgesA ), partA.occurrence.name ) )
	print( "Found {} edges on {} as potential joint targets".format( len( edgesB ), partB.occurrence.name ) )
	
	for edgeA in edgesA:
		for edgeB in edgesB:
			
			#print \
			#(
			#	"Comparing {} {}->{} against {} {}->{}".format
			#	(
			#		partA.occurrence.name,
			#		VectorToString( edgeA.startVertex.geometry ),
			#		VectorToString( edgeA.endVertex.geometry ),
			#		partB.occurrence.name,
			#		VectorToString( edgeB.startVertex.geometry ),
			#		VectorToString( edgeB.endVertex.geometry ),
			#	)
			#)
			
			if AreMidPointsEqual( edgeA, edgeB ):
				
				joinA = adsk.fusion.JointGeometry.createByCurve( edgeA, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint )
				joinB = adsk.fusion.JointGeometry.createByCurve( edgeB, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint )
				
				print( EdgeToString( edgeA ) )
				print( EdgeToString( edgeB ) )
				
				jointInput = parent.joints.createInput( joinA, joinB )
				jointInput.offset = adsk.core.ValueInput.createByReal( offset )
				jointInput.isFlipped = not AreEdgesInTheSameDirection( edgeA, edgeB )
				jointInput.setAsRigidJointMotion()
				joint = parent.joints.add( jointInput )
				
				joint.name = "{} -> {}".format( partA.occurrence.name, partB.occurrence.name )
				
				return