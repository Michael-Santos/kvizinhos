#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
import random
from sklearn.metrics.cluster import adjusted_rand_score

#########################################
# Dado de entrada
#########################################
class Objeto():
	def __init__(self, nome, x, y):
		self.nome = nome
		self.x = x
		self.y = y
		self.cluster = -1

	def __repr__(self):
		return(str(self.nome) + " " + str(self.x) + " " + str(self.y) + " " + str(self.cluster))

	def distancia(self, x, y):
		dx = self.x - x
		dy = self.y - y

		return math.sqrt( dx ** 2 + dy ** 2 )

	def melhorCentroid(self, centroides):
		menorDistancia = 999999999999;
		melhorIndice = 0;

		for indice, centroide in enumerate(centroides):
			distancia = self.distancia(centroide[0], centroide[1])
			
			if distancia < menorDistancia:
				menorDistancia = distancia
				melhorIndice = indice

		return melhorIndice


#########################################
# Lê arquivos de entrada
#########################################
def lerConjuntoDeDados(caminho, conjuntoDados):
	with open(caminho) as arq:
		cabecalho = arq.readline()

		for linha in arq:
			valores = linha.split()
			#print(valores)
			conjuntoDados.append( Objeto(valores[0], float(valores[1]), float(valores[2])) )


def lerConjuntoDadosReal(caminho, conjuntoDadosReal):
	with open(caminho) as arq:

		for linha in arq:
			valores = linha.split()
			#print(valores)
			conjuntoDadosReal.append( (valores[0], float(valores[1]))  )


#########################################
# Iteracao para recalcular centroides
#########################################
def agrupar(numClusters, conjuntoDados, centroides):
	# Associa cada objeto ao cluster com centróide mais próximo 
	for dado in conjuntoDados:
		dado.cluster = dado.melhorCentroid(centroides)


	# Recalcular os centróides
	vetoresTemporariosParaCadaCluster = []

	for centroide in centroides:
		vetoresTemporariosParaCadaCluster.append([])

	for indice, dado in enumerate(conjuntoDados):
		vetoresTemporariosParaCadaCluster[dado.cluster].append(indice)

	for indice, vetor in enumerate(vetoresTemporariosParaCadaCluster):
		somax = 0
		somay = 0

		for objeto in vetor:
			somax = somax + conjuntoDados[objeto].x
			somay = somay + conjuntoDados[objeto].y

		centroides[indice] = (somax/len(vetor), somay/len(vetor))

#########################################
# Lê entrada e executa o agrupamento
#########################################
def main():
	numClusters = 2
	maxInteracoes = 10


	conjuntoDadosReal = []
	lerConjuntoDadosReal('../datasets/c2ds1-2spReal.clu', conjuntoDadosReal)

	print(len(conjuntoDadosReal))

	conjuntoDados = []
	lerConjuntoDeDados('../datasets/c2ds1-2sp.txt', conjuntoDados);
	
	'''
	conjuntoDados = [
		Objeto("c2sp1s1", 10.5, 9),
		Objeto("c2sp1s2", 10.56717, 9.268445),
		Objeto("c2sp1s3", 8.27532, 11.38221),
		Objeto("c2sp1s4", 8.227458, 11.37764),
		Objeto("c2sp1s5", 8.179511, 11.37211),
		Objeto("c2sp1s6", 8.1315, 11.36561),
		Objeto("c2sp1s7", 8.083443, 11.35814),
		Objeto("c2sp1s8", 8.035361, 11.3497),
		Objeto("c2sp1s9", 7.98727, 11.34027),
		Objeto("c2sp1s10", 7.9392, 11.32987)
	]
	'''

	#exit()

	centroides = []

	for i in range(numClusters):
		centroides.append((conjuntoDados[i+1].x, conjuntoDados[i+1].y))

	for i in range(maxInteracoes):
		agrupar(numClusters, conjuntoDados, centroides)

	#	for objeto in conjuntoDados:
	#		print(repr(objeto))
	#	print("\n\n\n")

	for objeto in conjuntoDados:
		break
		#print(repr(objeto))


	# prepara vetores para calcula AR

	resultado = []
	for dado in conjuntoDados:
		resultado.append(dado.cluster)

	
	esperado = []
	for dado in conjuntoDadosReal:
		esperado.append(int(dado[1]))
		
	indiceRand = adjusted_rand_score(resultado, esperado)
	print("AR: " + str(indiceRand))


if __name__ == "__main__":
    main()








		