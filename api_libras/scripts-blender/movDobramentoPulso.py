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

arquivoDireita = open(paramDir, "r")
parametrosDireita = arquivoDireita.readlines();
arquivoEsquerda = open(paramEsq, "r")
parametrosEsquerda = arquivoEsquerda.readlines();

act = Armature.NLA.NewAction("TESTE")
act.setActive(armadura)

configDir = parametrosDireita[0]
ponto_articulacao_dir = parametrosDireita[1]
tipo_dobramento_dir = parametrosDireita[2]
flag_rep = parametrosDireita[3]
direcao_dir = parametrosDireita[4]
nomeVideo = parametrosDireita[5]

config_mao_direita = substr(configDir, 0, len(configDir) - 1)
ponto_articulacao_direita = substr(ponto_articulacao_dir, 0, len(ponto_articulacao_dir) - 1)
tipo_dobramento_direita = substr(tipo_dobramento_dir, 0, len(tipo_dobramento_dir) - 1)

#Configuracao de mao
for i in range(0 , len(listaPoseMaoDireita), 1):
	if (listaPoseMaoDireita[i].split()):
		if (listaPoseMaoDireita[i].split()[0] == config_mao_direita): 
			for k in range(i , i+15, 1): #varrendo todos os ossos da mao
				bone = pose.bones[listaPoseMaoDireita[k+1].split()[0]]
				bone.loc[:] = float(listaPoseMaoDireita[k+1].split()[2]), float(listaPoseMaoDireita[k+1].split()[3]), float(listaPoseMaoDireita[k+1].split()[4])				
				bone.insertKey(armadura, 1, Object.Pose.LOC)
				euler = bone.quat.toEuler()
				euler[:] = float(listaPoseMaoDireita[k+1].split()[6]), float(listaPoseMaoDireita[k+1].split()[7]), float(listaPoseMaoDireita[k+1].split()[8])				
				bone.quat = euler.toQuat()
				bone.insertKey(armadura, 1, Object.Pose.ROT)

#Ponto de articulacao da mao direita
for i in range(0 , len(listalibPontoArticulacaoDireita), 1):
	if (listalibPontoArticulacaoDireita[i].split()): #Split em cada linha			
		if (listalibPontoArticulacaoDireita[i].split()[0] == ponto_articulacao_direita):
			for k in range(i , i+2, 1): 
	       			bone = pose.bones[listalibPontoArticulacaoDireita[k+1].split()[0]]		
				bone.loc[:] = float(listalibPontoArticulacaoDireita[k+1].split()[2]), float(listalibPontoArticulacaoDireita[k+1].split()[3]), float(listalibPontoArticulacaoDireita[k+1].split()[4])
				bone.insertKey(armadura, 10, Object.Pose.LOC)
	       			euler = bone.quat.toEuler()
	       			euler[:] = float(listalibPontoArticulacaoDireita[k+1].split()[6]), float(listalibPontoArticulacaoDireita[k+1].split()[7]), float(listalibPontoArticulacaoDireita[k+1].split()[8])
	       			bone.quat = euler.toQuat()
	       			bone.insertKey(armadura, 10, Object.Pose.ROT)
	       			
