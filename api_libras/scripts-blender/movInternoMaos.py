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

libPoseMaoDireita = open("Libs/LibConfigMaoDir", "r")
libOritentacaoLadoDireito = open("Libs/LibOrientacaoDir", "r")
libPontoArticulacaoDireita = open("Libs/LibPontoArticulacaoDir", "r")

libPoseMaoEsquerda = open("Libs/LibConfigMaoEsq", "r")
libOritentacaoLadoEsquerdo = open("Libs/LibOrientacaoEsq", "r")
libPontoArticulacaoEsquerda = open("Libs/LibPontoArticulacaoEsq", "r")

listaPoseMaoDireita = libPoseMaoDireita.readlines();
listalibOritentacaoLadoDireito = libOritentacaoLadoDireito.readlines();
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

poseb = pose.bones['ik_FK.R']
poseb1 = pose.bones['ik_FK.L']

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();
arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();

act = Armature.NLA.NewAction("Circular")
act.setActive(armadura)

print "############ CONFIGURACOES DA MAO DIREITA ############"

oriDir = parametrosDireita[0]
oriDir = oriDir[:-1]
print oriDir

paDir = parametrosDireita[1]
paDir = paDir[:-1]
print paDir

tipo1Dir = parametrosDireita[2] #Abertura ou Fechamento da mão
tipo1Dir = tipo1Dir[:-1]
print tipo1Dir

tipo2Dir = parametrosDireita[3] #Abertura Simultanea dos dedos ou Gradativa
tipo2Dir = tipo2Dir[:-1]
print tipo2Dir

if(tipo2Dir == "simultanea"):
	expFacial = parametrosDireita[4]
	expFacial = expFacial[:-1]
	print expFacial

	nomeSinal = parametrosDireita[5]
	nomeSinal = nomeSinal[:-1]
	print nomeSinal

	maosUtilizadas = parametrosDireita[6] 
	maosUtilizadas = maosUtilizadas[:-1]
	print maosUtilizadas

if(tipo2Dir == "gradativa"):
	direcaoDir = parametrosDireita[4]
	direcaoDir = direcaoDir[:-1]
	print direcaoDir

	expFacial = parametrosDireita[5]
	expFacial = expFacial[:-1]
	print expFacial

	nomeSinal = parametrosDireita[6]
	nomeSinal = nomeSinal[:-1]
	print nomeSinal

	maosUtilizadas = parametrosDireita[7] 
	maosUtilizadas = maosUtilizadas[:-1]
	print maosUtilizadas

#Pose Padrao inicial
for i in range(0 , len(listaPosePadrao), 1):
	if (listaPosePadrao[i].split()): 			
		if (listaPosePadrao[i].split()[0] == "Pose_1"):  			
			for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
       				bone = pose.bones[listaPosePadrao[k+1].split()[0]]
       				bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])
				bone.insertKey(armadura, 1, Object.Pose.LOC)
       				euler = bone.quat.toEuler()
       				euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
       				bone.quat = euler.toQuat()
       				bone.insertKey(armadura, 1, Object.Pose.ROT)

#Define a orientacao da mao direita inicial
for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
	if (listalibOritentacaoLadoDireito[i].split()):
		if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
			for k in range(i , i+2, 1):	
				bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
				bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
				bone.insertKey(armadura, 17, Object.Pose.LOC)
				euler = bone.quat.toEuler()					
				euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, 17, Object.Pose.ROT)

#Ponto de articulacao da mao direita inicial
for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
	if (listalibPontoArticulacaoDireita[i].split()): 			
  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
			for k in range(i , i+2, 1): 
        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
				bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
				bone.insertKey(armadura, 17, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 17, Object.Pose.ROT)

