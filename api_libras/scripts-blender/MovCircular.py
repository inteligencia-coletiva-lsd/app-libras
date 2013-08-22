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
libPontoArticulacaoDireita = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibPontoArticulacaoDir", "r")

libPoseMaoEsquerda = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibConfigMaoEsq", "r")
libOritentacaoLadoEsquerdo = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibOrientacaoEsq", "r")
libPontoArticulacaoEsquerda = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibPontoArticulacaoEsq", "r")

listaPoseMaoDireita = libPoseMaoDireita.readlines();
listalibOritentacaoLadoDireito = libOritentacaoLadoDireito.readlines();
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

poseb = pose.bones['ik_FK.R']
poseb1 = pose.bones['ik_FK.L']

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();
arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();

act = Armature.NLA.NewAction("Circular")
act.setActive(armadura)

print "############ CONFIGURACOES DA MAO DIREITA ############"

configDir = parametrosDireita[0]
configDir = configDir[:-1]
print configDir

oriDir = parametrosDireita[1]
oriDir = oriDir[:-1]
print oriDir

paDir = parametrosDireita[2]
paDir = paDir[:-1]
print paDir

tamanhoRaio = parametrosDireita[3]
tamanhoRaio = tamanhoRaio[:-1]
print tamanhoRaio

if (tamanhoRaio == 'Grande') or (tamanhoRaio == 'grande'):
	r = 1
elif (tamanhoRaio == 'Medio') or (tamanhoRaio == 'medio'):
	r = 0.6
else:
	r = 0.1

sentidoMovimentoDir = parametrosDireita[4]
sentidoMovimentoDir = sentidoMovimentoDir[:-1]
print sentidoMovimentoDir

orientacaoMovimentoDir = parametrosDireita[5]
orientacaoMovimentoDir = orientacaoMovimentoDir[:-1]
print orientacaoMovimentoDir

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


sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramDir])

frame = 0

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


keyframes = [15,18]

#Configuracao de mao direita
for u in range(0, 2, 1 ):
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configDir): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, keyframes[u], Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, keyframes[u], Object.Pose.ROT)

#Define a orientacao da mao direita
for u in range(0, 2, 1 ):
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, keyframes[u], Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, keyframes[u], Object.Pose.ROT)
#Ponto de articulacao da mao direita
for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 			
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura, 18, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, 18, Object.Pose.ROT)
	        	
xp = poseb.loc.x
yp = poseb.loc.y
zp = poseb.loc.z

if(orientacaoMovimentoDir == "para-frente"): 
	if(sentidoMovimentoDir == "anti-horario"): 
		print "anti-horario e para frente";

		frame = 18
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 23
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp, yp + r, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 33
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 38
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 48	
		poseb.loc[:] = xp, yp - r, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 53
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 58
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)		
		if(flagRepDir == "com-repeticao"):		
			frame = 63
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 68
			poseb.loc[:] = xp , yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 73
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 78
			poseb.loc[:] = xp - r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 83
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 88
			poseb.loc[:] = xp , yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)			
			frame = 93
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 98
			poseb.loc[:] = xp + r, yp , zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)			

	else: 
		print "horario e para frente";
		frame = 18
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 23
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp , yp + r , zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 33
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 38
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 48
		poseb.loc[:] = xp, yp - r, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 53
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 58
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)

		if(flagRepDir == "com-repeticao"):
			frame = 63
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 68
			poseb.loc[:] = xp  , yp + r , zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 73
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 78
			poseb.loc[:] = xp + r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 83	
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 88	
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 93	
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 98	
			poseb.loc[:] = xp - r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)


#MOVIMENTO PARA DENTRO (DIREITA) - PERPENDICULAR AO CORPO

elif(orientacaoMovimentoDir == "para-dentro"): 
	if(sentidoMovimentoDir == "horario"): 
		frame = 18
		poseb.loc[:] = xp, yp, zp - r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 23
		poseb.loc[:] = xp , yp + (r * math.sqrt(2) / 2) , zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp, yp + r , zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 33
		poseb.loc[:] = xp , yp + (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 38
		poseb.loc[:] = xp , yp , zp + r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 48	
		poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 53
		poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 58
		poseb.loc[:] = xp, yp , zp - r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)

		if(flagRepDir == "com-repeticao"):		
			frame = 63
			poseb.loc[:] = xp, yp  + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 68
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 73
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp  + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 78
			poseb.loc[:] = xp, yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 83
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 88
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 93
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 98
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)			
#MOVIMENTO ANTI-HORARIO
	else:
		frame = 18
		poseb.loc[:] = xp, yp, zp + r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 23
		poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 33
		poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 38
		poseb.loc[:] = xp, yp, zp - r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 48
		poseb.loc[:] = xp, yp - r, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 53
		poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 58
		poseb.loc[:] = xp, yp , zp + r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		if(flagRepDir == "com-repeticao"):
			frame = 63
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 68
			poseb.loc[:] = xp , yp + r , zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 73
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 78
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 83	
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 88	
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 93	
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 98	
			poseb.loc[:] = xp, yp, zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