# Key Frames Pose Padrão Inicial e Final ----------------------------------------------------------------
for i in range(0 , len(listaPosePadrao), 1):
	if (listaPosePadrao[i].split()): #Split em cada linha			
  		if (listaPosePadrao[i].split()[0] == "Pose_1"):  			
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
				bone.insertKey(armadura, 45, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 45, Object.Pose.ROT)

		if (listaPosePadrao[i].split()[0] == "Pose_2"):  			
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
				bone.insertKey(armadura, 45, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listaPosePadrao[k+1].split()[6]), float(listaPosePadrao[k+1].split()[7]), float(listaPosePadrao[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 45, Object.Pose.ROT)	       			

temp = parametrosEsquerda[0]
temporario = substr(temp, 0, len(temp) - 1)


if(temporario != 'Nenhum'):
	configEsq = parametrosEsquerda[0]
	ponto_articulacao_esq = parametrosEsquerda[1]
	tipo_dobramento_esq = parametrosEsquerda[2]
	flag_rep1 = parametrosEsquerda[3]
	direcao_esq = parametrosEsquerda[4]
	#exp = parametrosEsquerda[5]

	config_mao_esquerda = substr(configEsq, 0, len(configEsq) - 1)
	ponto_articulacao_esquerda = substr(ponto_articulacao_esq, 0, len(ponto_articulacao_esq) - 1)
	tipo_dobramento_esquerda = substr(tipo_dobramento_esq , 0, len(tipo_dobramento_esq ) - 1)
	#expressao_facial = substr(exp, 0, len(exp) - 1)
	
	print config_mao_esquerda;
	print ponto_articulacao_esquerda;
	print tipo_dobramento_esquerda;
	#print expressao_facial;

	#Config da mao esquerda
	for i in range(0 , len(listaPoseMaoEsquerda), 1):
		if (listaPoseMaoEsquerda[i].split()):			
			if (listaPoseMaoEsquerda[i].split()[0] == config_mao_esquerda): 
				for k in range(i , i+15, 1): #varrendo todos os ossos da mao
					bone = pose.bones[listaPoseMaoEsquerda[k+1].split()[0]]
					bone.loc[:] = float(listaPoseMaoEsquerda[k+1].split()[2]), float(listaPoseMaoEsquerda[k+1].split()[3]), float(listaPoseMaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 1, Object.Pose.LOC)
					euler = bone.quat.toEuler()
					euler[:] = float(listaPoseMaoEsquerda[k+1].split()[6]), float(listaPoseMaoEsquerda[k+1].split()[7]), float(listaPoseMaoEsquerda[k+1].split()[8])
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 1, Object.Pose.ROT)
	
	#Ponto de articulacao da mao esquerda
	for i in range(0 , len(listalibPontoArticulacaoEsquerda), 1):
		if (listalibPontoArticulacaoEsquerda[i].split()):
			if (listalibPontoArticulacaoEsquerda[i].split()[0] == ponto_articulacao_esquerda):
				for k in range(i , i+2, 1): 
	        			bone = pose.bones[listalibPontoArticulacaoEsquerda[k+1].split()[0]]		
	        			bone.loc[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[2]), float(listalibPontoArticulacaoEsquerda[k+1].split()[3]), float(listalibPontoArticulacaoEsquerda[k+1].split()[4])
					bone.insertKey(armadura, 10, Object.Pose.LOC)
	        			euler = bone.quat.toEuler()
	        			euler[:] = float(listalibPontoArticulacaoEsquerda[k+1].split()[6]), float(listalibPontoArticulacaoEsquerda[k+1].split()[7]), float(listalibPontoArticulacaoEsquerda[k+1].split()[8])
	        			bone.quat = euler.toQuat()
	        			bone.insertKey(armadura, 10, Object.Pose.ROT)
	
	if(tipo_dobramento_esquerda == "para-cima"):
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoEsquerdo[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == "Ori_4"):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura, 10, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 10, Object.Pose.ROT)					
	
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == "Ori_3"):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura, 18, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 18, Object.Pose.ROT)
					
	if(tipo_dobramento_esquerda == "para-baixo"):
		for i in range(0 , len(listalibOritentacaoLadoEsquerdo), 1):
			if (listalibOritentacaoLadoEsquerdo[i].split()):
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == "Ori_3"):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura, 10, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 10, Object.Pose.ROT)					
	
				if (listalibOritentacaoLadoEsquerdo[i].split()[0] == "Ori_4"):	
					for k in range(i , i+2, 1):	
						bone = pose.bones[listalibOritentacaoLadoEsquerdo[k+1].split()[0]]					
						bone.loc[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[2]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[3]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[4])					
						bone.insertKey(armadura, 18, Object.Pose.LOC)
						euler = bone.quat.toEuler()					
						euler[:] = float(listalibOritentacaoLadoEsquerdo[k+1].split()[6]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[7]), float(listalibOritentacaoLadoEsquerdo[k+1].split()[8])					
						bone.quat = euler.toQuat()
						bone.insertKey(armadura, 18, Object.Pose.ROT)
        				       			
			
if(tipo_dobramento_direita == "para-cima"):
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == "Ori_4"):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, 10, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 10, Object.Pose.ROT)					
	
			if (listalibOritentacaoLadoDireito[i].split()[0] == "Ori_3"):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, 18, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 18, Object.Pose.ROT)
					