if(tipo1Dir == "fechamento"):
	if((tipo2Dir == "simultanea") or (tipo2Dir == "simultaneo")):
		#Configuracao de mao direita inicial
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == "conf_59"): #MAO ABERTA
					for k in range(i , i+15, 1): 
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura, 17, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 17, Object.Pose.ROT)

		#Configuracao de mao direita final
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO FECHADA
					for k in range(i , i+15, 1): 
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura, 22, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 22, Object.Pose.ROT)

		#Configuracao de mao direita final(permanencia)
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO FECHADA
					for k in range(i , i+15, 1): 
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura, 27, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 27, Object.Pose.ROT)

		#Define a orientacao da mao direita final
		for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
			if (listalibOritentacaoLadoDireito[i].split()):
				if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
						bone.insertKey(armadura, 22, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 22, Object.Pose.ROT)

		#Define a orientacao da mao direita final(permanencia)
		for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
			if (listalibOritentacaoLadoDireito[i].split()):
				if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
						bone.insertKey(armadura, 27, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 27, Object.Pose.ROT)

		#Ponto de articulacao da mao direita final
		for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
			if (listalibPontoArticulacaoDireita[i].split()): 			
  				if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
					for k in range(i , i+2, 1): 
        					bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
						bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
						bone.insertKey(armadura, 22, Object.Pose.LOC)
        					euler = bone.quat.toEuler()
        					euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        					bone.quat = euler.toQuat()
        					bone.insertKey(armadura, 22, Object.Pose.ROT)

		#Ponto de articulacao da mao direita final(permanencia)
		for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
			if (listalibPontoArticulacaoDireita[i].split()): 			
  				if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
					for k in range(i , i+2, 1): 
        					bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
						bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
						bone.insertKey(armadura, 27, Object.Pose.LOC)
        					euler = bone.quat.toEuler()
        					euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        					bone.quat = euler.toQuat()
        					bone.insertKey(armadura, 27, Object.Pose.ROT)

		endFrame = 27
		print "EndFrame = " + str(endFrame);
	if((tipo2Dir == "gradativa") or (tipo2Dir == "gradativo")):
		if(direcaoDir == "polegar-minimo"):
			#Configuracao de mao direita inicial
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_60"): #MAO FECHADA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
							bone.insertKey(armadura, 17, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 17, Object.Pose.ROT)
			#Configuracao de mao direita final
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 20, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 20, Object.Pose.ROT)
							
							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.011") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.012") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.003")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 23, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 23, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 26, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 26, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 29, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 29, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							else:#DO NOTHING
								print "Erro. Ln 397."
								sys.exit(1)
			
			#Configuracao de mao direita final(permanencia)					
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							
							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.011") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.012") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.003")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							else:#DO NOTHING
								print "Erro. Ln 449."	
			
			#Define a orientacao da mao direita final
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Define a orientacao da mao direita final(permanencia)
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final(permanencia)
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)
			endFrame = 32

			print "EndFrame = " + str(endFrame);
			
		if(direcaoDir == "minimo-polegar"):
			print "Direcao Dir " + direcaoDir
			#Configuracao de mao direita inicial
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_60"): #MAO FECHADA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
							bone.insertKey(armadura, 17, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 17, Object.Pose.ROT)
			#Configuracao de mao direita final
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 20, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 20, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 23, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 23, Object.Pose.ROT)
							
							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 26, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 26, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.011") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.012") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.003")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 29, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 29, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							else:#DO NOTHING
								print "Erro. Ln 397."
			
			#Configuracao de mao direita final(permanencia)					
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO ABERTA
						for k in range(i , i+15, 1): 

							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							else:#DO NOTHING
								print "Erro. Ln 449."	
			
			#Define a orientacao da mao direita final
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Define a orientacao da mao direita final(permanencia)
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final(permanencia)
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			endFrame = 32

			print "EndFrame = " + str(endFrame);