#MOVIMENTO PARA CIMA
else:
	if(sentidoMovimentoDir == "horario"):
		print "[DIREITA]para cima e horario"
		frame = 18
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 23
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp, yp , zp + r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 33
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp  , zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 38
		poseb.loc[:] = xp + r, yp , zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp , zp  - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 48	
		poseb.loc[:] = xp, yp, zp - r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 53
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp , zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 58
		poseb.loc[:] = xp - r, yp , zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)

		if(flagRepDir == "com-repeticao"):		
			frame = 63
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp  , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 68
			poseb.loc[:] = xp, yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 73
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp , zp  + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 78
			poseb.loc[:] = xp + r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 83
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp, zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 88
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 93
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp, zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 98
			poseb.loc[:] = xp - r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)		
	else:
		print "para cima e anti-horario"
		frame = 18
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 23
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp  , zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp , yp , zp + r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 33
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 38
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 48
		poseb.loc[:] = xp, yp, zp - r
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 53
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 58
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		if(flagRepDir == "com-repeticao"):
			frame = 63
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp, zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 68
			poseb.loc[:] = xp , yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 73
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp, zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 78
			poseb.loc[:] = xp - r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 83	
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp, zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 88	
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 93	
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp, zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)	
			frame = 98	
			poseb.loc[:] = xp + r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)

		
#--------------------------------------------------------------------------------------------------
#Configurando os keyframes do lado esquerdo
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

	tamanhoRaioEsq = parametrosEsquerda[3]
	tamanhoRaioEsq = tamanhoRaioEsq[:-1]
	print tamanhoRaioEsq

	if (tamanhoRaioEsq == 'Grande') or (tamanhoRaioEsq == 'grande'):
		r1 = 1
	elif (tamanhoRaioEsq == 'Medio') or (tamanhoRaioEsq == 'medio'):
		r1 = 0.6
	else:
		r1 = 0.1
	
	sentidoMovimentoEsq = parametrosEsquerda[4]
	sentidoMovimentoEsq = sentidoMovimentoEsq[:-1]
	print sentidoMovimentoEsq

	orientacaoMovimentoEsq = parametrosEsquerda[5]
	orientacaoMovimentoEsq = orientacaoMovimentoEsq[:-1]
	print orientacaoMovimentoEsq


	flagRepEsq = parametrosEsquerda[6]
	flagRepEsq = flagRepEsq[:-1]
	print flagRepEsq

	expFacial = parametrosEsquerda[7]
	expFacial = expFacial[:-1]
	print expFacial

	sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramEsq])
	
	#sincronismo == sincrono || sincronismo == assincrono

	#Config da mao esquerda
	for i in range(0 , len(listaPoseMaoEsquerda), 1):
		if (listaPoseMaoEsquerda[i].split()):			
			if (listaPoseMaoEsquerda[i].split()[0] == configEsq): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 1, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 1, Object.Pose.ROT)
	#Orientacao da mao esquerda
	for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
		if (listalibOritentacaoLadoEsquerdo[i].split()):
			if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]
					bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])
					bone.insertKey(armadura, 1, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 1, Object.Pose.ROT)	

	#Ponto de articulacao da mao esquerda
	for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
		if (listalibPontoArticulacaoEsquerda[i].split()):
			if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        			bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 1, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, 1, Object.Pose.ROT)
	xp1 = poseb1.loc.x
	yp1 = poseb1.loc.y
	zp1 = poseb1.loc.z

