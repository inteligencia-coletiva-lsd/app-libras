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
libPosePadrao = open("/usr/share/WikiLIBRAS/server/ScriptsPython/Libs/LibPosePadrao", "r")

listaPosePadrao = libPosePadrao.readlines();
listaExpressaoFacial = libExpressaoFacial.readlines();


armadura = Blender.Object.Get('Armature.001');
pose = armadura.getPose()

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();

arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();


poseb = pose.bones['ik_FK.R']
poseb1 = pose.bones['ik_FK.L']

act = Armature.NLA.NewAction("SemiCircular")
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
	r = 0.3

sentidoMovimentoDir = parametrosDireita[4]
sentidoMovimentoDir = sentidoMovimentoDir[:-1]
print sentidoMovimentoDir

orientacaoMovimentoDir = parametrosDireita[5]
orientacaoMovimentoDir = orientacaoMovimentoDir[:-1]
print orientacaoMovimentoDir

direcaoDir = parametrosDireita[6] #Orientacao do Movimento. Paralelo ou Perpendicular ao corpo
direcaoDir = direcaoDir[:-1]
print direcaoDir

flagRepDir = parametrosDireita[7]
flagRepDir = flagRepDir[:-1]
print flagRepDir

flagRepDir = "sem-repeticao"

tipoRepDir =  'avancar'

maoUtil = parametrosDireita[8]
maoUtil = maoUtil[:-1]
print maoUtil
	
nomeSinal = parametrosDireita[9]
nomeSinal = nomeSinal[:-1]
print nomeSinal

idUsuario = parametrosDireita[10]
idUsuario = idUsuario[:-1]
print idUsuario

print "########################PARAMETROS#########################";
print "DIREITA";
print parametrosDireita
print "###########################################################";

sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramDir])

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
for i in range(0 , len(listaPoseMaoDireita), 1):
	if (listaPoseMaoDireita[i].split()):
		if (listaPoseMaoDireita[i].split()[0] == configDir): 
			for k in range(i , i+15, 1): 
				bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
				bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
				bone.insertKey(armadura, 15, Object.Pose.LOC)
				euler = bone.quat.toEuler()
				euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, 15, Object.Pose.ROT)

#Configuracao de mao direita
for i in range(0 , len(listaPoseMaoDireita), 1):
	if (listaPoseMaoDireita[i].split()):
		if (listaPoseMaoDireita[i].split()[0] == configDir): 
			for k in range(i , i+15, 1): 
				bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
				bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
				bone.insertKey(armadura, 18, Object.Pose.LOC)
				euler = bone.quat.toEuler()
				euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, 18, Object.Pose.ROT)

#Define a orientacao da mao direita
for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
	if (listalibOritentacaoLadoDireito[i].split()):
		if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
			for k in range(i , i+2, 1):	
				bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
				bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
				bone.insertKey(armadura, 15, Object.Pose.LOC)
				euler = bone.quat.toEuler()					
				euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, 15, Object.Pose.ROT)

#Define a orientacao da mao direita
for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
	if (listalibOritentacaoLadoDireito[i].split()):
		if (listalibOritentacaoLadoDireito[i].split()[0] == oriDir):	
			for k in range(i , i+2, 1):	
				bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
				bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
				bone.insertKey(armadura, 18, Object.Pose.LOC)
				euler = bone.quat.toEuler()					
				euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, 18, Object.Pose.ROT)

#Ponto de articulacao da mao direita
for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): 			
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(armadura, 15, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, 15, Object.Pose.ROT)

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

frame = 0;
frameEsq = 0;

