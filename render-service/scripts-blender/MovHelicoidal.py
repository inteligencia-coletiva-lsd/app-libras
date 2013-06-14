#!BPY
# -*- coding: utf-8 -*-

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
	
print "Recebendo os nomes dos parametros das mãos direita e esquerda."

paramDir = sys.argv[5]
paramEsq = sys.argv[6]

print paramDir
print paramEsq

print "Abrindo libs"
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

arm = Blender.Object.Get('Armature.001');
pose = arm.getPose()

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();

arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();

#movimento do dedo indicador
poseb = pose.bones['ik_FK.R']
poseb1 = pose.bones['ik_FK.L']

act = Armature.NLA.NewAction("Helicoidal")
act.setActive(arm)

print "Parametros da mao direita"
configDir = parametrosDireita[0]
oriDir = parametrosDireita[1]
ponto_articulacao_dir = parametrosDireita[2]
sentido_movimento_d = parametrosDireita[3]
direcao_direita = parametrosDireita[4]
tamanho_raio = parametrosDireita[5]
raio = substr(tamanho_raio, 0, len(tamanho_raio) - 1)
if (raio == 'Grande'):
	r = 1
elif (raio == 'Medio'):
	r = 0.6
else:
	r = 0.3
	
print "RaioDir"
print r

nomeVideo = parametrosDireita[6]

config_mao_direita = substr(configDir, 0, len(configDir) - 1)
orientacao_direita = substr(oriDir, 0, len(oriDir) - 1)
ponto_articulacao_direita = substr(ponto_articulacao_dir, 0, len(ponto_articulacao_dir) - 1)
sentido_movimento_dir = substr(sentido_movimento_d, 0, len(sentido_movimento_d) - 1)
direcao_dir = substr(direcao_direita, 0, len(direcao_direita) - 1)

print "########################PARAMETROS#########################";
print "DIREITA";
print parametrosDireita
print "###########################################################";



#Configuracao de mao
for i in range(0 , len(listaPoseMaoDireita), 1):
	if (listaPoseMaoDireita[i].split()):
		if (listaPoseMaoDireita[i].split()[0] == config_mao_direita): 	
			#print config_mao_direita	
			for k in range(i , i+15, 1): #varrendo todos os ossos da mao
				bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
				bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
				bone.insertKey(arm, 1, Object.Pose.LOC)
				euler = bone.quat.toEuler()
				euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
				bone.quat = euler.toQuat()
				bone.insertKey(arm, 1, Object.Pose.ROT)

