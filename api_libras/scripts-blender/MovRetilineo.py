from utils02 import *
import Blender
from Blender import*
from Blender.Scene import Render
import math
import os
import commands
import subprocess as sub
import sys


def substr(str,origem, tamanho):
	return str[origem:tamanho+origem]

paramDir = sys.argv[5]
paramEsq = sys.argv[6]

libPoseMaoDireita = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibConfigMaoDir", "r")
libOritentacaoLadoDireito = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibOrientacaoDir", "r")
libPoseMaoEsquerda = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibConfigMaoEsq", "r")
libOritentacaoLadoEsquerdo = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibOrientacaoEsq", "r")
libPontoArticulacaoEsquerda = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibPontoArticulacaoEsq", "r")
listaPoseMaoDireita = libPoseMaoDireita.readlines();
listalibOritentacaoLadoDireito = libOritentacaoLadoDireito.readlines();
libPontoArticulacaoDireita = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibPontoArticulacaoDir", "r")
listalibPontoArticulacaoDireita = libPontoArticulacaoDireita.readlines();
listaPoseMaoEsquerda = libPoseMaoEsquerda.readlines();
listalibOritentacaoLadoEsquerdo  = libOritentacaoLadoEsquerdo.readlines();
listalibPontoArticulacaoEsquerda = libPontoArticulacaoEsquerda.readlines();
libExpressaoFacial = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibExpressaoFacial", "r")
listaExpressaoFacial = libExpressaoFacial.readlines();
libPosePadrao = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibPosePadrao", "r")
listaPosePadrao = libPosePadrao.readlines();

armadura = Blender.Object.Get('Armature.001');
pose = armadura.getPose()
print "#########################MOVIMENTO RETILINEO#########################"

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();
arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();

act = Armature.NLA.NewAction("ret")
act.setActive(armadura)


print#########################CONFIGURACOES DA MAO DIREITA#########################

configDirIni = parametrosDireita[0]
configDirIni = configDirIni[:-1]
print configDirIni

oriDirIni = parametrosDireita[1]
oriDirIni = oriDirIni[:-1]
print oriDirIni

paDirIni = parametrosDireita[2]
paDirIni = paDirIni[:-1]
print paDirIni

configDirFin = parametrosDireita[3]
configDirFin = configDirFin[:-1]
print configDirFin

oriDirFin = parametrosDireita[4]
oriDirFin = oriDirFin[:-1]
print oriDirFin

paDirFin = parametrosDireita[5]
paDirFin = paDirFin[:-1]
print paDirFin

flagRepDir = parametrosDireita[6]
flagRepDir = flagRepDir[:-1]
print flagRepDir

maoUtil = parametrosDireita[7]
maoUtil = maoUtil[:-1]
print maoUtil


nomeSinal = parametrosDireita[8]
nomeSinal = nomeSinal[:-1]
print nomeSinal

idUsuario = parametrosDireita[9]
idUsuario = idUsuario[:-1]
print idUsuario

if(flagRepDir == 'com-repeticao'):
	numVezes = 2
else:
	numVezes = 1

frame = 0

sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramDir])

print "#########################POSE PADRÃO ESQUERDA E DIREITA#########################"

#inserindo keyframes no frame 0 para pose padrao direita e esquerda
posePadrao = ["Pose_1", "Pose_2"]
print posePadrao
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

#variavel frame inicialmente em zero. keyframe inserido em frame + 15
#Configuracao da Mao Direita INICIAL - frame + 15
for p in range(0, numVezes,1):
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configDirIni): 
				for k in range(i , i+15, 1):
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura,frame + 15, Object.Pose.LOC) #frame 0 e 43. keyframe em 15 e 58
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					
					bone.insertKey(armadura,frame + 15, Object.Pose.ROT) #frame 0 e 43. keyframe em 15 e 58
 
	#Configuracao da Mao Direita INICIAL - frame + 18 - PERMANENCIA
	for p in range(0, numVezes,1):
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == configDirIni): 
					for k in range(i , i+15, 1): #varrendo todos os ossos da mao
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura,frame + 18, Object.Pose.LOC) #frame em 0 e 43. keyframe em 18 e 61
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
					
						bone.insertKey(armadura,frame + 18, Object.Pose.ROT) #frame em 0 e 43. keyframe em 18 e 61