if(tipo_dobramento_direita == "para-baixo"):
	for i in range(0 , len(listalibOritentacaoLadoDireito), 1):
		if (listalibOritentacaoLadoDireito[i].split()):
			if (listalibOritentacaoLadoDireito[i].split()[0] == "Ori_3"):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, 10, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 10, Object.Pose.ROT)					
	
			if (listalibOritentacaoLadoDireito[i].split()[0] == "Ori_4"):	
				for k in range(i , i+2, 1):	
					bone = pose.bones[listalibOritentacaoLadoDireito[k+1].split()[0]]					
					bone.loc[:] = float(listalibOritentacaoLadoDireito[k+1].split()[2]), float(listalibOritentacaoLadoDireito[k+1].split()[3]), float(listalibOritentacaoLadoDireito[k+1].split()[4])					
					bone.insertKey(armadura, 18, Object.Pose.LOC)
					euler = bone.quat.toEuler()					
					euler[:] = float(listalibOritentacaoLadoDireito[k+1].split()[6]), float(listalibOritentacaoLadoDireito[k+1].split()[7]), float(listalibOritentacaoLadoDireito[k+1].split()[8])					
					bone.quat = euler.toQuat()
					bone.insertKey(armadura, 18, Object.Pose.ROT)
					
if(temporario == "Nenhum"): 	
	exp_facial = parametrosEsquerda[1];
	expressao_facial = substr(exp_facial, 0, len(exp_facial) - 1);
else:
	exp_facial = parametrosEsquerda[len(parametrosEsquerda) - 1];
	expressao_facial = substr(exp_facial, 0, len(exp_facial) - 1);
	
# Key Frames Expressao Facial ---------------------------------------------------------------------
for i in range(0 , len(listaExpressaoFacial), 1):
	if (listaExpressaoFacial[i].split()): #Split em cada linha			
  		if (listaExpressaoFacial[i].split()[0] == "Exp_9"):
  			for k in range(i , i+ int(listaExpressaoFacial[i].split()[-1]), 1): 
        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
        			bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
				bone.insertKey(armadura, 1, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 1, Object.Pose.ROT)
        			
        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
        			bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
				bone.insertKey(armadura, 22, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 22, Object.Pose.ROT)			
			
		if (listaExpressaoFacial[i].split()[0] == expressao_facial):
  			for k in range(i , i+ int(listaExpressaoFacial[i].split()[-1]), 1): 
        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
        			bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
				bone.insertKey(armadura, 8, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 8, Object.Pose.ROT)
        			
        			bone = pose.bones[listaExpressaoFacial[k+1].split()[0]]		
        			bone.loc[:] = float(listaExpressaoFacial[k+1].split()[2]), float(listaExpressaoFacial[k+1].split()[3]), float(listaExpressaoFacial[k+1].split()[4])
				bone.insertKey(armadura, 15, Object.Pose.LOC)
        			euler = bone.quat.toEuler()
        			euler[:] = float(listaExpressaoFacial[k+1].split()[6]), float(listaExpressaoFacial[k+1].split()[7]), float(listaExpressaoFacial[k+1].split()[8])
        			bone.quat = euler.toQuat()
        			bone.insertKey(armadura, 15, Object.Pose.ROT)			
	
	
#print "Obtendo Nome do Video..."
#dados = open(parametros[0],"r")
listDados = parametrosDireita#.readlines()
#dados.close()

nomeVideoTemp = listDados[len(listDados) - 1]

nomeVideo = substr(nomeVideoTemp, 0, len(nomeVideoTemp) - 1)

# RENDER ------------------------------------------------------------------------------------------
cena = Blender.Scene.GetCurrent()
cont = cena.getRenderingContext()
cont.renderPath = "//"+nomeVideo+"_"
cont.sFrame = 1
cont.eFrame = 40
cont.renderAnim()

#sub.Popen("ffmpeg -i "+ nomeVideo+ "*.avi -y -b 800 -r 25 -f flv -vcodec flv -acodec mp3 -ab 128 -ar 44100 "+ nomeVideo+".flv",shell=True,stdout=sub.PIPE).stdout.readlines()

sub.Popen("ffmpeg -i "+ nomeVideo+ "*.avi -b 2028k -s 640x480 -r 30 -acodec copy "+ nomeVideo+".flv",shell=True,stdout=sub.PIPE).stdout.readlines()

temp1 = commands.getoutput('ls /home/linear/Projetos/ProjetoLibras/server/ScriptsPython | grep '+nomeVideo + '*.avi')

videoAVIrenomeado = nomeVideo + '.avi';
os.rename(temp1,  videoAVIrenomeado);

sub.Popen("rm "+nomeVideo+"Dir"+ " "+ nomeVideo+"Esq",shell=True,stdout=sub.PIPE).stdout.readlines()

Blender.Quit()						
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			

