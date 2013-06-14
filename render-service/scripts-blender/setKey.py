libPA_Dir = open("Libs/LibPontoArticulacaoDir","r")
listaPA_Dir = libPA_Dir.readlines()
libPA_Dir.close()

libOrient_Dir = open("Libs/LibOrientacaoDir","r")
listaOrient_Dir = libOrient_Dir.readlines() 
libOrient_Dir.close()

libConfigMao_Dir = open("Libs/LibConfigMaoDir","r")
listaConfigMao_Dir = libConfigMao_Dir.readlines() 
libConfigMao_Dir.close()


def pontoArt(p):
	pa = [[]]
	for i in range(0, len(listaPA_Dir),1):
		if len(listaPA_Dir[i]) < 20 : 
			pa.append([])
		else:
			pa[-1].append(listaPA_Dir[i])
	return pa[p]


def orient(o):
	ori = [[]]
	for i in range(0, len(listaOrient_Dir),1):
		if len(listaOrient_Dir[i]) < 20 : 
			ori.append([])
		else:
			ori[-1].append(listaOrient_Dir[i])
	return ori[o]

def confMao(c):
	conf = [[]]
	for i in range(0, len(listaConfigMao_Dir),1):
		if len(listaConfigMao_Dir[i]) < 20 : 
			conf.append([])
		else:
			conf[-1].append(listaConfigMao_Dir[i])
	return conf[c]