#Configuracao de mao direita FINAL - frame + 40
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configDirFin): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura,frame + 40, Object.Pose.LOC) #frame em 0 e 43. keyframe em 40 e 83
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura,frame + 40, Object.Pose.ROT) #frame em 0 e 43. keyframe em 40 e 83

#Configuracao de mao direita FINAL - frame + 40 - PERMANENCIA
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configDirFin): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura,frame + 43, Object.Pose.LOC) #frame em 0 e 43. keyframe em 43 e 86
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura,frame + 43, Object.Pose.ROT) #frame em 0 e 43. keyframe em 43 e 86


#Configuracao da Orientacao da Mao Inicial - frame + 15
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDirIni):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura,frame + 15, Object.Pose.LOC) #frame em 0 e 43. keyframe em 15 e 58
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura,frame + 15, Object.Pose.ROT) #frame em 0 e 43. keyframe em 15 e 58

#Configuracao da Orientacao da Mao Inicial - frame + 18 - PERMANENCIA
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDirIni):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura,frame + 18, Object.Pose.LOC) #frame em 0 e 43. keyframe em 18 e 61
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura,frame + 18, Object.Pose.ROT) #frame em 0 e 43. keyframe em 18 e 61

#Configuracao da Orientacao da Mao Final - frame + 40
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDirFin):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, frame + 40, Object.Pose.LOC) #frame em 0 e 43. keyframe em 40 e 83
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura,frame + 40, Object.Pose.ROT) #frame em 0 e 43. keyframe em 40 e 83

#Configuracao da Orientacao da Mao Final - frame + 40 - PERMANENCIA
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDirFin):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, frame + 43, Object.Pose.LOC) #frame em 0 e 43. keyframe em 43 e 86
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura,frame + 43, Object.Pose.ROT) #frame em 0 e 43. keyframe em 43 e 86

#Configuracao do Ponto de Articulacao Direito INICIAL - frame + 15
	for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 		
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDirIni):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura,frame + 15, Object.Pose.LOC) #frame em 0 e 43. keyframe em 15 e 58
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura,frame + 15, Object.Pose.ROT) #frame em 0 e 43. keyframe em 15 e 58

#Configuracao do Ponto de Articulacao Direito INICIAL - frame + 18 - PERMANENCIA
	for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 		
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDirIni):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura,frame + 18, Object.Pose.LOC) #frame em 0 e 43. keyframe em 18 e 61
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura,frame + 18, Object.Pose.ROT) #frame em 0 e 43. keyframe em 18 e 61

#Configuracao do Ponto de Articulacao Direito FINAL - frame + 40
	for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 		
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDirFin):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura,frame + 40, Object.Pose.LOC) #frame em 0 e 43. keyframe em 40 e 83
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, frame + 40, Object.Pose.ROT) #frame em 0 e 43. keyframe em 40 e 83

#Configuracao do Ponto de Articulacao Direito FINAL - frame + 43 - PERMANENCIA
	for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 		
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDirFin):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura,frame + 43, Object.Pose.LOC) #frame em 0 e 43. keyframe em 43 e 86
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, frame + 43, Object.Pose.ROT) #frame em 0 e 43. keyframe em 43 e 86

	frame += 43


if (numVezes == 1):
	frame = 43
if(numVezes == 2):
	frame = 86	