if(tipo1Dir == "abertura"):
	if((tipo2Dir == "simultanea") or (tipo2Dir == "simultaneo")):
		#Configuracao de mao direita inicial
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO FECHADA
					for k in range(i , i+15, 1): 
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura, 17, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 17, Object.Pose.ROT)

		#Configuracao de mao direita final
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == "conf_59"): #MAO ABERTA
					for k in range(i , i+15, 1): 
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura, 22, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 22, Object.Pose.ROT)

		#Configuracao de mao direita final(permanencia)
		for i in range(0 , len(listaPoseMaoDireita), 1):
			if (listaPoseMaoDireita[i].split()):
				if (listaPoseMaoDireita[i].split()[0] == "conf_59"): #MAO ABERTA
					for k in range(i , i+15, 1): 
						bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
						bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
						bone.insertKey(armadura, 27, Object.Pose.LOC)
						euler = bone.quat.toEuler()
						euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 27, Object.Pose.ROT)

		#Define a orientacao da mao direita final
		for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
			if (listalibOritentacaoLadoDireito[i].split()):
				if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
						bone.insertKey(armadura, 22, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 22, Object.Pose.ROT)

		#Define a orientacao da mao direita final(permanencia)
		for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
			if (listalibOritentacaoLadoDireito[i].split()):
				if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
						bone.insertKey(armadura, 27, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 27, Object.Pose.ROT)

		#Ponto de articulacao da mao direita final
		for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
			if (listalibPontoArticulacaoDireita[i].split()): 			
  				if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
					for k in range(i , i+2, 1): 
        					bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
						bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
						bone.insertKey(armadura, 22, Object.Pose.LOC)
        					euler = bone.quat.toEuler()
        					euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        					bone.quat = euler.toQuat()
        					bone.insertKey(armadura, 22, Object.Pose.ROT)

		#Ponto de articulacao da mao direita final(permanencia)
		for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
			if (listalibPontoArticulacaoDireita[i].split()): 			
  				if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
					for k in range(i , i+2, 1): 
        					bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
						bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
						bone.insertKey(armadura, 27, Object.Pose.LOC)
        					euler = bone.quat.toEuler()
        					euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        					bone.quat = euler.toQuat()
        					bone.insertKey(armadura, 27, Object.Pose.ROT)

		endFrame = 27

		print "EndFrame = " + str(endFrame);

	if((tipo2Dir == "gradativa") or (tipo2Dir == "gradativo")):
		if(direcaoDir == "polegar-minimo"):
			#Configuracao de mao direita inicial
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO FECHADA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
							bone.insertKey(armadura, 17, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 17, Object.Pose.ROT)
			#Configuracao de mao direita final
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_60"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 20, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 20, Object.Pose.ROT)
							
							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.011") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.012") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.003")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 23, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 23, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 26, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 26, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 29, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 29, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							else:#DO NOTHING
								print "Erro. Ln 397."
			
			#Configuracao de mao direita final(permanencia)					
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_60"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							
							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.011") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.012") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.003")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							else:#DO NOTHING
								print "Erro. Ln 449."	
			
			#Define a orientacao da mao direita final
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Define a orientacao da mao direita final(permanencia)
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final(permanencia)
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			endFrame = 32

			print "EndFrame = " + str(endFrame);

			
		if(direcaoDir == "minimo-polegar"):
			print "Direcao Dir " + direcaoDir
			#Configuracao de mao direita inicial
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_1"): #MAO FECHADA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
							bone.insertKey(armadura, 17, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 17, Object.Pose.ROT)
			#Configuracao de mao direita final
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_60"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 20, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 20, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 23, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 23, Object.Pose.ROT)
							
							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 26, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 26, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.011") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.012") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.003")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 29, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 29, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)
							else:#DO NOTHING
								print "Erro. Ln 397."
			
			#Configuracao de mao direita final(permanencia)					
			for i in range(0 , len(listaPoseMaoDireita), 1):
				if (listaPoseMaoDireita[i].split()):
					if (listaPoseMaoDireita[i].split()[0] == "conf_60"): #MAO ABERTA
						for k in range(i , i+15, 1): 

							if((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.005") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.006") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.007") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.008") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.001")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.009") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.010") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.002")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							elif((listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.013") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.014") or (listaPoseMaoDireita[k+1].split()[0] == "BnDedo.1.R.004")):
								bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

							else:#DO NOTHING
								print "Erro. Ln 449."	

			
			#Define a orientacao da mao direita final
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Define a orientacao da mao direita final(permanencia)
			for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
				if (listalibOritentacaoLadoDireito[i].split()):
					if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
							bone.insertKey(armadura, 32, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			#Ponto de articulacao da mao direita final(permanencia)
			for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
				if (listalibPontoArticulacaoDireita[i].split()): 			
  					if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
							bone.insertKey(armadura, 32, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 32, Object.Pose.ROT)

			endFrame = 32

			print "EndFrame = " + str(endFrame);

if(maosUtilizadas == "duas"):
	oriEsq = parametrosEsquerda[0]
	oriEsq = oriEsq[:-1]
	print oriEsq

	paEsq = parametrosEsquerda[1]
	paEsq = paEsq[:-1]
	print paEsq

	tipo1Esq = parametrosEsquerda[2] #Abertura ou Fechamento da mão
	tipo1Esq = tipo1Esq[:-1]
	print tipo1Esq

	tipo2Esq = parametrosEsquerda[3] #Abertura Simultanea dos dedos ou Gradativa
	tipo2Esq = tipo2Esq[:-1]
	print tipo2Esq
	
	if(tipo2Esq == "gradativa"):
		direcaoEsq = parametrosEsquerda[4]
		direcaoEsq = direcaoEsq[:-1]
		print direcaoEsq

	#Pose Padrao inicial LEFT
	for i in range(0 , len(listaPosePadrao), 1):
		if (listaPosePadrao[i].split()): 			
			if (listaPosePadrao[i].split()[0] == "Pose_2"):  			
				for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
       					bone = pose.bones[listaPosePadrao[k+1].split()[0]]
       					bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])
					bone.insertKey(armadura, 1, Object.Pose.LOC)
       					euler = bone.quat.toEuler()
       					euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
       					bone.quat = euler.toQuat()
       					bone.insertKey(armadura, 1, Object.Pose.ROT)

	#Define a orientacao da mao Esquerda inicial
	for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
		if (listalibOritentacaoLadoEsquerdo[i].split()):
			if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
					bone.insertKey(armadura, 17, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 17, Object.Pose.ROT)

	#Ponto de articulacao da mao Esquerda inicial
	for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
		if (listalibPontoArticulacaoEsquerda[i].split()): 			
  			if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
				for k in range(i , i+2, 1): 
        				bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 17, Object.Pose.LOC)
        				euler = bone.quat.toEuler()
        				euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        				bone.quat = euler.toQuat()
        				bone.insertKey(armadura, 17, Object.Pose.ROT)

	if(tipo1Esq == "fechamento"):
		if((tipo2Esq == "simultanea") or (tipo2Esq == "simultaneo")):
			#Configuracao de mao Esquerda inicial
			for i in range(0 , len(listaPoseMaoEsquerda), 1):
				if (listaPoseMaoEsquerda[i].split()):
					if (listaPoseMaoEsquerda[i].split()[0] == "conf_59"): #MAO ABERTA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
							bone.insertKey(armadura, 17, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 17, Object.Pose.ROT)

			#Configuracao de mao Esquerda final
			for i in range(0 , len(listaPoseMaoEsquerda), 1):
				if (listaPoseMaoEsquerda[i].split()):
					if (listaPoseMaoEsquerda[i].split()[0] == "conf_1"): #MAO FECHADA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
							bone.insertKey(armadura, 22, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 22, Object.Pose.ROT)

			#Configuracao de mao Esquerda final(permanencia)
			for i in range(0 , len(listaPoseMaoEsquerda), 1):
				if (listaPoseMaoEsquerda[i].split()):
					if (listaPoseMaoEsquerda[i].split()[0] == "conf_1"): #MAO FECHADA
						for k in range(i , i+15, 1): 
							bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
							bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
							bone.insertKey(armadura, 27, Object.Pose.LOC)
							euler = bone.quat.toEuler()
							euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 27, Object.Pose.ROT)

			#Define a orientacao da mao Esquerda final
			for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
				if (listalibOritentacaoLadoEsquerdo[i].split()):
					if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
							bone.insertKey(armadura, 22, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 22, Object.Pose.ROT)

			#Define a orientacao da mao Esquerda final(permanencia)
			for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
				if (listalibOritentacaoLadoEsquerdo[i].split()):
					if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
						for k in range(i , i+2, 1):	
							bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
							bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
							bone.insertKey(armadura, 27, Object.Pose.LOC)
							euler = bone.quat.toEuler()					
							euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
							bone.quat = euler.toQuat()
							bone.insertKey(armadura, 27, Object.Pose.ROT)

			#Ponto de articulacao da mao Esquerda final
			for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
				if (listalibPontoArticulacaoEsquerda[i].split()): 			
  					if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
							bone.insertKey(armadura, 22, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 22, Object.Pose.ROT)

			#Ponto de articulacao da mao Esquerda final(permanencia)
			for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
				if (listalibPontoArticulacaoEsquerda[i].split()): 			
  					if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
						for k in range(i , i+2, 1): 
        						bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
							bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
							bone.insertKey(armadura, 27, Object.Pose.LOC)
        						euler = bone.quat.toEuler()
        						euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        						bone.quat = euler.toQuat()
        						bone.insertKey(armadura, 27, Object.Pose.ROT)

			endFrame = 27
			print "EndFrame = " + str(endFrame);
		if((tipo2Esq == "gradativa") or (tipo2Esq == "gradativo")):
			if(direcaoEsq == "polegar-minimo"):
				#Configuracao de mao Esquerda inicial
				for i in range(0 , len(listaPoseMaoEsquerda), 1):
					if (listaPoseMaoEsquerda[i].split()):
						if (listaPoseMaoEsquerda[i].split()[0] == "conf_60"): #MAO FECHADA
							for k in range(i , i+15, 1): 
								bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
								bone.insertKey(armadura, 17, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 17, Object.Pose.ROT)
				#Configuracao de mao Esquerda final
				for i in range(0 , len(listaPoseMaoEsquerda), 1):
					if (listaPoseMaoEsquerda[i].split()):
						if (listaPoseMaoEsquerda[i].split()[0] == "conf_1"): #MAO ABERTA
							for k in range(i , i+15, 1): 
								if((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.013") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.014") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.004")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 20, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 20, Object.Pose.ROT)
							
								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.011") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.012") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.003")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 23, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 23, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.009") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.010") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.002")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 26, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 26, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.007") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.008") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.001")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 29, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 29, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.005") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.006") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)
								else:#DO NOTHING
									print "Erro. Ln 397."
								
			
				#Configuracao de mao Esquerda final(permanencia)					
				for i in range(0 , len(listaPoseMaoEsquerda), 1):
					if (listaPoseMaoEsquerda[i].split()):
						if (listaPoseMaoEsquerda[i].split()[0] == "conf_1"): #MAO ABERTA
							for k in range(i , i+15, 1): 
								if((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.013") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.014") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.004")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)
							
								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.011") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.012") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.003")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.009") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.010") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.002")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.007") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.008") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.001")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.005") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.006") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)
								else:#DO NOTHING
									print "Erro. Ln 449."	
			
				#Define a orientacao da mao Esquerda final
				for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
					if (listalibOritentacaoLadoEsquerdo[i].split()):
						if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
							for k in range(i , i+2, 1):	
								bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]						
								bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()					
								euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

				#Define a orientacao da mao Esquerda final(permanencia)
				for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
					if (listalibOritentacaoLadoEsquerdo[i].split()):
						if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
							for k in range(i , i+2, 1):	
								bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
								bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()					
								euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

				#Ponto de articulacao da mao Esquerda final
				for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
					if (listalibPontoArticulacaoEsquerda[i].split()): 			
  						if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
							for k in range(i , i+2, 1): 
        							bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
								bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
								bone.insertKey(armadura, 32, Object.Pose.LOC)
        							euler = bone.quat.toEuler()
        							euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        							bone.quat = euler.toQuat()
        							bone.insertKey(armadura, 32, Object.Pose.ROT)

				#Ponto de articulacao da mao Esquerda final(permanencia)
				for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
					if (listalibPontoArticulacaoEsquerda[i].split()): 			
  						if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
							for k in range(i , i+2, 1): 
        							bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
								bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
								bone.insertKey(armadura, 32, Object.Pose.LOC)
        							euler = bone.quat.toEuler()
        							euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        							bone.quat = euler.toQuat()
        							bone.insertKey(armadura, 32, Object.Pose.ROT)
				endFrame = 32

				print "EndFrame = " + str(endFrame);
			
			if(direcaoEsq == "minimo-polegar"):
				print "Direcao Esq " + direcaoEsq
				#Configuracao de mao Esquerda inicial
				for i in range(0 , len(listaPoseMaoEsquerda), 1):
					if (listaPoseMaoEsquerda[i].split()):
						if (listaPoseMaoEsquerda[i].split()[0] == "conf_60"): #MAO FECHADA
							for k in range(i , i+15, 1): 
								bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
								bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
								bone.insertKey(armadura, 17, Object.Pose.LOC)
								euler = bone.quat.toEuler()
								euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 17, Object.Pose.ROT)
				#Configuracao de mao Esquerda final
				for i in range(0 , len(listaPoseMaoEsquerda), 1):
					if (listaPoseMaoEsquerda[i].split()):
						if (listaPoseMaoEsquerda[i].split()[0] == "conf_1"): #MAO ABERTA
							for k in range(i , i+15, 1): 
								if((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.005") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.006") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 20, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 20, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.007") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.008") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.001")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 23, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 23, Object.Pose.ROT)
							
								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.009") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.010") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.002")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 26, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 26, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.011") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.012") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.003")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 29, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 29, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.013") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.014") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.004")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)
								else:#DO NOTHING
									print "Erro. Ln 397."
			
				#Configuracao de mao Esquerda final(permanencia)					
				for i in range(0 , len(listaPoseMaoEsquerda), 1):
					if (listaPoseMaoEsquerda[i].split()):
						if (listaPoseMaoEsquerda[i].split()[0] == "conf_1"): #MAO ABERTA
							for k in range(i , i+15, 1): 

								if((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.005") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.006") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.007") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.008") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.001")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.009") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.010") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.002")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.009") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.010") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.002")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								elif((listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.013") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.014") or (listaPoseMaoEsquerda[k+1].split()[0] == "BnDedo.1.L.004")):
									bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
									bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])				
									bone.insertKey(armadura, 32, Object.Pose.LOC)
									euler = bone.quat.toEuler()
									euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])				
									bone.quat = euler.toQuat()
									bone.insertKey(armadura, 32, Object.Pose.ROT)

								else:#DO NOTHING
									print "Erro. Ln 449."	
			
				#Define a orientacao da mao Esquerda final
				for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
					if (listalibOritentacaoLadoEsquerdo[i].split()):
						if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
							for k in range(i , i+2, 1):	
								bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
								bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()					
								euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

				#Define a orientacao da mao Esquerda final(permanencia)
				for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
					if (listalibOritentacaoLadoEsquerdo[i].split()):
						if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
							for k in range(i , i+2, 1):	
								bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
								bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
								bone.insertKey(armadura, 32, Object.Pose.LOC)
								euler = bone.quat.toEuler()					
								euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
								bone.quat = euler.toQuat()
								bone.insertKey(armadura, 32, Object.Pose.ROT)

				#Ponto de articulacao da mao Esquerda final
				for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
					if (listalibPontoArticulacaoEsquerda[i].split()): 			
  						if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
							for k in range(i , i+2, 1): 
        							bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
								bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
								bone.insertKey(armadura, 32, Object.Pose.LOC)
        							euler = bone.quat.toEuler()
        							euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        							bone.quat = euler.toQuat()
        							bone.insertKey(armadura, 32, Object.Pose.ROT)

				#Ponto de articulacao da mao Esquerda final(permanencia)
				for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
					if (listalibPontoArticulacaoEsquerda[i].split()): 			
  						if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
							for k in range(i , i+2, 1): 
        							bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
								bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
								bone.insertKey(armadura, 32, Object.Pose.LOC)
        							euler = bone.quat.toEuler()
        							euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
        							bone.quat = euler.toQuat()
        							bone.insertKey(armadura, 32, Object.Pose.ROT)

				endFrame = 32

				print "EndFrame = " + str(endFrame);