if(orientacaoMovimentoDir == "para-frente"):
	print "para-frente"
	if(sentidoMovimentoDir == "horario"):
		if(direcaoDir == "para-direita"):
			print "para-direita"
			frame = 18
			poseb.loc[:] = xp - r , yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp + r, yp, zp		
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			
			if(flagRepDir == "com-repeticao"):	
				if(tipoRepDir == "retroceder"):	
					frame = 43
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp + r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: 
					xp = poseb.loc.x + r
					yp = poseb.loc.y
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp + r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)


		else:#Direção = para-esquerda
			print "para esquerda"
			frame = 18
			poseb.loc[:] = xp + r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp - r, yp, zp		
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			
			if(flagRepDir == "com-repeticao"):	
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp + r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x - r
					yp = poseb.loc.y
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp + r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)			


	else:#Sentido Anti-Horario
		print "sentido anti-horario. linha 362"
		if(direcaoDir == "para-direita"): #para direita
			print "Para direita. linha 364"
			frame = 18
			poseb.loc[:] = xp - r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp , yp - r , zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp + r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)

			if(flagRepDir == "com-repeticao"):	
				if(tipoRepDir == "retroceder"):
					print "anti horario, para direita, com repeticao, RETROCEDER."
					frame = 43
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp - r , zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp + r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					print "anti horario, para direita, com repeticao, AVANCAR."
					xp = poseb.loc.x + r
					yp = poseb.loc.y
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2) , zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp- (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp + r, yp , zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
		if(direcaoDir == "para-esquerda"): #para direita
			print "Para ESQUERDA. Linha 417"
			frame = 18
			poseb.loc[:] = xp + r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp , yp + r , zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp - r, yp, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):	
				if(tipoRepDir == "retroceder"):
					print "anti horario, para direita, com repeticao, RETROCEDER."
					frame = 43
					poseb.loc[:] = xp + r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp + r , zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				if(tipoRepDir == "avancar"): #avancar
					print "anti horario, para direita, com repeticao, AVANCAR."
					xp = poseb.loc.x - r
					yp = poseb.loc.y
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp + r, yp , zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp + (r * math.sqrt(2) / 2) , zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp - r, yp, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)

elif(orientacaoMovimentoDir == "para-dentro"): 
	if(sentidoMovimentoDir == "horario"): 
		if(direcaoDir == "para-frente"):
			frame = 18
			poseb.loc[:] = xp, yp , zp  - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23	
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)			
			frame = 33
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp , yp, zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)					
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp, yp , zp  - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48	
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)			
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp , yp, zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y
					zp = poseb.loc.z + r	
					frame = 43
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48	
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)			
					frame = 58
					poseb.loc[:] = xp, yp, zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					

#direção direita = para trás e horario
		elif(direcaoDir == "para-tras"):
			frame = 18
			poseb.loc[:] = xp, yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp , yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp , yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38	
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp, yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp , yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63	
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y
					zp = poseb.loc.z - r
					frame = 43
					poseb.loc[:] = xp, yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp , yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63	
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
		elif(direcaoDir == "para-cima"):
			frame = 18
			poseb.loc[:] = xp , yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28	
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp , yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53	
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y + r
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp , yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp  - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53	
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
# direcao dir = para baixo
		else:
			frame = 18
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp , yp + (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp , yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp , yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp , yp + (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp , yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp , yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y - r
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp , yp + (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp , yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp , yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
	
#sentido movimento direita anti-horario
	else:
		if(direcaoDir == "para-frente"):
			frame = 18
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)			
			frame = 38
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 43
			poseb.loc[:] = xp , yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 48
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 68
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 73
					poseb.loc[:] = xp , yp , zp + r
					frame = 78
					poseb.loc[:] = xp , yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y
					zp = poseb.loc.z + r
					frame = 48
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)			
					frame = 68
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 73
					poseb.loc[:] = xp , yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)

		elif(direcaoDir == "para-tras"):
			frame = 18
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp , yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 43
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 48
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 68
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 73
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y
					zp = poseb.loc.z - r
					frame = 48
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 68
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 73
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)


		elif(direcaoDir == "para-cima"):
			frame = 18
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp , yp , zp + r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y + r
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2) , zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp , yp , zp + r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
#direcao direita = para baixo		
		else:
			frame = 18
			poseb.loc[:] = xp, yp + r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 23
			poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 28
			poseb.loc[:] = xp, yp, zp - r
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 33
			poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			frame = 38
			poseb.loc[:] = xp, yp - r, zp
			poseb.insertKey(armadura, frame, Object.Pose.LOC)
			if(flagRepDir == "com-repeticao"):
				if(tipoRepDir == "retroceder"):
					frame = 43
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
				else: #avancar
					xp = poseb.loc.x
					yp = poseb.loc.y - r
					zp = poseb.loc.z
					frame = 43
					poseb.loc[:] = xp, yp + r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 48
					poseb.loc[:] = xp, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 53
					poseb.loc[:] = xp, yp, zp - r
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 58
					poseb.loc[:] = xp, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
					frame = 63
					poseb.loc[:] = xp, yp - r, zp
					poseb.insertKey(armadura, frame, Object.Pose.LOC)
