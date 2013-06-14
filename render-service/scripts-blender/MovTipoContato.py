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
#paramEsq = sys.argv[6]

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
#arquivoEsquerda = open(paramEsq, "r")
#parametrosEsquerda = arquivoEsquerda.readlines();

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

tipoContato = parametrosDireita[3]
tipoContato = tipoContato[:-1]
print tipoContato

expFacial = parametrosDireita[4]
expFacial = expFacial[:-1]
print expFacial

nomeSinal = parametrosDireita[5]
nomeSinal = nomeSinal[:-1]
print nomeSinal

if(tipoContato == "coçar"):
	endFrame = 55;

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

	#Configuracao de mao direita
	configuracoesMao = ["conf_1", "conf_59"];
	
	#Configuracao de mao direita
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configuracoesMao[0]): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, 20, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 20, Object.Pose.ROT)

		#Configuracao de mao direita
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configuracoesMao[1]): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, 27, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 27, Object.Pose.ROT)

		#Configuracao de mao direita
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configuracoesMao[0]): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, 34, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 34, Object.Pose.ROT)

		#Configuracao de mao direita
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configuracoesMao[1]): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, 41, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 41, Object.Pose.ROT)

		#Configuracao de mao direita
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configuracoesMao[0]): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, 48, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 48, Object.Pose.ROT)

		#Configuracao de mao direita
	for i in range(0 , len(listaPoseMaoDireita), 1):
		if (listaPoseMaoDireita[i].split()):
			if (listaPoseMaoDireita[i].split()[0] == configuracoesMao[1]): 
				for k in range(i , i+15, 1): 
					bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
					bone.insertKey(armadura, 55, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 55, Object.Pose.ROT)

	#Define a orientacao da mao direita
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
	
	#Ponto de articulacao da mao direita
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

	#Ponto de articulacao da mao direita
	for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
			if (listalibPontoArticulacaoDireita[i].split()): 			
		  		if (listalibPontoArticulacaoDireita[i].split()[0] == paDir):
					for k in range(i , i+2, 1): 
		        			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
						bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
						bone.insertKey(armadura, 55, Object.Pose.LOC)
		        			euler = bone.quat.toEuler()
		        			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
		        			bone.quat = euler.toQuat()
		        			bone.insertKey(armadura, 55, Object.Pose.ROT)

	#Pose Padrao inicial
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

else:
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
	xp = poseb.loc.x
	yp = poseb.loc.y
	zp = poseb.loc.z

	frame = 0;
	if(tipoContato == 'tocar'):

		frame = 25
		poseb.loc[:] = xp , yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 30
		poseb.loc[:] = xp , yp , zp - 0.4
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 35
		poseb.loc[:] = xp, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 40
		poseb.loc[:] = xp, yp, zp - 0.4
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 45
		poseb.loc[:] = xp, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 50
		poseb.loc[:] = xp, yp, zp - 0.4
		poseb.insertKey(armadura, frame, Object.Pose.LOC)

	if(tipoContato == 'alisar'):
		frame = 25
		poseb.loc[:] = xp , yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 28
		poseb.loc[:] = xp , yp - 0.3 , zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 31
		poseb.loc[:] = xp, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 34
		poseb.loc[:] = xp, yp + 0.3, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 37
		poseb.loc[:] = xp, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 40
		poseb.loc[:] = xp, yp - 0.3, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 43
		poseb.loc[:] = xp, yp, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		frame = 46
		poseb.loc[:] = xp, yp + 0.3, zp
		poseb.insertKey(armadura, frame, Object.Pose.LOC)
		
	
	# Key Frames Pose Padrão Final ----------------------------------------------------------------
	#poseInicial = ["Pose_1", "Pose_2"]
	endFrame = frame;

	print "endFrame = " + str(endFrame);
	
	for i in range(0 , len(listaPosePadrao), 1):
		if (listaPosePadrao[i].split()): 			
			if (listaPosePadrao[i].split()[0] == poseInicial):  
				for k in range(i , int(listaPosePadrao[i].split()[-1]), 1): 
					bone = pose.bones[listaPosePadrao[k+1].split()[0]]	
					bone.loc[:] = float(listaPosePadrao[k+1].split()[2]), float(listaPosePadrao[k+1].split()[3]), float(listaPosePadrao[k+1].split()[4])	
					bone.insertKey(armadura, endFrame + 20, Object.Pose.LOC)
	
       					euler = bone.quat.toEuler()
       					euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])		
       					bone.quat = euler.toQuat()
       					bone.insertKey(armadura, endFrame + 20, Object.Pose.ROT)
	

print endFrame;

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
	
	