#Verificação sincronismo entre as maos
	sincFlag = 'sincrono';
	if(sincFlag == 'sincrono'):
		assincronismo = 0
		print "MOV SINCRONOOOO"
	else:
		assincronismo = 1
		print "MOV ASSINCRONOOOO"
	
	frameEsq = 0
	if(orientacaoMovimentoEsq == "para-frente"):
		if(sentidoMovimentoEsq == "anti-horario"):
			print "ESQUERDA ---- para frente e anti-horario assincronismo = " + str(assincronismo)
			frameEsq = 18
			poseb1.loc[:] = xp1 + r1, yp1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 23 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 28 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 + r1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 33 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 38 + 10*assincronismo
			poseb1.loc[:] = xp1 - r1, yp1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 43 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 48 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - r1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 53 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 58 + 10*assincronismo
			poseb1.loc[:] = xp1 + r1, yp1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			if(flagRepEsq == "com-repeticao"):
				frameEsq = 63 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 68 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 73 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 78 + 10*assincronismo
				poseb1.loc[:] = xp1 - r1, yp1, zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 83 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 88 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - r1, zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 93 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 98 + 10*assincronismo
				poseb1.loc[:] = xp1 + r1, yp1, zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)

		#para-frente e horario
		else:
			print "ESQUERDA ---- para frente e horario assincronismo = " + str(assincronismo)
			frameEsq = 18
			poseb1.loc[:] = xp1 - r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 23 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 28 + 10*assincronismo
			poseb1.loc[:] = xp1 , yp1 + r1 , zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 33 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 38 + 10*assincronismo
			poseb1.loc[:] = xp1 + r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 43 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 48 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - r1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 53 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 58 + 10*assincronismo
			poseb1.loc[:] = xp1 - r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
			if(flagRepEsq == "com-repeticao"):
				frameEsq = 63 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 68 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 + r1 , zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 73 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 78 + 10*assincronismo
				poseb1.loc[:] = xp1 + r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 83 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 88 + 10*assincronismo	
				poseb1.loc[:] = xp1, yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 93 + 10*assincronismo	
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 98 + 10*assincronismo	
				poseb1.loc[:] = xp1 - r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)

	#orientacaoMovimentoEsq para-dentro (perpendicular ao corpo)
	elif(orientacaoMovimentoEsq == "para-dentro"): 
		if(sentidoMovimentoEsq == 'anti-horario'):
			frameEsq = 18
			poseb1.loc[:] = xp1, yp1, zp + r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 23 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 28 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 + r1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 33 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 38 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 , zp - r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 43 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 48 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - r1, zp
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 53 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 58 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1, zp + r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
			if(flagRepEsq == "com-repeticao"):
				frameEsq = 63 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 68 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 73 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 78 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 83 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 88 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - r1, zp
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 93 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 98 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 , zp + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)

		else:#para dentro horario
			frameEsq = 18
			poseb1.loc[:] = xp1, yp1 , zp1 - r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 23 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 28 + 10*assincronismo
			poseb1.loc[:] = xp1 , yp1 + r1 , zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 33 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 38 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 , zp1 + r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 43 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 48 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - r1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 53 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 58 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1, zp1 - r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			if(flagRepEsq == "com-repeticao"):
				frameEsq = 63 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 68 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 + r1 , zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 73 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 78 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 83 + 10*assincronismo	
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 88 + 10*assincronismo	
				poseb1.loc[:] = xp1, yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 93 + 10*assincronismo	
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 98 + 10*assincronismo	
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
	#MOVIMENTO PARA CIMA
	else:
		if(sentidoMovimentoEsq == "horario"):
			print "para cima e horario!"
			frameEsq = 18
			poseb1.loc[:] = xp1 - r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 23 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1  , zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 28 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1 , zp1 + r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 33 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1  , zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 38 + 10*assincronismo
			poseb1.loc[:] = xp1 + r1, yp1 , zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 43 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 , zp1  - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 48 + 10*assincronismo	
			poseb1.loc[:] = xp1, yp1, zp1 - r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 53 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 , zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 58 + 10*assincronismo
			poseb1.loc[:] = xp1 - r1, yp1 , zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			
			if(flagRepEsq == "com-repeticao"):		
				frameEsq = 63 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1  , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 68 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 73 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 , zp1  + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 78 + 10*assincronismo
				poseb1.loc[:] = xp1 + r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 83 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1, zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 88 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 93 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1, zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 98 + 10*assincronismo
				poseb1.loc[:] = xp1 - r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)		
		else:
			print "para cima e anti-horario"
			frameEsq = 18
			poseb1.loc[:] = xp1 + r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 23 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1  , zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 28 + 10*assincronismo
			poseb1.loc[:] = xp1 , yp1 , zp1 + r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 33 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 38 + 10*assincronismo
			poseb1.loc[:] = xp1 - r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 43 + 10*assincronismo
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 48 + 10*assincronismo
			poseb1.loc[:] = xp1, yp1, zp1 - r1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 53 + 10*assincronismo
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			frameEsq = 58 + 10*assincronismo
			poseb1.loc[:] = xp1 + r1, yp1, zp1
			poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)

			if(flagRepEsq == "com-repeticao"):
				frameEsq = 63 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1, zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 68 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 73 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1, zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 78 + 10*assincronismo
				poseb1.loc[:] = xp1 - r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 83 + 10*assincronismo	
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1, zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 88 + 10*assincronismo	
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 93 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1, zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
				frameEsq = 98 + 10*assincronismo	
				poseb1.loc[:] = xp1 + r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
