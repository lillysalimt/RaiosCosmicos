########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####                  Simulação do Detector Gama                    ####
####                       simuGammaMass.py                         ####
####                                                                ####
####             Daniel de Almeida Magalhães Campolina              ####
####                      Lilly Salim Thein                         ####
####                 Thalles Oliveira Campagnani                    ####
####               Jefferson Quintão Campos Duarte                  ####
####                                                                ####
########################################################################

import os #para renomear arquivo e limpar tela
os.system("clear") #Limpa tela
import sys
import numpy as np
import openmc
import matplotlib.pyplot as plt


# Funções para escrita em arquivo
from pprint import pprint

def escreva_comentario(arquivo, comentario = ""):
    # Escreva comantário e salte linha
    arquivo.write(f"#{comentario}\n")

# Função para salvar valores das variáveis em um arquivo python
def escreva_variaveis(arquivo, vertical=False, comentario = None, **kwargs):
    # Se for passado comentário, escreva antes da variável
    if comentario != None:
        arquivo.write(f"#{comentario}\n")

    #Se quiser usar escrita vertical (mais legivel), só use vertical para listas/matrizes pequenas
    if vertical:
        for nome, valor in kwargs.items():
            arquivo.write(f"{nome} = ")
            pprint(valor, stream=arquivo)
            arquivo.write("\n")
    else:
        for nome, valor in kwargs.items():
            arquivo.write(f"{nome} = {repr(valor)}\n")




# --- Seção responsável por executar o experimento ---

import libGammaMass
libGammaMass.simu = True
libGammaMass.plotar = True


# Configurações da simulação
particulas = 10000000
ciclos     = 1

# Configurações de outras geometrias e fonte
## Parâmetros do tarugo (Substituidos se gerados automaticamente)
tarugo_esteira_pos = 0 #centralizado em cima da fonte
tarugo_comprimento = 20
tarugo_largura     = 20
## Variável do estudo
tarugo_altura      = 15.6

## Parâmetros do colimador
colimador_espessura = 2.8 #Espessura nominal do colimador LB-4700
colimador_abertura  = 7.8 #Diametro do detector
colimador_impureza  = 0 #Não foi implementado

## Parãmetros das fontes
fonte_cobalto_intensidade    = 7.4e4 ########### Atividade de 3.7e4 x2 pois são 2 fótons
fonte_raiosCosmicos_mes      = 1
fonte_raiosCosmicos_latitude = 0


## Parametros do detector
detectores_numero           = 1
detectores_altura_meio      = 52.35
detectores_altura_esquerda  = 52.35
detectores_altura_direita   = 52.35

##Parametros concreto
fonte_Concreto_intensidade = 1.59E4           ### multiplicado por 2pi
fonte_raiosCosmicos_intensidade = 4.39E5       ### multiplicado por 2pi

# Cria pasta com data no nome para armazenar os resultados
libGammaMass.mkdir("finalmb_00", data=False, voltar=False)

# Criando reator no OpenMC
detector = libGammaMass.Detector()
# Alterando Geometria
detector.geometria(
    # Valores gerados de acordo com os parâmetros
    tarugo_largura               = tarugo_largura,
    tarugo_altura                = tarugo_altura,
    tarugo_comprimento           = tarugo_comprimento,
    tarugo_esteira_pos           = tarugo_esteira_pos,
    # Repassar o restante dos parâmetros
    colimador_espessura          = colimador_espessura,
    colimador_abertura           = colimador_abertura,
    colimador_impureza           = colimador_impureza,
    fonte_cobalto_intensidade    = fonte_cobalto_intensidade,
    fonte_raiosCosmicos_intensidade =fonte_raiosCosmicos_intensidade,
    fonte_raiosCosmicos_mes      = fonte_raiosCosmicos_mes,
    fonte_raiosCosmicos_latitude = fonte_raiosCosmicos_latitude,
    fonte_Concreto_intensidade   = fonte_Concreto_intensidade,
    detectores_numero            = detectores_numero,
    detectores_altura_meio       = detectores_altura_meio,
    detectores_altura_esquerda   = detectores_altura_esquerda,
    detectores_altura_direita    = detectores_altura_direita
)
# Rodando configurações novamente para atualizar a fonte da simulação e alterar as configurações de simulação
detector.configurações(particulas=particulas, ciclos=ciclos)

