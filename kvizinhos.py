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

	# representacao do objeto na forma de string
	def __repr__(self):
		return(str(self.nome) + " " + str(self.x) + " " + str(self.y) + " " + str(self.cluster))

	# converte para a forma de string para imprimir no arquivo de saida
	def saida(self):
		return(str(self.nome) + " " + str(self.cluster))

	# calcula a distancia do objeto até um dado ponto 
	def distancia(self, x, y):
		dx = self.x - x
		dy = self.y - y

		return math.sqrt( dx ** 2 + dy ** 2 )

	# Retorno o indice do melhor centroide
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
# Realiza a leitura do conjunto de dados do arquivo entrada
def lerConjuntoDeDados(caminho, conjuntoDados):
	with open(caminho) as arq:
		cabecalho = arq.readline()

		for linha in arq:
			valores = linha.split()
			#print(valores)
			conjuntoDados.append( Objeto(valores[0], float(valores[1]), float(valores[2])) )

# Realiza a leitura do arquivo com os valores corretos das classes
def lerConjuntoDadosReal(caminho, conjuntoDadosReal):
	with open(caminho) as arq:

		for linha in arq:
			valores = linha.split()
			#print(valores)
			conjuntoDadosReal.append( (valores[0], float(valores[1]))  )


#########################################
# Escreve arquivo de saida
#########################################
# Escreve os objetos da partão no arquivo de saida
def escreveParticaoArquivo(caminho, conjuntoDadosReal):
	with open(caminho, 'w') as arq:
		for dado in conjuntoDadosReal:
			arq.write(dado.saida() + "\n")


#########################################
# Iteracao para recalcular centroides
#########################################
# Código que executa a lógica do k-vizinhos a cada iteração
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

	numClusters = (int(input("Digite o valor de k: ")))
	maxInteracoes = (int(input("Digite o numero de iteracoes: ")))

	conjuntoDadosReal = []
	lerConjuntoDadosReal('../datasets/c2ds1-2spReal.clu', conjuntoDadosReal)

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

	# Escolhe os k primeiros objetos como centróides
	centroides = []

	for i in range(numClusters):
		centroides.append((conjuntoDados[i+1].x, conjuntoDados[i+1].y))

	for i in range(maxInteracoes):
		agrupar(numClusters, conjuntoDados, centroides)

	# vetor de resultados para calcula AR
	resultado = []
	for dado in conjuntoDados:
		resultado.append(dado.cluster)

	# vetor com os valores esperados para calcular AR
	esperado = []
	for dado in conjuntoDadosReal:
		esperado.append(int(dado[1]))
		
	# calcula Ar
	indiceRand = adjusted_rand_score(resultado, esperado)
	print("AR: " + str(indiceRand))

	escreveParticaoArquivo('c2ds1-2spK' + str(numClusters) + '.txt', conjuntoDados)


if __name__ == "__main__":
    main()








		