else: 
	expFacial = parametrosEsquerda[1]
	expFacial = expFacial[:-1]
	print expFacial

	sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramEsq])

if(maoUtil == 'uma'):
	if(flagRepDir == 'com-repeticao'):
		endFrame = 98
	#sem repeticao
	else:
		endFrame = 58
#duas maos
else:
	if(sincFlag == 'sincrono'):
		if(flagRepDir == 'com-repeticao'):
			frame = 98
		#sem repeticao
		else:
			frame = 58
		
		if(flagRepEsq == 'com-repeticao'):
			frameEsq = 98
		#sem repeticao
		else:
			frameEsq = 58
	#assincrono
	else:
		if(flagRepDir == 'com-repeticao'):
			frame = 98
		#sem repeticao
		else:
			frame = 58
		
		if(flagRepEsq == 'com-repeticao'):
			frameEsq = 108
		#sem repeticao
		else:
			frameEsq = 68

	if(frame > frameEsq):
		endFrame = frame
		#print "endFrame" + " " + str(endFrame)
	else:
		endFrame = frameEsq
		#print "endFrame" + " " + str(endFrame)

	print "frameDir " + str(frame)
	print "frameEsq " + str(frameEsq)
	print "endFrame " + str(endFrame)

#Define a orientacao da mao direita
for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, endFrame, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, endFrame, Object.Pose.ROT)

#Configuracao de mao direita
for i in range(0 , len(listaPoseMaoDireita), 1):
	if (listaPoseMaoDireita[i].split()):
		if (listaPoseMaoDireita[i].split()[0] == configDir): 
			for k in range(i , i+15, 1): 
				bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
				bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
				bone.insertKey(armadura, endFrame, Object.Pose.LOC)
				euler = bone.quat.toEuler()
				euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, endFrame, Object.Pose.ROT)

if(maoUtil == 'duas'):
#Orientacao da mao esquerda
	for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
		if (listalibOritentacaoLadoEsquerdo[i].split()):
			if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]
					bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])
					bone.insertKey(armadura, endFrame, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, endFrame, Object.Pose.ROT)	

#Config da mao esquerda
	for i in range(0 , len(listaPoseMaoEsquerda), 1):
		if (listaPoseMaoEsquerda[i].split()):			
			if (listaPoseMaoEsquerda[i].split()[0] == configEsq): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, endFrame, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, endFrame, Object.Pose.ROT)
	


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

posePadrao = ["Pose_1", "Pose_2"]
for h in range(0, 2, 1):
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


cena = Blender.Scene.GetCurrent()
cont = cena.getRenderingContext()
cont.renderPath = "//"+nomeSinal+"_"
cont.sFrame = 0
cont.eFrame = endFrame + 25
cont.renderAnim()

print "Removendo ParamDir e ParamEsq da pasta ScriptsPython"
sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"Dir", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"Esq"])
print
print"Convertendo AVI em FLV usando ffmpeg"

num = endFrame + 25
if(num > 100):
	s = "0" + str(num);
else: 
	s = "00" + str(num);

print nomeSinal+"_0001_"+s+".avi";

sub.call(["ffmpeg", "-i", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"_0001_"+s+".avi", "-b", "2028k", "-s", "640x480", "-r", "30", "-acodec", "copy",  nomeSinal+".flv"])

print idUsuario + "**********************************************"
sub.call(["mv", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+".flv", "/home/gtaaas/gtaaas_web/public/uploads/files/"+idUsuario + "/"])

#sub.call(["mv", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"_0001_"+s+".avi", "home/gtaaas_web/public/uploads/files/" + idUsuario + "/" + nomeSinal+".avi"])

Blender.Quit()