print "numVezes = " + str(numVezes)		
print "Frame == " + str(frame)			
print "Maos Utilizadas no sinal: " + str(maoUtil)
#--------------------------------------------------------------------------------------------------
#Configurando os keyframes do lado esquerdo
if (maoUtil == 'duas'):
	print "############ CONFIGURACOES DA MAO ESQUERDA ############"
	configEsqIni = parametrosEsquerda[0]
	configEsqIni = configEsqIni[:-1]
	print configEsqIni

	oriEsqIni = parametrosEsquerda[1]
	oriEsqIni = oriEsqIni[:-1]
	print oriEsqIni

	paEsqIni = parametrosEsquerda[2]
	paEsqIni = paEsqIni[:-1]
	print paEsqIni

	configEsqFin = parametrosEsquerda[3]
	configEsqFin = configEsqFin[:-1]
	print configEsqFin

	oriEsqFin = parametrosEsquerda[4]
	oriEsqFin = oriEsqFin[:-1]
	print oriEsqFin
	
	paEsqFin = parametrosEsquerda[5]
	paEsqFin = paEsqFin[:-1]
	print paEsqFin
	
	flagRepEsq = parametrosEsquerda[6]
	flagRepEsq = flagRepEsq[:-1]
	print flagRepEsq
	
	expFacial = parametrosEsquerda[7]
	expFacial = expFacial[:-1]
	print expFacial


	if(flagRepEsq == 'com-repeticao'):
		numVezesEsq = 2
	else:
		numVezesEsq = 1
	
	sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramEsq])	


	frameEsq = 0
	for p in range(0, numVezesEsq,1):
		#Configuracao de mao esquerda inicial
		for i in range(0 , len(listaPoseMaoEsquerda), 1):
			if (listaPoseMaoEsquerda[i].split()):
				if (listaPoseMaoEsquerda[i].split()[0] == configEsqIni): 
					for k in range(i , i+15, 1): #varrendo todos os ossos da mao
						bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
						bone.insertKey(armadura,frameEsq + 15, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 15, Object.Pose.ROT)

		for i in range(0 , len(listaPoseMaoEsquerda), 1):
			if (listaPoseMaoEsquerda[i].split()):
				if (listaPoseMaoEsquerda[i].split()[0] == configEsqIni): 
					for k in range(i , i+15, 1): #varrendo todos os ossos da mao
						bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
						bone.insertKey(armadura,frameEsq + 18, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 18, Object.Pose.ROT)


		#Configuracao de mao esquerda final
		for i in range(0 , len(listaPoseMaoEsquerda), 1):
			if (listaPoseMaoEsquerda[i].split()):
				if (listaPoseMaoEsquerda[i].split()[0] == configEsqFin): 
					for k in range(i , i+15, 1): #varrendo todos os ossos da mao
						bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
						bone.insertKey(armadura,frameEsq + 40, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 40, Object.Pose.ROT)

		#Configuracao de mao esquerda final
		for i in range(0 , len(listaPoseMaoEsquerda), 1):
			if (listaPoseMaoEsquerda[i].split()):
				if (listaPoseMaoEsquerda[i].split()[0] == configEsqFin): 
					for k in range(i , i+15, 1): #varrendo todos os ossos da mao
						bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
						bone.insertKey(armadura,frameEsq + 43, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 43, Object.Pose.ROT)


		#Define a orientacao da mao esquerda incial
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoEsquerdo[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsqIni):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura,frameEsq + 15, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 15, Object.Pose.ROT)

		#Define a orientacao da mao esquerda incial
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoEsquerdo[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsqIni):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura,frameEsq + 18, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 18, Object.Pose.ROT)

		#Define a orientacao da mao esquerda final
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoDireito[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsqFin):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura,frameEsq + 40, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 40, Object.Pose.ROT)

		#Define a orientacao da mao esquerda final
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoDireito[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsqFin):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura,frameEsq + 43, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura,frameEsq + 43, Object.Pose.ROT)

		#Ponto de articulacao da mao esquerda inicial
		for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
			if (listalibPontoArticulacaoEsquerda[i].split()):
				if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsqIni):
					for k in range(i , i+2, 1): 
	        				bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        				bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
						bone.insertKey(armadura,frameEsq + 15, Object.Pose.LOC)
	        				euler = bone.quat.toEuler()
	        				euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        				bone.quat = euler.toQuat()
	        				bone.insertKey(armadura,frameEsq + 15, Object.Pose.ROT)

		#Ponto de articulacao da mao esquerda inicial
		for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
			if (listalibPontoArticulacaoEsquerda[i].split()):
				if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsqIni):
					for k in range(i , i+2, 1): 
	        				bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        				bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
						bone.insertKey(armadura,frameEsq + 18, Object.Pose.LOC)
	        				euler = bone.quat.toEuler()
	        				euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        				bone.quat = euler.toQuat()
	        				bone.insertKey(armadura,frameEsq + 18, Object.Pose.ROT)

		#Ponto de articulacao da mao esquerda final
		for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
			if (listalibPontoArticulacaoEsquerda[i].split()):
				if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsqFin):
					for k in range(i , i+2, 1): 
	        				bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        				bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
						bone.insertKey(armadura,frameEsq + 40, Object.Pose.LOC)
	        				euler = bone.quat.toEuler()
	        				euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        				bone.quat = euler.toQuat()
	        				bone.insertKey(armadura,frameEsq + 40, Object.Pose.ROT)

		#Ponto de articulacao da mao esquerda final
		for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
			if (listalibPontoArticulacaoEsquerda[i].split()):
				if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsqFin):
					for k in range(i , i+2, 1): 
	        				bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        				bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
						bone.insertKey(armadura,frameEsq + 43, Object.Pose.LOC)
	        				euler = bone.quat.toEuler()
	        				euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        				bone.quat = euler.toQuat()
	        				bone.insertKey(armadura,frameEsq + 43, Object.Pose.ROT)
			
		frameEsq += 43

	if (numVezesEsq == 1):
		frameEsq = 43
	if(numVezesEsq == 2):
		frameEsq = 86	
	
	print "FrameEsq == " + str(frameEsq)		