#Define a orientacao da mao direita incial
for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == orientacao_direita):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(arm, 1, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(arm, 1, Object.Pose.ROT)

#Ponto de articulacao da mao direita

# len(listalibPontoArticulacaoDireita) == numero de linhas do arquivo LibPontoArticulacaoEsq

for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
		if (listalibPontoArticulacaoDireita[i].split()): #Split em cada linha			
	  		if (listalibPontoArticulacaoDireita[i].split()[0] == ponto_articulacao_direita):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
					bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
					bone.insertKey(arm, 1, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(arm, 1, Object.Pose.ROT)
	        			
#Configurando expressão facial do sinal NEUTRA
for i in range(0 , len(listaExpressaoFacial), 1):
		if (listaExpressaoFacial[i].split()): #Split em cada linha			
	  		if (listaExpressaoFacial[i].split()[0] == "Exp_9"):
	  			#print listaExpressaoFacial[i].split()[0];
				for k in range(i , i+int(listaExpressaoFacial[i].split()[-1]), 1): 
	        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
	        			#print bone;
					bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
					bone.insertKey(arm, 1, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(arm, 1, Object.Pose.ROT)	        			

temp = parametrosEsquerda[0][:-1]

print "########################PARAMETROS#########################";
print "ESQUERDA";
print parametrosEsquerda
print "###########################################################";

if(temp != 'Nenhum'):	
	print "parametrosEsq[0] != Nenhum";

	configEsq = parametrosEsquerda[0]
	oriEsq = parametrosEsquerda[1]
	ponto_articulacao_Esq = parametrosEsquerda[2]
	sentido_movimento_e = parametrosEsquerda[3]
	direcao_esquerda = parametrosEsquerda[4]
	r1 = 0.4#parametros[5]
	#if(tamanho_raio == "Pequeno"):
	#	r = 0.2;
	#if(tamanho_raio == "Medio"):
	#	r = 0.5;
	#if(tamanho_raio == "Grande"):
	#	r = 1;
	exp_facial = parametrosEsquerda[6]


	config_mao_esquerda = substr(configEsq, 0, len(configEsq) - 1)
	orientacao_esquerda = substr(oriEsq, 0, len(oriEsq) - 1)
	ponto_articulacao_esquerda = substr(ponto_articulacao_Esq, 0, len(ponto_articulacao_Esq) - 1)
	sentido_movimento_esq = substr(sentido_movimento_e, 0, len(sentido_movimento_e) - 1)
	direcao_esq = substr(direcao_esquerda, 0, len(direcao_esquerda) - 1)
	expressao_facial = substr(exp_facial, 0, len(exp_facial) - 1)
	
	
	#Config da mao esquerda
	for i in range(0 , len(listaPoseMaoEsquerda), 1):
		if (listaPoseMaoEsquerda[i].split()):			
			if (listaPoseMaoEsquerda[i].split()[0] == config_mao_esquerda): 
				
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
					bone.insertKey(arm, 1, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(arm, 1, Object.Pose.ROT)
#Orientacao da mao esquerda
	for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
		if (listalibOritentacaoLadoEsquerdo[i].split()):
			if (listalibOritentacaoLadoEsquerdo[i].split()[0] == orientacao_esquerda):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]
					bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])
					bone.insertKey(arm, 1, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(arm, 1, Object.Pose.ROT)	

#Ponto de articulacao da mao esquerda

	for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
		if (listalibPontoArticulacaoEsquerda[i].split()):
			if (listalibPontoArticulacaoEsquerda[i].split()[0] == ponto_articulacao_esquerda):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        			bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
					bone.insertKey(arm, 1, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(arm, 1, Object.Pose.ROT)

xp = poseb.loc.x
yp = poseb.loc.y
zp = poseb.loc.z

xp1 = poseb1.loc.x
yp1 = poseb1.loc.y
zp1 = poseb1.loc.z




if(sentido_movimento_dir == "horario"): 
	if(direcao_dir == "para-baixo"):
		frame = 1
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 6
		poseb.loc[:] = xp, yp - 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 9
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 12
		poseb.loc[:] = xp - r, yp - 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 15
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 18
		poseb.loc[:] = xp, yp - 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 21
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 24
		poseb.loc[:] = xp + r, yp - 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		xp = poseb.loc.x - r
		yp = poseb.loc.y
		zp = poseb.loc.z
	
		frame = 27
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 30
		poseb.loc[:] = xp, yp - 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 33
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 36
		poseb.loc[:] = xp - r, yp - 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 39
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 42
		poseb.loc[:] = xp, yp - 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 45
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 48
		poseb.loc[:] = xp + r, yp - 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-cima"):
		frame = 1
		poseb.loc[:] = xp + r, yp, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 6
		poseb.loc[:] = xp, yp + 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 9
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 12
		poseb.loc[:] = xp - r, yp + 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 15
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 18
		poseb.loc[:] = xp, yp + 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 21
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 24
		poseb.loc[:] = xp + r, yp + 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		xp = poseb.loc.x - r
		yp = poseb.loc.y
		zp = poseb.loc.z
	
		frame = 27
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 30
		poseb.loc[:] = xp, yp + 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 33
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 36
		poseb.loc[:] = xp - r, yp + 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 39
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 42
		poseb.loc[:] = xp, yp + 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 45
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 48
		poseb.loc[:] = xp + r, yp + 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-direita"): #inverti os sinais do eixo z para mudar de anti-horari para horario
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp - 0.1, yp+ (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp - 0.2, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp - 0.3 , yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp - 0.4 , yp- r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp - 0.5 , yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp - 0.6, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp - 0.7 , yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp - 0.8, yp+ r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp - 0.1, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp - 0.2, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp - 0.3, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp - 0.4, yp - r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp - 0.5 , yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp - 0.6, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp - 0.7 , yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp - 0.8, yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-esquerda"): #acho que ficou anti-horario e nao horario
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp  + 0.1, yp+ (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp+ 0.2, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp+ 0.3 , yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp + 0.4 , yp- r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp+ 0.5 , yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp+ 0.6, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp + 0.7 , yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp  + 0.8, yp+ r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp + 0.1, yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp+ 0.2, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp + 0.3, yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp+ 0.4, yp - r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp+ 0.5 , yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp+ 0.6, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp+ 0.7 , yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp + 0.8, yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		
	if(direcao_dir == "para-frente"):
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp+ (r * math.sqrt(2) / 2), yp+ (r * math.sqrt(2) / 2), zp   + 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp + r, yp , zp + 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp  + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp + 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp , yp- r, zp + 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp- (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp + 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp - r, yp , zp+ 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp  - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp + 0.7
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp , yp+ r, zp + 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp + (r * math.sqrt(2) / 2), zp+ 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp + r, yp , zp+ 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp+ 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp, yp - r, zp+ 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp  - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp+ 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp - r, yp , zp+ 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp- (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp + 0.7 
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp, yp + r, zp + 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-tras"):
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp - 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp + r, yp , zp - 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp - 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp , yp - r, zp - 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp - 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp - r, yp , zp - 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp - 0.7
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp , yp + r, zp - 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp + (r * math.sqrt(2) / 2), zp - 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp + r, yp , zp - 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp - 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp, yp - r, zp - 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp  - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp - 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp - r, yp , zp - 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp- (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp - 0.7 
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp, yp + r, zp - 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		
else: #sentido movimento direita = anti-horario
	if(direcao_dir == "para-baixo"):
		frame = 1
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 6
		poseb.loc[:] = xp, yp - 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 9
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 12
		poseb.loc[:] = xp + r, yp - 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 15
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 18
		poseb.loc[:] = xp, yp - 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 21
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 24
		poseb.loc[:] = xp - r, yp - 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		xp = poseb.loc.x + r
		yp = poseb.loc.y
		zp = poseb.loc.z
	
		frame = 27
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 30
		poseb.loc[:] = xp, yp - 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 33
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 36
		poseb.loc[:] = xp + r, yp - 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 39
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 42
		poseb.loc[:] = xp, yp - 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 45
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 48
		poseb.loc[:] = xp - r, yp - 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-cima"):
		frame = 1
		poseb.loc[:] = xp - r, yp, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 6
		poseb.loc[:] = xp, yp + 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 9
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 12
		poseb.loc[:] = xp + r, yp + 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 15
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 18
		poseb.loc[:] = xp, yp + 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 21
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 24
		poseb.loc[:] = xp - r, yp + 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		xp = poseb.loc.x + r
		yp = poseb.loc.y
		zp = poseb.loc.z
	
		frame = 27
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.1, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 30
		poseb.loc[:] = xp, yp + 0.2, zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 33
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.3, zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 36
		poseb.loc[:] = xp + r, yp + 0.4, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 39
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + 0.5, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 42
		poseb.loc[:] = xp, yp + 0.6, zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 45
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + 0.7, zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
	
		frame = 48
		poseb.loc[:] = xp - r, yp + 0.8, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-direita"): #inverti os sinais do eixo z para mudar de anti-horari para horario
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp - 0.1, yp+ (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp - 0.2, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp - 0.3 , yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp - 0.4 , yp- r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp - 0.5 , yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp - 0.6, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp - 0.7 , yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp - 0.8, yp+ r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp - 0.1, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp - 0.2, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp - 0.3, yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp - 0.4, yp - r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp - 0.5 , yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp - 0.6, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp - 0.7 , yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp - 0.8, yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-esquerda"): 
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp  + 0.1, yp+ (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp+ 0.2, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp+ 0.3 , yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp + 0.4 , yp- r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp+ 0.5 , yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp+ 0.6, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp + 0.7 , yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp  + 0.8, yp+ r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp + 0.1, yp + (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp+ 0.2, yp , zp + r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp + 0.3, yp - (r * math.sqrt(2) / 2), zp + (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp+ 0.4, yp - r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp+ 0.5 , yp - (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp+ 0.6, yp , zp - r
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp+ 0.7 , yp + (r * math.sqrt(2) / 2), zp - (r * math.sqrt(2) / 2)
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp + 0.8, yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		
	if(direcao_dir == "para-frente"):
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp- (r * math.sqrt(2) / 2), yp+ (r * math.sqrt(2) / 2), zp   + 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp - r, yp , zp + 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp  - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp + 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp , yp- r, zp + 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp + 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp + r, yp , zp+ 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp  + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp + 0.7
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp , yp+ r, zp + 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2) , yp + (r * math.sqrt(2) / 2), zp+ 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp - r, yp , zp+ 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp+ 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp, yp - r, zp+ 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp  + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp+ 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp + r, yp , zp+ 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp + 0.7 
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp, yp + r, zp + 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
	if(direcao_dir == "para-tras"):
		frame = 1
		poseb.loc[:] = xp , yp + r, zp
		poseb.insertKey(arm, frame, Object.Pose.LOC)

		frame = 3
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp - 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
			
		frame = 6
		poseb.loc[:] = xp - r, yp , zp - 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 9
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp - 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 12
		poseb.loc[:] = xp , yp - r, zp - 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 15
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp - 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 18
		poseb.loc[:] = xp + r, yp , zp - 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 21
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp - 0.7
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 24
		poseb.loc[:] = xp , yp + r, zp - 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		xp = poseb.loc.x 
		yp = poseb.loc.y - r
		zp = poseb.loc.z
		
		frame = 27
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2) , yp + (r * math.sqrt(2) / 2), zp - 0.1
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 30
		poseb.loc[:] = xp - r, yp , zp - 0.2
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 33
		poseb.loc[:] = xp - (r * math.sqrt(2) / 2) , yp - (r * math.sqrt(2) / 2), zp - 0.3
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 36
		poseb.loc[:] = xp, yp - r, zp - 0.4
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 39
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp - (r * math.sqrt(2) / 2), zp - 0.5
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 42
		poseb.loc[:] = xp + r, yp , zp - 0.6
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 45
		poseb.loc[:] = xp + (r * math.sqrt(2) / 2), yp + (r * math.sqrt(2) / 2), zp - 0.7 
		poseb.insertKey(arm, frame, Object.Pose.LOC)
		
		frame = 48
		poseb.loc[:] = xp, yp + r, zp - 0.8
		poseb.insertKey(arm, frame, Object.Pose.LOC)

	
########################################################################################################################


if(temp != 'Nenhum'):
	if(sentido_movimento_esq == "horario"): 
	    	
        	if(direcao_esq == "para-baixo"):
			print
        		print"Direção do Movimento da Mão Esquerda é para baixo.";
        		print
			frame = 1
			poseb1.loc[:] = xp1 + r1, yp1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)	
			frame = 3
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 6
			poseb1.loc[:] = xp1, yp1 - 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 9
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 12
			poseb1.loc[:] = xp1 - r1, yp1 - 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 15
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 18
			poseb1.loc[:] = xp1, yp1 - 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 21
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 24
			poseb1.loc[:] = xp1 + r1, yp1 - 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x - r1
			yp1 = poseb1.loc.y
			zp1 = poseb1.loc.z
				
			frame = 27
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1, yp1 - 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 33
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 36
			poseb1.loc[:] = xp1 - r1, yp1 - 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 42
			poseb1.loc[:] = xp1, yp1 - 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1 + r1, yp1 - 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
		if(direcao_esq == "para-cima"):
			frame = 1
			poseb1.loc[:] = xp1 + r1, yp1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 6
			poseb1.loc[:] = xp1, yp1 + 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 9
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 12
			poseb1.loc[:] = xp1 - r1, yp1 + 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 15
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 18
			poseb1.loc[:] = xp1, yp1 + 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 21
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 24
			poseb1.loc[:] = xp1 + r1, yp1 + 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x - r1
			yp1 = poseb1.loc.y
			zp1 = poseb1.loc.z
			
			frame = 27
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1, yp1 + 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 33
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 36
			poseb1.loc[:] = xp1 - r1, yp1 + 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 42
			poseb1.loc[:] = xp1, yp1 + 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1 + r1, yp1 + 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
		if(direcao_esq == "para-direita"): #inverti os sinais do eixo z para mudar de anti-horari para horario
			print "Esquerda horario e para direita";
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1 - 0.1, yp1+ (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1 - 0.2, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 9
			poseb1.loc[:] = xp1 - 0.3 , yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 - 0.4 , yp1- r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1 - 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 18
			poseb1.loc[:] = xp1 - 0.6, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 21
			poseb1.loc[:] = xp1 - 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 24
			poseb1.loc[:] = xp1 - 0.8, yp1+ r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
				
			frame = 27
			poseb1.loc[:] = xp1 - 0.1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 30
			poseb1.loc[:] = xp1 - 0.2, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 33
			poseb1.loc[:] = xp1 - 0.3, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 36
			poseb1.loc[:] = xp1 - 0.4, yp1 - r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 39
			poseb1.loc[:] = xp1 - 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 42
			poseb1.loc[:] = xp1 - 0.6, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 45
			poseb1.loc[:] = xp1 - 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 48
			poseb1.loc[:] = xp1 - 0.8, yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
		if(direcao_esq == "para-esquerda"): 
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1  + 0.1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1 + 0.2, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 9
			poseb1.loc[:] = xp1 + 0.3 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 + 0.4 , yp1 - r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1 + 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 18
			poseb1.loc[:] = xp1 + 0.6, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 21
			poseb1.loc[:] = xp1 + 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 24
			poseb1.loc[:] = xp1  + 0.8, yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
				
			frame = 27
			poseb1.loc[:] = xp1  + 0.1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 30
			poseb1.loc[:] = xp1 + 0.2, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 33
			poseb1.loc[:] = xp1 + 0.3 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 36
			poseb1.loc[:] = xp1 + 0.4 , yp1 - r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 39
			poseb1.loc[:] = xp1 + 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 42
			poseb1.loc[:] = xp1 + 0.6, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 45
			poseb1.loc[:] = xp1 + 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 48
			poseb1.loc[:] = xp1  + 0.8, yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)			
				
		if(direcao_esq == "para-frente"):
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1+ (r1 * math.sqrt(2) / 2), yp1+ (r1 * math.sqrt(2) / 2), zp1   + 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1 + r1, yp1 , zp1 + 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 9
			poseb1.loc[:] = xp1  + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1 + 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 , yp1- r1, zp1 + 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1- (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1 + 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 18
			poseb1.loc[:] = xp1 - r1, yp1 , zp1+ 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 21
			poseb1.loc[:] = xp1  - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 + 0.7
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 24
			poseb1.loc[:] = xp1 , yp1+ r1, zp1 + 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
				
			frame = 27
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2) , yp1 + (r1 * math.sqrt(2) / 2), zp1+ 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 30
			poseb1.loc[:] = xp1 + r1, yp1 , zp1+ 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 33
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1+ 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 36
			poseb1.loc[:] = xp1, yp1 - r1, zp1+ 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 39
			poseb1.loc[:] = xp1  - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1+ 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 42
			poseb1.loc[:] = xp1 - r1, yp1 , zp1+ 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 45
			poseb1.loc[:] = xp1- (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 + 0.7 
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 48
			poseb1.loc[:] = xp1, yp1 + r1, zp1 + 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
		if(direcao_esq == "para-tras"):
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1 + r1, yp1 , zp1 - 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 9
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 , yp1 - r1, zp1 - 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 18
			poseb1.loc[:] = xp1 - r1, yp1 , zp1 - 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 21
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.7
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 24
			poseb1.loc[:] = xp1 , yp1 + r1, zp1 - 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
			
			frame = 27
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2) , yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1 + r1, yp1 , zp1 - 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 33
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 36
			poseb1.loc[:] = xp1, yp1 - r1, zp1 - 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1  - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 42
			poseb1.loc[:] = xp1 - r1, yp1 , zp1 - 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1- (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.7 
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1, yp1 + r1, zp1 - 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
	
			
	else: #sentido movimento esq = anti-horario
        	if(direcao_esq == "para-baixo"):
			frame = 1
			poseb1.loc[:] = xp1 - r1, yp1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 6
			poseb1.loc[:] = xp1, yp1 - 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 9
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 12
			poseb1.loc[:] = xp1 + r1, yp1 - 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 18
			poseb1.loc[:] = xp1, yp1 - 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 21
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 24
			poseb1.loc[:] = xp1 - r1, yp1 - 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x + r1
			yp1 = poseb1.loc.y
			zp1 = poseb1.loc.z
			
			frame = 27
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1, yp1 - 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 33
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 36
			poseb1.loc[:] = xp1 + r1, yp1 - 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 42
			poseb1.loc[:] = xp1, yp1 - 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1 - r1, yp1 - 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
		if(direcao_esq == "para-cima"):
			frame = 1
			poseb1.loc[:] = xp1 - r1, yp1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
	
			frame = 3
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 6
			poseb1.loc[:] = xp1, yp1 + 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 9
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 12
			poseb1.loc[:] = xp1 + r1, yp1 + 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 15
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 18
			poseb1.loc[:] = xp1, yp1 + 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 21
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 24
			poseb1.loc[:] = xp1 - r1, yp1 + 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
	
			xp1 = poseb1.loc.x + r1
			yp1 = poseb1.loc.y
			zp1 = poseb1.loc.z
			
			frame = 27
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.1, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1, yp1 + 0.2, zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 33
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.3, zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 36
			poseb1.loc[:] = xp1 + r1, yp1 + 0.4, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + 0.5, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 42
			poseb1.loc[:] = xp1, yp1 + 0.6, zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + 0.7, zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1 - r1, yp1 + 0.8, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
	
	
	
		if(direcao_esq == "para-direita"): #inverti os sinais do eixo z para mudar de anti-horario para horario
			
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1 - 0.1, yp1+ (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1 - 0.2, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 9
			poseb1.loc[:] = xp1 - 0.3 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 - 0.4 , yp1- r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1 - 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 18
			poseb1.loc[:] = xp1 - 0.6, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 21
			poseb1.loc[:] = xp1 - 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 24
			poseb1.loc[:] = xp1 - 0.8, yp1+ r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
				
			frame = 27
			poseb1.loc[:] = xp1 - 0.1, yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 30
			poseb1.loc[:] = xp1 - 0.2, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 33
			poseb1.loc[:] = xp1 - 0.3, yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 36
			poseb1.loc[:] = xp1 - 0.4, yp1 - r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 39
			poseb1.loc[:] = xp1 - 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 42
			poseb1.loc[:] = xp1 - 0.6, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 45
			poseb1.loc[:] = xp1 - 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 48
			poseb1.loc[:] = xp1 - 0.8, yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
		if(direcao_esq == "para-esquerda"): 
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1  + 0.1, yp1+ (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1+ 0.2, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 9
			poseb1.loc[:] = xp1+ 0.3 , yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 + 0.4 , yp1- r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 15
			poseb1.loc[:] = xp1+ 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 18
			poseb1.loc[:] = xp1+ 0.6, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 21
			poseb1.loc[:] = xp1 + 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 24
			poseb1.loc[:] = xp1  + 0.8, yp1+ r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
				
			frame = 27
			poseb1.loc[:] = xp1 + 0.1, yp1 + (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 30
			poseb1.loc[:] = xp1+ 0.2, yp1 , zp1 - r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 33
			poseb1.loc[:] = xp1 + 0.3, yp1 - (r1 * math.sqrt(2) / 2), zp1 - (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 36
			poseb1.loc[:] = xp1+ 0.4, yp1 - r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 39
			poseb1.loc[:] = xp1+ 0.5 , yp1 - (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 42
			poseb1.loc[:] = xp1+ 0.6, yp1 , zp1 + r1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1+ 0.7 , yp1 + (r1 * math.sqrt(2) / 2), zp1 + (r1 * math.sqrt(2) / 2)
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 48
			poseb1.loc[:] = xp1 + 0.8, yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
				
		if(direcao_esq == "para-frente"):
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1- (r1 * math.sqrt(2) / 2), yp1+ (r1 * math.sqrt(2) / 2), zp1   + 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
					
			frame = 6
			poseb1.loc[:] = xp1 - r1, yp1 , zp1 + 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 9
			poseb1.loc[:] = xp1  - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1 + 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 12
			poseb1.loc[:] = xp1 , yp1- r1, zp1 + 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 15
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1 + 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 18
			poseb1.loc[:] = xp1 + r1, yp1 , zp1+ 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 21
			poseb1.loc[:] = xp1  + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 + 0.7
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 24
			poseb1.loc[:] = xp1 , yp1+ r1, zp1 + 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
			
			frame = 27
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2) , yp1 + (r1 * math.sqrt(2) / 2), zp1+ 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1 - r1, yp1 , zp1+ 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 33
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1+ 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 36
			poseb1.loc[:] = xp1, yp1 - r1, zp1+ 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1  + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1+ 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 42
			poseb1.loc[:] = xp1 + r1, yp1 , zp1+ 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 45
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 + 0.7 
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1, yp1 + r1, zp1 + 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
		if(direcao_esq == "para-tras"):
			frame = 1
			poseb1.loc[:] = xp1 , yp1 + r1, zp1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 3
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
				
			frame = 6
			poseb1.loc[:] = xp1 - r1, yp1 , zp1 - 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 9
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 12
			poseb1.loc[:] = xp1 , yp1 - r1, zp1 - 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 15
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 18
			poseb1.loc[:] = xp1 + r1, yp1 , zp1 - 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 21
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.7
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 24
			poseb1.loc[:] = xp1 , yp1 + r1, zp1 - 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			xp1 = poseb1.loc.x 
			yp1 = poseb1.loc.y - r1
			zp1 = poseb1.loc.z
			
			frame = 27
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2) , yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.1
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 30
			poseb1.loc[:] = xp1 - r1, yp1 , zp1 - 0.2
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 33
			poseb1.loc[:] = xp1 - (r1 * math.sqrt(2) / 2) , yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.3
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 36
			poseb1.loc[:] = xp1, yp1 - r1, zp1 - 0.4
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 39
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 - (r1 * math.sqrt(2) / 2), zp1 - 0.5
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
		
			frame = 42
			poseb1.loc[:] = xp1 + r1, yp1 , zp1 - 0.6
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 45
			poseb1.loc[:] = xp1 + (r1 * math.sqrt(2) / 2), yp1 + (r1 * math.sqrt(2) / 2), zp1 - 0.7 
			poseb1.insertKey(arm, frame, Object.Pose.LOC)
			
			frame = 48
			poseb1.loc[:] = xp1, yp1 + r1, zp1 - 0.8
			poseb1.insertKey(arm, frame, Object.Pose.LOC)	
	
	#MOVIMENTO COM AS DUAS MAOS
	#Configurando expressão facial do sinal escolhida
	print "Mov duas Maos - "
	print expressao_facial
	
	for i in range(0 , len(listaExpressaoFacial), 1):
		if (listaExpressaoFacial[i].split()): #Split em cada linha			
	  		if (listaExpressaoFacial[i].split()[0] == expressao_facial):
	  			#print listaExpressaoFacial[i].split()[0];
				for k in range(i , i+int(listaExpressaoFacial[i].split()[-1]), 1): 
	        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
	        			#print bone;
					bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
					bone.insertKey(arm, frame/2, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(arm, frame/2, Object.Pose.ROT)
	        		
else:
	exp_facial = parametrosEsquerda[1]
	expressao_facial = substr(exp_facial, 0, len(exp_facial) - 1)
	print "Mov left HAND = "	
	print expressao_facial;	
	#Configurando expressão facial do sinal escolhida
	for i in range(0 , len(listaExpressaoFacial), 1):
		if (listaExpressaoFacial[i].split()): #Split em cada linha			
	  		if (listaExpressaoFacial[i].split()[0] == expressao_facial):
	  			#print listaExpressaoFacial[i].split()[0];
				for k in range(i , i+int(listaExpressaoFacial[i].split()[-1]), 1): 
	        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
	        			#print bone;
					bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
					bone.insertKey(arm, frame/2, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(arm, frame/2, Object.Pose.ROT)
	
	
		
nomeVideoTemp = substr(nomeVideo, 0, len(nomeVideo) - 1)
print nomeVideoTemp
	
cena = Blender.Scene.GetCurrent()
cont = cena.getRenderingContext()
cont.renderPath = "//"+nomeVideoTemp+"_"
cont.sFrame = 1
cont.eFrame = frame
cont.renderAnim()


sub.Popen("ffmpeg -i "+ nomeVideoTemp+ "*.avi -y -b 800 -r 25 -f flv -vcodec flv -acodec mp3 -ab 128 -ar 44100 "+ nomeVideoTemp+".flv",shell=True,stdout=sub.PIPE).stdout.readlines()

#temp = commands.getoutput('ls $HOME/Projetos/ProjetoLibras/server/ScriptsPython | grep convertido')

temp1 = commands.getoutput('ls /home/linear/Projetos/ProjetoLibras/server/ScriptsPython | grep '+nomeVideoTemp + '*.avi')
videoAVIrenomeado = nomeVideoTemp + '.avi';
os.rename(temp1,  videoAVIrenomeado);

#nomeVideoConvertido = substr(nomeVideo, 0, len(nomeVideo) - 1)
#nomeDoSinal =  nomeVideo + '.flv';
#os.rename(temp,  nomeDoSinal);

Blender.Quit()

