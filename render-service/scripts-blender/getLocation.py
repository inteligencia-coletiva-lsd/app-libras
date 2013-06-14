# -*- coding: utf-8 -*-
import Blender
from Blender import *

arm = Blender.Object.Get("Armature.001")

act = arm.getAction()
pose = arm.getPose()

bones = act.getChannelNames()

frames = act.getFrameNumbers()

out = str(act.name)

arq = file('testandoLibExp','w')

for k in range(1 , len(frames) + 1):
  Blender.Set('curframe',k)
  print "Pa_" + str(k)
  for i in range(0 , len(bones)):	
	bone = pose.bones[bones[i]]
	print str(bone.name) + "  loc " + str(bone.loc) + "  rot " + str(bone.quat.toEuler())
arq.close()

print "Lib: " + str(act.name)
print "Num de Frames: " + str(len(frames))

Blender.Quit()