detector.plotagem("plot.frontal.yz.png",  "yz", rotacionar = True)
detector.plotagem("plot.lateral.xy.png",  "xy")

# Plotar vista lateral maior caso o tarugo supere a borda de ar
borda_dir_tarugo = tarugo_esteira_pos + tarugo_comprimento / 2
borda_esq_tarugo = abs(tarugo_esteira_pos - tarugo_comprimento / 2)
maior_extensao = max(borda_dir_tarugo, borda_esq_tarugo)
if maior_extensao >= 200:
    referencia_limite = maior_extensao + 10
    detector.plotagem("plot.lateralMaior.xy.png", "xy",width  = (referencia_limite, 200), pixels = (int(referencia_limite * 4), 800))



#Configurações de tallies
intervalos_energias=np.linspace(5e3,2.005e6,101).tolist() # Intervalo de 5KeV a 2MeV dividido em 40 canais
detector.tallies(init=True)     #Iniciar a lista de tallies
#detector.tallies_detector(energia=intervalos_energias, score="flux",         nome="espectroFluxo")           #1
detector.tallies_detector(energia=intervalos_energias, score="pulse-height", nome="espectroPulso")           #2
detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)

# Gerar os arquivos XML e simular
detector.simular()




# --- Seção responsável por extrair resultados dos experimentos ---
if libGammaMass.simu == True: # Somente extraia caso tenha sido realizada as simulações

    # Navegue arquivo por arquivo coletando os resultados
    espectroPulso, espectroPulso_STD =     detector.tallies_detector(get=True,    nome="espectroPulso", score="pulse-height",  file=f"statepoint.{ciclos}.h5")


    with open("resultados_simuVariaTarugo.py", "w") as f:  #### mudar nome para separar os casos
        escreva_comentario(f," Resultados da Simulação OpenMC - Função simuVariaTarugo\n\n")
        escreva_comentario(f," Arquivo gerado automaticamente\n\n")
        escreva_variaveis(f," Configurações de simulação:", particulas=particulas,  ciclos=ciclos)
        escreva_comentario(f," Configurações de geometria e fonte:")
        escreva_variaveis(f,"# Parâmetros do colimador:",  colimador_espessura=colimador_espessura, colimador_abertura=colimador_abertura, colimador_impureza=colimador_impureza)
        escreva_variaveis(f,"# Parãmetros das fontes", fonte_cobalto_intensidade=fonte_cobalto_intensidade, fonte_raiosCosmicos_mes=fonte_raiosCosmicos_mes, fonte_raiosCosmicos_latitude=fonte_raiosCosmicos_latitude)
        escreva_variaveis(f,"# Parametros do detector", detectores_numero=detectores_numero, detectores_altura_meio=detectores_altura_meio, detectores_altura_esquerda=detectores_altura_esquerda, detectores_altura_direita=detectores_altura_direita)
        escreva_variaveis(f,"# Parametros concreto", fonte_Concreto_intensidade=fonte_Concreto_intensidade)
        escreva_comentario(f," Espectro para resultados:")
        escreva_variaveis(f," Intervalos de energias que são divididos os tallies de fluxo e altura de pulso", intervalos_energias=intervalos_energias)
        escreva_comentario(f," Resultados:\n\n")
        escreva_variaveis(f,"# Espectro de pulso",espectroPulso=espectroPulso)
        escreva_variaveis(f,"# Espectro de desvio padrão",espectroPulso_STD=espectroPulso_STD)
      
        