#Orientação para-cima
else:
	print "Orientação para Cima em desenvolvimento...";
	
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
		r1 = 0.3
	
	sentidoMovimentoEsq = parametrosEsquerda[4]
	sentidoMovimentoEsq = sentidoMovimentoEsq[:-1]
	print sentidoMovimentoEsq

	orientacaoMovimentoEsq = parametrosEsquerda[5]
	orientacaoMovimentoEsq = orientacaoMovimentoEsq[:-1]
	print orientacaoMovimentoEsq

	direcaoEsq = parametrosEsquerda[6]
	direcaoEsq = direcaoEsq[:-1]
	print direcaoEsq

	flagRepEsq = parametrosEsquerda[7]
	flagRepEsq = flagRepEsq[:-1]
	print flagRepEsq

	expFacial = parametrosEsquerda[8]
	expFacial = expFacial[:-1]
	print expFacial

	sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramEsq])
		
	#Config da mao esquerda
	for i in range(0 , len(listaPoseMaoEsquerda), 1):
		if (listaPoseMaoEsquerda[i].split()):			
			if (listaPoseMaoEsquerda[i].split()[0] == configEsq): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 15, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 1, Object.Pose.ROT)
	#Config da mao esquerda
	for i in range(0 , len(listaPoseMaoEsquerda), 1):
		if (listaPoseMaoEsquerda[i].split()):			
			if (listaPoseMaoEsquerda[i].split()[0] == configEsq): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 18, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 18, Object.Pose.ROT)

	#Orientacao da mao esquerda
	for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
		if (listalibOritentacaoLadoEsquerdo[i].split()):
			if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]
					bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])
					bone.insertKey(armadura, 15, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 15, Object.Pose.ROT)	

	#Orientacao da mao esquerda
	for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
		if (listalibOritentacaoLadoEsquerdo[i].split()):
			if (listalibOritentacaoLadoEsquerdo[i].split()[0] == oriEsq):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]
					bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])
					bone.insertKey(armadura, 18, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 18, Object.Pose.ROT)	

	#Ponto de articulacao da mao esquerda
	for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
		if (listalibPontoArticulacaoEsquerda[i].split()):
			if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        			bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 15, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, 15, Object.Pose.ROT)

	#Ponto de articulacao da mao esquerda
	for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
		if (listalibPontoArticulacaoEsquerda[i].split()):
			if (listalibPontoArticulacaoEsquerda[i].split()[0] == paEsq):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        			bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 18, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, 18, Object.Pose.ROT)
	xp1 = poseb1.loc.x
	yp1 = poseb1.loc.y
	zp1 = poseb1.loc.z

	#Verificação sincronismo entre as maos
	sincFlag = 'sincrono'
	if(sincFlag == 'sincrono'):
		assincronismo = 0
		print "MOV SINCRONOOOO"
	else:
		assincronismo = 1
		print "MOV ASSINCRONOOOO"
	
	frameEsq = 0
	
	if(orientacaoMovimentoEsq == "para-frente"):
		if(sentidoMovimentoEsq == "horario"): 
			if(direcaoEsq == "para-direita"):	
				frameEsq = 18
				poseb1.loc[:] = xp1 + r1, yp1, zp1
				poseb1.insertKey(armadura, frame, Object.Pose.LOC)
				frameEsq = 23  + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1 - r1, yp1, zp1		
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):	
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1+ r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x - r1
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
		
			else: #(direcao_esquerda == "para-esquerda"):	
				frameEsq = 18
				poseb1.loc[:] = xp1 - r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1 + r1, yp1, zp1		
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):	
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x + r1
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)		
#sentido esquerda anti-horario
		else:
			if(direcaoEsq == "para-direita"):	
				frameEsq = 18
				poseb1.loc[:] = xp1 - r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 + r1 , zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1 + r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):	
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 + r1 , zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x + r1
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 + r1 , zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			
			else: #(direcao_esquerda == "para-esquerda"):
				frameEsq = 18
				poseb1.loc[:] = xp1 + r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 - r1 , zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1 - r1, yp1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):	
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1 , zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x - r1
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 + r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1 , zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 - r1, yp1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)

	elif(orientacaoMovimentoEsq == "para-dentro"):
		if(sentidoMovimentoEsq == "horario"): 	
			if(direcaoEsq == "para-frente"):
				frameEsq = 18
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23	 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 + (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 43 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53	 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 68 +10*assincronismo
						poseb1.loc[:] = xp1 , yp1 + (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 73 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 78 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z + r1
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53	 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 68 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1+ (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 73 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 78 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
			elif(direcaoEsq == "para-tras"):	
				frameEsq = 18
				poseb1.loc[:] = xp1, yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38	 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63	 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z - r1
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo	
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			elif(direcaoEsq == "para-cima"):	
				frameEsq = 18
				poseb1.loc[:] = xp1 , yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28	 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo	
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y + r1
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1  - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo	
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			else: #if(direcao_esquerda == "para-baixo"):	
				frameEsq = 19
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 + (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 + (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y - r1
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 + (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
#sentido esquerda anti-horario
		else:
			if(direcaoEsq == "para-frente"):
				frameEsq = 18
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 43 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					
						frameEsq = 68 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 73 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 78 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z + r1
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)			
						frameEsq = 68 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 73 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)	
			elif(direcaoEsq == "para-tras"):	
				frameEsq = 18
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 43 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 68 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 73 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y
						zp1 = poseb1.loc.z - r1
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 68 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 73 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			elif(direcaoEsq == "para-cima"):	
				frameEsq = 18
				poseb1.loc[:] = xp1, yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1 , yp1 , zp1 + r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y + r1
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2) , zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1 , yp1 , zp1 + r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
			else: #if(direcao_esquerda == "para-baixo"):	
				frameEsq = 18
				poseb1.loc[:] = xp1, yp1 + r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 23 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 28 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1, zp1 - r1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 33 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				frameEsq = 38 + 10*assincronismo
				poseb1.loc[:] = xp1, yp1 - r1, zp1
				poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
				if(flagRepEsq == "com-repeticao"):
					if(tipoRepEsq == "retroceder"):
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
					else: #avancar
						xp1 = poseb1.loc.x
						yp1 = poseb1.loc.y - r1
						zp1 = poseb1.loc.z
						frameEsq = 43 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 48 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 + (r1 * math.sqrt(2) / 2), zp1- (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 53 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1, zp1 - r1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 58 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
						frameEsq = 63 + 10*assincronismo
						poseb1.loc[:] = xp1, yp1 - r1, zp1
						poseb1.insertKey(armadura, frameEsq, Object.Pose.LOC)
#Orientacao esquerda para cima
	else:
		print "Em desenvolvimento ...";
					
else: 
	expFacial = parametrosEsquerda[1]
	expFacial = expFacial[:-1]
	print expFacial
	sub.call(["rm", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+paramEsq])
							

print "Frame Dir = " + str(frame);
print "Frame Esq = " + str(frameEsq);

endFrame = 0;

if(frame > frameEsq):
	endFrame = frame;
else:
	endFrame = frameEsq;

print "End Frame  = " + str(endFrame);

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
	
fixRots(0)
fixRots(1)

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


fixRots(0) 
fixRots(1)

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




'''						
nomeVideoTemp = substr(nomeVideo, 0, len(nomeVideo) - 1)
print nomeVideoTemp
'''	
cena = Blender.Scene.GetCurrent()
cont = cena.getRenderingContext()
cont.renderPath = "//"+nomeSinal+"_"
cont.sFrame = 1
cont.eFrame = endFrame + 30
cont.renderAnim()


num = endFrame + 30
if(num > 100):
	s = "0" + str(num);
else: 
	s = "00" + str(num);

sub.call(["ffmpeg", "-i", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+"_0001_"+s+".avi", "-b", "2028k", "-s", "640x480", "-r", "30", "-acodec", "copy",  nomeSinal+".flv"])

print idUsuario + "**********************************************"
sub.call(["mv", "/usr/share/WikiLIBRAS/server/ScriptsPython/"+nomeSinal+".flv", "/home/gtaaas/gtaaas_web/public/uploads/files/"+idUsuario + "/"])

Blender.Quit()


