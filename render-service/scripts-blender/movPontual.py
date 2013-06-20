from utils02 import *
import Blender
from Blender import*
from Blender.Scene import Render
import math
import os
import commands
import subprocess as sub
import sys

#import time
#init = time.time()

def substr(str,origem, tamanho):
	return str[origem:tamanho+origem]

paramDir = sys.argv[7]
paramEsq = sys.argv[8]

libPoseMaoDireita = open("Libs/LibConfigMaoDir", "r")
libOritentacaoLadoDireito = open("Libs/LibOrientacaoDir", "r")
libPoseMaoEsquerda = open("Libs/LibConfigMaoEsq", "r")
libOritentacaoLadoEsquerdo = open("Libs/LibOrientacaoEsq", "r")
libPontoArticulacaoEsquerda = open("Libs/LibPontoArticulacaoEsq", "r")
listaPoseMaoDireita = libPoseMaoDireita.readlines();
listalibOritentacaoLadoDireito = libOritentacaoLadoDireito.readlines();
libPontoArticulacaoDireita = open("Libs/LibPontoArticulacaoDir", "r")
listalibPontoArticulacaoDireita = libPontoArticulacaoDireita.readlines();
listaPoseMaoEsquerda = libPoseMaoEsquerda.readlines();
listalibOritentacaoLadoEsquerdo  = libOritentacaoLadoEsquerdo.readlines();
listalibPontoArticulacaoEsquerda = libPontoArticulacaoEsquerda.readlines();
libExpressaoFacial = open("Libs/LibExpressaoFacial", "r")
listaExpressaoFacial = libExpressaoFacial.readlines();
libPosePadrao = open("Libs/LibPosePadrao", "r")
listaPosePadrao = libPosePadrao.readlines();

armadura = Blender.Object.Get('Armature.001');
pose = armadura.getPose()
print "#########################MOVIMENTO RETILINEO#########################"

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();
print parametrosDireita
arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();
print parametrosEsquerda
act = Armature.NLA.NewAction("ret")
act.setActive(armadura)

print "#########################CONFIGURACOES DA MAO DIREITA#########################"

configDir = parametrosDireita[0]
configDir = configDir[:-1]
print configDir

oriDir = parametrosDireita[1]
oriDir = oriDir[:-1]
print oriDir

paDir = parametrosDireita[2]
paDir = paDir[:-1]
print paDir

maoUtil = parametrosDireita[3]
maoUtil = maoUtil[:-1]
print maoUtil[:-1]

nomeSinal = parametrosDireita[4]
nomeSinal = nomeSinal[:-1]
print nomeSinal

idUsuario = parametrosDireita[5]
idUsuario = idUsuario[:-1]
print idUsuario

#sub.call(["rm", ""+paramDir])
os.remove( paramDir )

print "#########################POSE PADRÃO ESQUERDA E DIREITA#########################"

posePadrao = ["Pose_1", "Pose_2"]
for h in range(0, 2, 1):
	#Pose Padrao inicial
	print "Pose Padrão Inicial: " + str(posePadrao[h])
	for i in range(0 , len(listaPosePadrao), 1):
		if (listaPosePadrao[i].split()): 			
			if (listaPosePadrao[i].split()[0] == posePadrao[h]):  			
				for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
       					bone = pose.bones[listaPosePadrao[k+1].split()[0]]
       					bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])	
					bone.insertKey(armadura, 0, Object.Pose.LOC)
       					euler = bone.quat.toEuler()
       					euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
       					bone.quat = euler.toQuat()					
       					bone.insertKey(armadura, 0, Object.Pose.ROT)

#Configuracao de mao direita
param = [15, 18]
for u in range(0, 2, 1 ):
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configDir): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, param[u], Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, param[u], Object.Pose.ROT)

#Define a orientacao da mao direita
for u in range(0, 2, 1 ):
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, param[u], Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, param[u], Object.Pose.ROT)

#Ponto de articulacao da mao direita
for u in range(0, 2, 1 ):
	for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 			
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura, param[u], Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, param[u], Object.Pose.ROT)

