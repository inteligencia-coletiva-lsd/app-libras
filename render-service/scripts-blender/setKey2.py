libPaFiles = ["Libs/LibPontoArticulacaoDir", "Libs/LibPontoArticulacaoEsq"]
libOrientFiles = ["Libs/LibOrientacaoDir", "Libs/LibOrientacaoEsq"]
libConfMaoFiles = ["Libs/LibConfigMaoDir", "Libs/LibConfigMaoEsq"]

def pontoArt(p, lado):
	libPA = open(libPaFiles[lado], "r")
	listaPA = libPA.readlines()
	libPA.close()
	pa = [[]]
	for i in range(0, len(listaPA),1):
		if (listaPA[i].split()[0].find("Pa_") != -1) : 
			pa.append([])
		else:
			pa[-1].append(listaPA[i])
	return pa[p]

def orient(o, lado):
	libOrient = open(libOrientFiles[lado], "r")
	listaOrient = libOrient.readlines()
	libOrient.close()
	ori = [[]]
	for i in range(0, len(listaOrient),1):
		if (listaOrient[i].split()[0].find("Ori_") != -1 ) : 
			ori.append([])
		else:
			ori[-1].append(listaOrient[i])
	return ori[o]

def confMao(c, lado):
	libConfMao = open(libConfMaoFiles[lado], "r")
	listaConfMao = libConfMao.readlines()
	libConfMao.close()
	conf = [[]]
	for i in range(0, len(listaConfMao),1):
		if (listaConfMao[i].split()[0].find("conf_")) != -1 : 
			conf.append([])
		else:
			conf[-1].append(listaConfMao[i])
	return conf[c]