#Pose Padrao Final
for i in range(0 , len(listaPosePadrao), 1):
	if (listaPosePadrao[i].split()): 			
		if (listaPosePadrao[i].split()[0] == "Pose_1"):  			
			for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
       				bone = pose.bones[listaPosePadrao[k+1].split()[0]]
       				bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])
				bone.insertKey(armadura, endFrame + 15, Object.Pose.LOC)
       				euler = bone.quat.toEuler()
       				euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
       				bone.quat = euler.toQuat()
       				bone.insertKey(armadura, endFrame + 15, Object.Pose.ROT)

#Pose Padrao Final
for i in range(0 , len(listaPosePadrao), 1):
	if (listaPosePadrao[i].split()): 			
		if (listaPosePadrao[i].split()[0] == "Pose_2"):  			
			for k in range(i , i+ int(listaPosePadrao[i].split()[-1]), 1): 
       				bone = pose.bones[listaPosePadrao[k+1].split()[0]]
       				bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])
				bone.insertKey(armadura, endFrame + 15, Object.Pose.LOC)
       				euler = bone.quat.toEuler()
       				euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])	
       				bone.quat = euler.toQuat()
       				bone.insertKey(armadura, endFrame + 15, Object.Pose.ROT)

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

fixRots(0);

cena = Blender.Scene.GetCurrent()
cont = cena.getRenderingContext()
cont.renderPath = "//"+nomeSinal+"_"
cont.sFrame = 1
cont.eFrame = endFrame + 25
cont.renderAnim()

sub.Popen("ffmpeg -i "+ nomeSinal+ "*.avi -b 2028k -s 640x480 -r 30 -acodec copy "+ nomeSinal+".flv",shell=True,stdout=sub.PIPE).stdout.readlines()
temp1 = commands.getoutput('ls /home/linear/Projetos/ProjetoLibras/server/ScriptsPython | grep '+nomeSinal + '*.avi')
videoAVIrenomeado = nomeSinal + '.avi';
os.rename(temp1,  videoAVIrenomeado);

#Blender.Save("Modelo_Teste.blend", 1);

Blender.Quit
