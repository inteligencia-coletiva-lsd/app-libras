libPA_Dir = open("LibPontoArticulacaoDir","r")
listaPA_Dir = libPA_Dir.readlines()

def pontoArt(ponto):
	pa = [[]]
	for i in range(0, len(listaPA_Dir),1):
		if len(listaPA_Dir[i]) < 20 : 
			pa.append([])
		else:
			pa[-1].append(listaPA_Dir[i])
	return pa[ponto]

libPA_Dir.close()