if (maoUtil == 'duas'):
	print "############ CONFIGURACOES DA MAO ESQUERDA ############"
	configEsq = parametrosEsquerda[0]
	configEsq = configEsq[:-1]
	print configEsq

	oriEsq = parametrosEsquerda[1]
	oriEsq = oriEsq[:-1]
	print oriEsq

	paEsq = parametrosEsquerda[2]
	paEsq = paEsq[:-1]
	print paEsq

	expFacial = parametrosEsquerda[3]
	expFacial = expFacial[:-1]
	print expFacial
	#sub.call(["rm", ""+paramEsq])
        #rm( 'rf', paramEsq )
        os.remove( paramEsq )	

	#Config da mao esquerda
	for u in range(0, 2, 1 ):
		for i in range(0 , len(listaPoseMaoEsquerda), 1):
			if (listaPoseMaoEsquerda[i].split()):			
				if (listaPoseMaoEsquerda[i].split()[0] == configEsq): 
					for k in range(i , i+15, 1): #varrendo todos os ossos da mao
						bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
						bone.insertKey(armadura, param[u], Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, param[u], Object.Pose.ROT)

		#Orientacao da mao esquerda
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoEsquerdo[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])
					bone.insertKey(armadura, param[u], Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, param[u], Object.Pose.ROT)	

		#Ponto de articulacao da mao esquerda
		for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
			if (listalibPontoArticulacaoEsquerda[i].split()):
				if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
					for k in range(i , i+2, 1): 
	        				bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        				bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
						bone.insertKey(armadura, param[u], Object.Pose.LOC)
	        				euler = bone.quat.toEuler()
	        				euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        				bone.quat = euler.toQuat()
	        				bone.insertKey(armadura, param[u], Object.Pose.ROT)

else: 
	expFacial = parametrosEsquerda[1]
	expFacial = expFacial[:-1]
	print expFacial
	#sub.call(["rm", ""+paramEsq])
        #rm( 'rf', paramEsq )	
        os.remove( paramEsq )

endFrame = 20

expressaoFacial = ["Exp_9", expFacial, "Exp_9"]
for h in range(0, 3, 1):
	#Configurando expressão facial do sinal escolhida
	for i in range(0 , len(listaExpressaoFacial), 1):
		if (listaExpressaoFacial[i].split()): #Split em cada linha			
  			if (listaExpressaoFacial[i].split()[0] == expressaoFacial[h]):
  				#print listaExpressaoFacial[i].split()[0];
				for k in range(i , i+int(listaExpressaoFacial[i].split()[-1]), 1): 
        				bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
        				#print bone;
					bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
					bone.insertKey(armadura, h*(endFrame/2) + 1 + h*3, Object.Pose.LOC)
        				euler = bone.quat.toEuler()
        				euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
        				bone.quat = euler.toQuat()
        				bone.insertKey(armadura, h*(endFrame/2) + 1, Object.Pose.ROT)

# Key Frames Pose Padrão Inicial e Final ----------------------------------------------------------------
poseInicial = ["Pose_1", "Pose_2"]

for u in range(0, 2, 1 ):
	for i in range(0 , len(listaPosePadrao), 1):
		if (listaPosePadrao[i].split()): 			
  			if (listaPosePadrao[i].split()[0] == poseInicial[u]):  			
				for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
        				bone = pose.bones[listaPosePadrao[k+1].split()[0]]
        				bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])
					bone.insertKey(armadura, 1, Object.Pose.LOC)
        				euler = bone.quat.toEuler()
        				euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
        				bone.quat = euler.toQuat()
        				bone.insertKey(armadura, 1, Object.Pose.ROT)
				
					bone = pose.bones[listaPosePadrao[k+1].split()[0]]	
					bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])	
					bone.insertKey(armadura, endFrame + 20, Object.Pose.LOC)
        				euler = bone.quat.toEuler()
        				euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
        				bone.quat = euler.toQuat()
        				bone.insertKey(armadura, endFrame + 20, Object.Pose.ROT)



cena = Blender.Scene.GetCurrent()

cont = cena.getRenderingContext()
cont.imageSizeX(400)
cont.imageSizeY(400)
#cont.imageSizeX(200)
#cont.imageSizeY(200)
cont.enableShadow(0)
cont.enableRayTracing(0)
cont.enableEnvironmentMap(0)
cont.enablePanorama(0)
cont.enableRadiosityRender(0)
cont.enableMotionBlur(0)
cont.enableOversampling(0)

# threads e particionamento da imagem
cont.threads = 4
cont.xParts = 2
cont.yParts = 2

renderPath = cont.renderPath
cont.renderPath += "//" + nomeSinal + "_"
cont.sFrame = 1
cont.eFrame = endFrame + 15
cont.renderAnim()

print
print"Convertendo AVI em FLV usando ffmpeg"

num = endFrame + 15
if(num > 100):
	s = "0" + str(num);
else: 
	s = "00" + str(num);

print nomeSinal+"_0001_" + s + ".avi";

sub.call(["ffmpeg", "-y", "-i", cont.renderPath + "0001_" + s + ".avi", "-r", "24", "-vcodec", "libvpx", renderPath + "//" + nomeSinal + ".webm"])
sub.call(["rm", cont.renderPath + "0001_" + s + ".avi"])

print idUsuario + "**********************************************"

#final = time.time()
#diff = final - init
#print "Tempo total de execução: " + str(diff)
#print "Threads " + str(cont.threads)
#print "xPart " + str(cont.xParts) + " yPart " + str(cont.yParts)

Blender.Quit()