#***************MOVIMENTO COM APENAS UMA MAO***************
else: 

	expFacial = parametrosEsquerda[1]
	expFacial = expFacial[:-1]
	print expFacial
	sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramEsq])


endFrame = 0;

if(maoUtil == "uma"):
	if(numVezes == 1):
		endFrame = 43;
	else: #numVezes = 2
		endFrame = 86;

else: #maoUtil = duas
	if(frame > frameEsq):
		endFrame = frame;
		print "frame: " + str(frame)
		print "frameEsq: " + str(frameEsq)
		print "endFrame: " + str(endFrame)
	else:
		endFrame = frameEsq;
		print "frame: " + str(frame)
		print "frameEsq: " + str(frameEsq)
		print "endFrame: " + str(endFrame)

posePadrao = ["Pose_1", "Pose_2"]
for h in range(0, 2, 1):
	#Pose Padrao inicial
	if(posePadrao[h] == "Pose_1"):
		endFrame = frame
	else:
		if(maoUtil == "uma"):
			endFrame = frame
		else:
			endFrame = frameEsq
	for i in range(0 , len(listaPosePadrao), 1):
		if (listaPosePadrao[i].split()): 			
			if (listaPosePadrao[i].split()[0] == posePadrao[h]):  				
				for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
       					bone = pose.bones[listaPosePadrao[k+1].split()[0]]
       					bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])	
					bone.insertKey(armadura, endFrame + 15, Object.Pose.LOC)
       					euler = bone.quat.toEuler()
       					euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
       					bone.quat = euler.toQuat()
       					bone.insertKey(armadura, endFrame + 15, Object.Pose.ROT)

#Corrigindo rotacoes
fixRots(0) 
fixRots(1)

print "endFrame = " + str(endFrame)

expressaoFacial = ["Exp_9", expFacial, "Exp_9"]
for h in range(0, 3, 1):
	#Configurando expressão facial do sinal escolhida
	for i in range(0 , len(listaExpressaoFacial), 1):
		if (listaExpressaoFacial[i].split()): #Split em cada linha			
  			if (listaExpressaoFacial[i].split()[0] == expressaoFacial[h]):
  				print listaExpressaoFacial[i].split()[0];
				print str(listaExpressaoFacial[i].split()[-1])
				for k in range(i , i+int(listaExpressaoFacial[i].split()[-1]), 1): 
        				bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
        				#print bone;
					bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
					bone.insertKey(armadura, h*(endFrame/2) + 1 + h*3, Object.Pose.LOC)
        				euler = bone.quat.toEuler()
        				euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
        				bone.quat = euler.toQuat()




# RENDER ------------------------------------------------------------------------------------------
cena = Blender.Scene.GetCurrent()
cont = cena.getRenderingContext()
cont.renderPath = "//"+nomeSinal+"_"
cont.sFrame = 0
cont.eFrame = endFrame + 25
cont.renderAnim()

num = endFrame + 25
if(num > 100):
	s = "0" + str(num);
else: 
	s = "00" + str(num);


#sub.call(["ffmpeg", "-i", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"_0001_"+s+".avi", "-b", "2028k", "-s", "640x480", "-r", "30", "-acodec", "copy", "home/gtaaas_web/public/uploads/files/" + idUsuario + "/" + nomeSinal+".flv"])

#sub.call(["mv", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"_0001_"+s+".avi", "/home/gtaaas/gtaaas_web/public/uploads/files/" + idUsuario + "/" + nomeSinal+".avi"])

sub.call(["ffmpeg", "-i", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"_0001_"+s+".avi", "-b", "2028k", "-s", "640x480", "-r", "30", "-acodec", "copy",  nomeSinal+".flv"])

print idUsuario + "**********************************************"
sub.call(["mv", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+".flv", "/home/gtaaas/gtaaas_web/public/uploads/files/"+idUsuario + "/"])

Blender.Quit()





























