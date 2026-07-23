########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####   Bibliteca para variar automáticamente a geometria do tarugo  ####
####                      libVariaTarugo.py                         ####
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


def simuVariaTarugo(
        # Configurações de variação
        ini=None,
        fin=None,
        passo=None,
        tipoVaria="area", #Outras opções: proporção, posição, largura, altura, comprimento, area+sequencia, area+aleatorio
        vetor_varia = None,
        area = None,
        prop = 1,
        
        # Configurações de outras variações [tarugo_comprimento, prop]
        ## apenas para area+sequencia
        matriz_sequencia = None, #inf linhas por 3 colunas
        ## Apenas para area+aleatorio
        vetor_lim_inf = [  10, 0.5 ],
        vetor_lim_sup = [ 200,   2 ],


        # Controle de pastas, para se deve voltar uma pasta acima antes de criar
        voltar=False,
        
        # Configurações da simulação
        particulas = 100000,
        ciclos     = 100,

        # Configurações de outras geometrias e fonte
        ## Parâmetros do tarugo (Substituidos se gerados automaticamente)
        tarugo_esteira_pos = 0, #centralizado em cima da fonte
        tarugo_comprimento = 10,
        tarugo_largura     = 10,
        tarugo_altura      = 10,

        ## Parâmetros do colimador
        colimador_espessura = 2.8, #Espessura nominal do colimador LB-4700
        colimador_abertura  = 7.8, #Diametro do detector
        colimador_impureza  = 0,
        
        ## Parãmetros das fontes
        fonte_cobalto_intensidade    = 7.4e6, ########### Atividade de 3.7e7 x2 pois são 2 fótons
        fonte_raiosCosmicos_mes      = 1,
        fonte_raiosCosmicos_latitude = 0,
        
        ## Parametros do detector
        detectores_numero           = 1,
        detectores_altura_meio      = 52.35,
        detectores_altura_esquerda  = 52.35,
        detectores_altura_direita   = 52.35,

        ##Parametros concreto
        fonte_Concreto_intensidade = 1.59e4           ### multiplicado por 1,57 área da semi-esfera
        ):
    
    # Cria pasta com data no nome para armazenar os resultados
    libGammaMass.mkdir("resultados_"+str(int(fonte_cobalto_intensidade))+"_"+str(int(colimador_espessura*10)), data=False, voltar=voltar)

    if vetor_varia is not None:#Se vetor_veria estiver definido, ignore valores passados como parametros que são usados para gerar vetor_varia
        ini=None
        fin=None
        passo=None
    else:#Se vetor varia estiver vazio, gere altomaticamente conforme valores passados
        vetor_varia = np.arange(ini, fin + passo/1000.0, passo)
        
        if tipoVaria == "proporção": #Se o tipo for proporção, gere pontos simetricamente em torno de 1
            sequencia_lado_esquerdo = np.sort(1 / vetor_varia[1:])
            vetor_varia = np.concatenate((sequencia_lado_esquerdo, vetor_varia))
        vetor_varia = vetor_varia.tolist()
        
    #Declare a variável sequência, no caso de "area+sequencia"
    if tipoVaria == "area+sequencia":
        sequencia = 0
            

    # Vetor para salvar o histórico de dimensões do tarugo
    vetor_prop = []
    vetor_area = []
    vetor_tarugo_largura = []
    vetor_tarugo_altura = []
    vetor_tarugo_comprimento = []
    vetor_tarugo_esteira_pos = []

    
    # Realize as diversas simulações com a variação respectiva
    voltar = False
    for varia in vetor_varia:
        # Crie uma pasta para cada variação, sem data.
        libGammaMass.mkdir(f"simulação_{varia:.4f}", data=False, voltar=voltar)#Voltar é false apenas para a primeira execução
        voltar = True
        
        print("################")
        print("######## Rodando variação: ")
        print(f"####### {tipoVaria} = {varia} ")
        print("################")

        # Gera dimensões do tarugo de acordo com o tipo de variação
        if tipoVaria == "area":
            tarugo_largura      = np.sqrt(varia*prop)
            tarugo_altura       = np.sqrt(varia/prop)
            
        elif tipoVaria == "area+sequencia":
            tarugo_comprimento  = matriz_sequencia[sequencia][0]
            prop_seq            = matriz_sequencia[sequencia][1]
            tarugo_largura      = np.sqrt(varia*prop_seq)
            tarugo_altura       = np.sqrt(varia/prop_seq)
            # Controle da variável sequência: incremente 1 e reinicie caso supere o tamanho do vetor sequência
            sequencia=sequencia+1
            if sequencia >= len(matriz_sequencia):
                sequencia=0
            
            
        elif tipoVaria == "area+aleatorio":
            tarugo_esteira_pos, tarugo_comprimento, prop_ale = np.random.uniform(vetor_lim_inf, vetor_lim_sup)
            tarugo_largura      = np.sqrt(varia*prop_ale)
            tarugo_altura       = np.sqrt(varia/prop_ale)


        elif tipoVaria == "proporção":
            tarugo_largura  = np.sqrt(area*varia)
            tarugo_altura   = np.sqrt(area/varia)

        elif tipoVaria == "posição":
            tarugo_esteira_pos           = varia
            if area is not None:
                tarugo_largura      = np.sqrt(area*prop)
                tarugo_altura       = np.sqrt(area/prop)

        elif tipoVaria == "largura":
            tarugo_largura               = varia
            if area is not None:
                tarugo_largura      = np.sqrt(area*prop)
                tarugo_altura       = np.sqrt(area/prop)

        elif tipoVaria == "altura":
            tarugo_altura                = varia
            if area is not None:
                tarugo_largura      = np.sqrt(area*prop)
                tarugo_altura       = np.sqrt(area/prop)

        elif tipoVaria == "comprimento":
            tarugo_comprimento            = varia
            if area is not None:
                tarugo_largura      = np.sqrt(area*prop)
                tarugo_altura       = np.sqrt(area/prop)

        else:
            sys.exit(f"Erro: Tipo de variação '{tipoVaria}' desconhecido.")


        # Salva histórico de dimensões do tarugo
        vetor_tarugo_esteira_pos.append(float(tarugo_esteira_pos))
        vetor_tarugo_comprimento.append(float(tarugo_comprimento))
        if tipoVaria == "area+sequencia":
            vetor_prop.append(float(prop_seq))
        elif tipoVaria == "area+aleatorio":
            vetor_prop.append(float(prop_ale))
        else:
            vetor_prop.append(float(prop))
        vetor_tarugo_largura.append(float(tarugo_largura))
        vetor_tarugo_altura.append(float(tarugo_altura))
        vetor_area.append(float(tarugo_largura*tarugo_altura))

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
        intervalos_energias=np.linspace(5e3,2e6,1000).tolist() # Intervalo de 5KeV a 2MeV dividido em 2¹⁰ canais
        detector.tallies(init=True)     #Iniciar a lista de tallies
        detector.tallies_detector(energia=intervalos_energias, score="flux",         nome="espectroFluxo")           #1
        detector.tallies_detector(energia=intervalos_energias, score="pulse-height", nome="espectroPulso")           #2
        detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)

        # Gerar os arquivos XML e simular
        detector.simular()




    # --- Seção responsável por extrair resultados dos experimentos ---
    if libGammaMass.simu == True: # Somente extraia caso tenha sido realizada as simulações

        import libCalib
        
        libGammaMass.chdir("..") # Saia da pasta destinada a ultima simução

        # Crie os vetores para salvar todos os resultados (tallies de espectro)
        vetor_espectroFluxo     = [] #vetor para salvar todos os espectros de fluxo
        vetor_espectroFluxo_STD = [] #vetor para salvar todos os desvios padrão (std) dos espectros de fluxo
        vetor_espectroPulso     = [] #vetor para salvar todos os espectros de pulso
        vetor_espectroPulso_STD = [] #vetor para salvar todos os desvios padrão (std)) dos espectros de pulso
        
        # Navegue arquivo por arquivo coletando os resultados
        for varia in vetor_varia:
            espectroFluxo, espectroFluxo_STD =     detector.tallies_detector(get=True,    nome="espectroFluxo", score="flux",          file=f"simulação_{varia:.4f}/statepoint.{ciclos}.h5")
            espectroPulso, espectroPulso_STD =     detector.tallies_detector(get=True,    nome="espectroPulso", score="pulse-height",  file=f"simulação_{varia:.4f}/statepoint.{ciclos}.h5")
            
            #Salve eles nos vetores
            vetor_espectroFluxo.append(espectroFluxo)
            vetor_espectroFluxo_STD.append(espectroFluxo_STD)
            vetor_espectroPulso.append(espectroPulso)
            vetor_espectroPulso_STD.append(espectroPulso_STD)

            # Colapsar espectro
            fluxo_total     = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo)
            fluxo_total_std = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo_STD)
            pulso_total     = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso)
            pulso_total_std = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso_STD)

            # Energia A cobalto: 1.1732e6
            # Energia B cobalto: 1.3325e6
            energia_entre_AB_cobalto = [1.15e6, 1.35e6]
            fluxo_entreCobalto     = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo,      intervalos_energias, energia_entre_AB_cobalto)
            fluxo_entreCobalto_std = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo_STD,  intervalos_energias, energia_entre_AB_cobalto)
            pulso_entreCobalto     = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso,      intervalos_energias, energia_entre_AB_cobalto)
            pulso_entreCobalto_std = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso_STD,  intervalos_energias, energia_entre_AB_cobalto)

            # Energia A cobalto: 1.1732e6
            # Energia B cobalto: 1.3325e6
            energia_somente_A_cobalto = [1.15e6, 1.2e6]
            energia_somente_B_cobalto = [1.3e6, 1.35e6]
            fluxo_somenteCobalto     = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo,      intervalos_energias, energia_somente_A_cobalto) + libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo,      intervalos_energias, energia_somente_B_cobalto)
            fluxo_somenteCobalto_std = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo_STD,  intervalos_energias, energia_somente_A_cobalto) + libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo_STD,  intervalos_energias, energia_somente_B_cobalto)
            pulso_somenteCobalto     = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso,      intervalos_energias, energia_somente_A_cobalto) + libCalib.sum_espectro(vetor_varia, vetor_espectroPulso,      intervalos_energias, energia_somente_B_cobalto)
            pulso_somenteCobalto_std = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso_STD,  intervalos_energias, energia_somente_A_cobalto) + libCalib.sum_espectro(vetor_varia, vetor_espectroPulso_STD,  intervalos_energias, energia_somente_B_cobalto)

            # Energia A cobalto: 1.1732e6
            # Energia B cobalto: 1.3325e6
            energia_abaixoCobalto = [5e3, 1.15e6]
            fluxo_abaixoCobalto     = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo,      intervalos_energias, energia_abaixoCobalto)
            fluxo_abaixoCobalto_std = libCalib.sum_espectro(vetor_varia, vetor_espectroFluxo_STD,  intervalos_energias, energia_abaixoCobalto)
            pulso_abaixoCobalto     = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso,      intervalos_energias, energia_abaixoCobalto)
            pulso_abaixoCobalto_std = libCalib.sum_espectro(vetor_varia, vetor_espectroPulso_STD,  intervalos_energias, energia_abaixoCobalto)

            #Se o tipo de variação for area, realize a calibração
            if tipoVaria == "area" or tipoVaria == "area+sequencia" or tipoVaria == "area+aleatorio":
                pulso_total_calib           = libCalib.calcula_curva_calibracao_area(vetor_varia, pulso_total, plotar=False)
                pulso_entreCobalto_calib    = libCalib.calcula_curva_calibracao_area(vetor_varia, pulso_entreCobalto, plotar=False)
                pulso_somenteCobalto_calib  = libCalib.calcula_curva_calibracao_area(vetor_varia, pulso_somenteCobalto, plotar=False)
                pulso_abaixoCobalto_calib   = libCalib.calcula_curva_calibracao_area(vetor_varia, pulso_abaixoCobalto, plotar=False)

        # --- Seção responsável por salvar entradas e saídas de todos experimentos ---


        with open("resultados_simuVariaTarugo.py", "w") as f:  #### mudar nome para separar os casos
            escreva_comentario(f," Resultados da Simulação OpenMC - Função simuVariaTarugo\n\n")
            escreva_comentario(f," Arquivo gerado automaticamente\n\n")
            escreva_variaveis(f," Configurações de simulação:", particulas=particulas,  ciclos=ciclos)
            escreva_variaveis(f," Configurações de variação:", tipoVaria=tipoVaria, ini=ini, fin=fin, passo=passo, area=area, prop=prop, vetor_varia=vetor_varia, matriz_sequencia=matriz_sequencia, vetor_lim_inf=vetor_lim_inf, vetor_lim_sup=vetor_lim_sup)
            escreva_comentario(f," Configurações de geometria e fonte:")
            escreva_variaveis(f,"# Parâmetros do tarugo (alguns gerados automaticamente):", vetor_tarugo_esteira_pos=vetor_tarugo_esteira_pos, vetor_tarugo_comprimento=vetor_tarugo_comprimento, vetor_prop=vetor_prop, vetor_tarugo_largura=vetor_tarugo_largura, vetor_tarugo_altura=vetor_tarugo_altura, vetor_area=vetor_area)
            escreva_variaveis(f,"# Parâmetros do colimador:",  colimador_espessura=colimador_espessura, colimador_abertura=colimador_abertura, colimador_impureza=colimador_impureza)
            escreva_variaveis(f,"# Parãmetros das fontes", fonte_cobalto_intensidade=fonte_cobalto_intensidade, fonte_raiosCosmicos_mes=fonte_raiosCosmicos_mes, fonte_raiosCosmicos_latitude=fonte_raiosCosmicos_latitude)
            escreva_variaveis(f,"# Parametros do detector", detectores_numero=detectores_numero, detectores_altura_meio=detectores_altura_meio, detectores_altura_esquerda=detectores_altura_esquerda, detectores_altura_direita=detectores_altura_direita)
            escreva_variaveis(f,"# Parametros concreto", fonte_Concreto_intensidade=fonte_Concreto_intensidade)
            escreva_comentario(f," Espectro para resultados:")
            escreva_variaveis(f," Intervalos de energias que são divididos os tallies de fluxo e altura de pulso", intervalos_energias=intervalos_energias)
            escreva_comentario(f," Resultados:\n\n")
            escreva_variaveis(f,"# Vetor contendo o espectro de fluxo para cada variação simulada",vetor_espectroFluxo=vetor_espectroFluxo)
            escreva_variaveis(f,"# Vetor contendo o espectro de desvio padrão do fluxo para cada variação simulada",vetor_espectroFluxo_STD=vetor_espectroFluxo_STD)
            escreva_variaveis(f,"# Vetor contendo o espectro de pulso para cada variação simulada",vetor_espectroPulso=vetor_espectroPulso)
            escreva_variaveis(f,"# Vetor contendo o espectro de desvio padrão do pulso para cada variação simulada",vetor_espectroPulso_STD=vetor_espectroPulso_STD)
            escreva_variaveis(f,"# Vetor contendo o espectro de desvio padrão do pulso para cada variação simulada",vetor_espectroPulso_STD=vetor_espectroPulso_STD)
            escreva_variaveis(f,"# Fluxo e pulso total para cada variação simulada, com respectivos desvios padrão",fluxo_total=fluxo_total, fluxo_total_std=fluxo_total_std, pulso_total=pulso_total, pulso_total_std=pulso_total_std, )
            escreva_variaveis(f,"# Fluxo e pulso entre as energias do cobalto para cada variação simulada, com respectivos desvios padrão",energia_entre_AB_cobalto=energia_entre_AB_cobalto, fluxo_entreCobalto=fluxo_entreCobalto, fluxo_entreCobalto_std=fluxo_entreCobalto_std, pulso_entreCobalto=pulso_entreCobalto, pulso_entreCobalto_std=pulso_entreCobalto_std, )
            escreva_variaveis(f,"# Fluxo e pulso somente nas energias do cobalto para cada variação simulada, com respectivos desvios padrão",energia_somente_A_cobalto=energia_somente_A_cobalto, energia_somente_B_cobalto=energia_somente_B_cobalto, fluxo_somenteCobalto=fluxo_somenteCobalto, fluxo_somenteCobalto_std=fluxo_somenteCobalto_std, pulso_somenteCobalto=pulso_somenteCobalto, pulso_somenteCobalto_std=pulso_somenteCobalto_std, )
            escreva_variaveis(f,"# Fluxo e pulso abaixo das energias do cobalto para cada variação simulada, com respectivos desvios padrão",energia_abaixoCobalto=energia_abaixoCobalto, fluxo_abaixoCobalto=fluxo_abaixoCobalto, fluxo_abaixoCobalto_std=fluxo_abaixoCobalto_std, pulso_abaixoCobalto=pulso_abaixoCobalto, pulso_abaixoCobalto_std=pulso_abaixoCobalto_std, )
            
            if tipoVaria == "area" or tipoVaria == "area+sequencia" or tipoVaria == "area+aleatorio":
                escreva_variaveis(f,"# Variáveis relativas a calibração de área",pulso_total_calib=pulso_total_calib,pulso_entreCobalto_calib=pulso_entreCobalto_calib,pulso_somenteCobalto_calib=pulso_somenteCobalto_calib,pulso_abaixoCobalto_calib=pulso_abaixoCobalto_calib)
            
    # Volte mais uma pasta para sair do diretório de resultados
    os.chdir("..")













