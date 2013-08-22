import Blender as b
from Blender import *
import math as m

bones = ["BnMao.R","BnMao.L"]

def flip(frame, lado):
	print "flipou Frame: " + str(frame) + "  BONE: " + str(bones[lado])
	for i in range(0, 4, 1):
		b.Object.Get("Armature.001").getAction().getChannelIpo(bones[lado]).getCurves()[i][frame]*=-1
	
def fixRots(lado):
	keyFrames = b.Object.Get("Armature.001").getAction().getFrameNumbers()
	print keyFrames
	rotFrames = [[]]
	status = [True]*(len(keyFrames)+1)
	for i in range(0,len(keyFrames),1):
		b.Set('curframe',keyFrames[i])
		rotFrames[-1] = b.Object.Get("Armature.001").getPose().bones[bones[lado]].quat.toEuler()
		rotFrames.append( [] )
	rotFrames.remove([])

	for k in range(1, len(keyFrames), 1):
		for i in range(0, 3, 1):
			if (m.fabs(rotFrames[k][i] - rotFrames[k-1][i])) > 180 :
				status[k] = False

	print status[0:len(status)-1]

	for k in range(1, len(keyFrames), 1):
		if status[k] == False:
			flip(keyFrames[k], lado)
			if status[k+1] == True:
				status[k+1] = False
			else:
				status[k+1] = True

	print status[0:len(status)-1]
