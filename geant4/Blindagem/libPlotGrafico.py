########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####    Biblioteca para plotar os resultados de forma padronizada   ####
####                     libPlotResultado.py                        ####
####                                                                ####
####             Daniel de Almeida Magalhães Campolina              ####
####                      Lilly Salim Thein                         ####
####                 Thalles Oliveira Campagnani                    ####
####               Jefferson Quintão Campos Duarte                  ####
####                                                                ####
########################################################################


import matplotlib.pyplot as plt
import numpy as np
import importlib.util
import pandas as pd


def plot_padrao(
    eixo_x,                 #Obrigatório: Lista de numeros que compõem o eixo x
    vetor_eixo_y,           #Obrigatório: Lista de numeros que compõem o eixo y, ou uma lista de várias listas de eixos y
    vetor_eixo_y_std=None,  #Lista de numeros que compõem o desvio padrão do eixo y, ou uma lista de várias listas de desvio padrão do eixo y
    vetor_legenda=None,     #Legenda do gráfico, ou uma lista de legenda do mesmo tamanho que a quantidade de eixo y
    vetor_cores=None,       #Cor do gráfico, ou uma lista de cores do mesmo tamanho que a quantidade de eixo y
    salvar=None,            #Nome do arquivo para ser salvo
    plotar=True,
    estilo=None,
    titulo="",
    xlabel="",
    ylabel=""
    ):

    plt.figure(figsize=(10, 6))

    # Se for único eixo y, envolvemos em uma lista [] para o loop funcionar igual.
    multiplo = isinstance(vetor_eixo_y[0], (list, tuple, np.ndarray))
    if not multiplo:
        vetor_eixo_y = [vetor_eixo_y]
        if vetor_eixo_y_std is not None:
            vetor_eixo_y_std = [vetor_eixo_y_std]

    # Loop de Plotagem 
    for i, eixo_y in enumerate(vetor_eixo_y):
        
        # Define a cor (se o vetor existir e tiver índice suficiente)
        cor = None
        if vetor_cores and i < len(vetor_cores):
            cor = vetor_cores[i]
            
        # Define a legenda (se o vetor existir e tiver índice suficiente)
        label = None
        if vetor_legenda and i < len(vetor_legenda):
            label = vetor_legenda[i]
            
        # Define o erro padrão para esta curva específica
        yerr = None
        if vetor_eixo_y_std is not None and i < len(vetor_eixo_y_std):
            yerr = vetor_eixo_y_std[i]

        # Plota com ou sem barra de erro
        if yerr is not None:
                if estilo == "barras":
                    plt.errorbar(
                        eixo_x, 
                        eixo_y, 
                        yerr=yerr, 
                        fmt='-', 
                        drawstyle='steps-mid',
                        color=cor,     # Usa a cor definida ou automática se None
                        ecolor='red', # Cor da barra de erro (opcional, ou usar 'cor')
                        elinewidth=2, 
                        capsize=3, 
                        label=label,
                        alpha=0.8
                    )
                if estilo == "linhas":
                    plt.errorbar(
                        eixo_x, 
                        eixo_y, 
                        yerr=yerr, 
                        fmt='o-', 
                        color=cor,     # Usa a cor definida ou automática se None
                        ecolor='red', # Cor da barra de erro (opcional, ou usar 'cor')
                        elinewidth=1, 
                        capsize=3, 
                        label=label,
                        alpha=0.8
                    )
        else:
            plt.plot(
                eixo_x, 
                eixo_y, 
                'o-', 
                color=cor, 
               # drawstyle='steps-mid',
                label=label
            )

    # Estilização
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.xlabel(xlabel, fontsize=14, fontweight='bold')
    plt.ylabel(ylabel, fontsize=14, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.figsize=(9, 6)
    
    # Só exibe a legenda se houver labels definidos
    if vetor_legenda:
        plt.legend()

    # Só salva se o nome do arquivo estiver definido
    if salvar is not None:
        plt.savefig(f"{salvar}.png", dpi=300)
        plt.savefig(f"{salvar}.pdf", dpi=300)
        print(f"Gráfico salvo como '{salvar}.png' e '{salvar}.pdf'")
        
    if plotar:
        plt.show()
    

        

def plot_espectro_padrao(
        espectro,
        intervalos_energias = None,
        log = True,
        salvar=None,            #Nome do arquivo para ser salvo
        plotar=True,
        titulo="",
        xlabel=None,
        ylabel=""
    ):
    # Lógica para definir o Eixo X
    if intervalos_energias is None:
        eixo_x = np.arange(len(espectro))
        if xlabel is None:
            label_x = 'Canal'
    else:
        # Garante que o vetor de energia tenha o mesmo tamanho do fluxo
        intervalos_energias_np = np.array(intervalos_energias)
        eixo_x = (intervalos_energias_np[:-1] + intervalos_energias_np[1:]) / 2
        if xlabel is None:
            label_x = 'Energia (MeV)' # Ou a unidade que você estiver usando

    # Plotagem das barras
    # O align='center' garante que a barra fique centralizada no valor do eixo X
    plt.bar(eixo_x, espectro, width=np.diff(eixo_x)[0] if len(eixo_x) > 1 else 1.0, 
            color='royalblue', edgecolor='white', linewidth=0.5, align='center')

    # Configurações dinâmicas
    plt.xlabel(xlabel, fontsize=14, fontweight='bold')
    plt.ylabel('Intensidade', fontsize=14, fontweight='bold')
    plt.title(f'Espectro de {label_x}', fontsize=16, fontweight='bold')
    plt.grid(axis='y', linestyle=':', alpha=0.5)

    if log:
        plt.yscale('log')
        # Evita erro de log se houver zeros no espectro
        plt.ylim(bottom=max(min(espectro)*0.1, 1e-10) if any(espectro) else None)

    plt.tight_layout()
    plt.show()
    
    
# Só executa se for executado diretamente, caso seja importado não execute
if __name__ == "__main__":

    def carregar_modulo(nome_modulo, caminho_arquivo):
        spec = importlib.util.spec_from_file_location(nome_modulo, caminho_arquivo)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo

    pht_00 = carregar_modulo(
        "pht_00",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\simulacao_00\resultados_simuVariaTarugo.py")
    
    pht_25 = carregar_modulo(
        "pht_25",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\simulacao_25\resultados_simuVariaTarugo.py")

    pht_50 = carregar_modulo(
        "pht_50",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\simulacao_50\resultados_simuVariaTarugo.py")

    pht_75 = carregar_modulo(
        "pht_75",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\simulacao_75\resultados_simuVariaTarugo.py")

    pht_100 = carregar_modulo(
        "pht_100",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\simulacao_100\resultados_simuVariaTarugo.py")

    ####################################
    ######### OpenMC ###################
    altura_lista = [0, 25, 50, 75, 100]
    openmc_total_00 = sum(pht_00.espectroPulso)*33
    openmc_total_25 = sum(pht_25.espectroPulso)*33
    openmc_total_50 = sum(pht_50.espectroPulso)*33
    openmc_total_75 = sum(pht_75.espectroPulso)*33
    openmc_total_100 = sum(pht_100.espectroPulso)*33
    total_pulso_openmc = [openmc_total_00, openmc_total_25, openmc_total_50, openmc_total_75, openmc_total_100]
    openmc_total_std =[1/np.sqrt(openmc_total_00),
                 1/np.sqrt(openmc_total_25), 
                 1/np.sqrt(openmc_total_50), 
                 1/np.sqrt(openmc_total_75), 
                 1/np.sqrt(openmc_total_100)]


    try:
        dados_00 = pd.read_csv('Simulacao_00_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_25 = pd.read_csv('Simulacao_25_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_50 = pd.read_csv('Simulacao_50_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_75 = pd.read_csv('Simulacao_75_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_100 = pd.read_csv('Simulacao_100_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_00_cint = pd.read_csv('Simulacao_00_cint_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_25_cint = pd.read_csv('Simulacao_25_cint_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_50_cint = pd.read_csv('Simulacao_50_cint_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_75_cint = pd.read_csv('Simulacao_75_cint_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
        dados_100_cint = pd.read_csv('Simulacao_100_cint_h1_PHS.csv', skiprows=7, comment='#', 
                            names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
    except FileNotFoundError:
        print("Erro: Um ou mais arquivos de simulação não foram encontrados.")
        exit()

    contagens_00_geant4 = dados_00['Sw'].iloc[1:101].values
    contagens_25_geant4 = dados_25['Sw'].iloc[1:101].values
    contagens_50_geant4 = dados_50['Sw'].iloc[1:101].values
    contagens_75_geant4 = dados_75['Sw'].iloc[1:101].values
    contagens_100_geant4 = dados_100['Sw'].iloc[1:101].values

    contagens_00_geant4_cint = dados_00_cint['Sw'].iloc[1:101].values
    contagens_25_geant4_cint = dados_25_cint['Sw'].iloc[1:101].values
    contagens_50_geant4_cint = dados_50_cint['Sw'].iloc[1:101].values
    contagens_75_geant4_cint = dados_75_cint['Sw'].iloc[1:101].values
    contagens_100_geant4_cint = dados_100_cint['Sw'].iloc[1:101].values


    energia_maxima_simulada = 2.005  # MeV
    energia_x = np.linspace(0.005, energia_maxima_simulada, 100)

    # =====================================================================
    # TRUQUE DO REBINNING: Agrupar canais para o gráfico de barras ficar nítido
    # =====================================================================



    sinal_00_geant4 = (np.array(contagens_00_geant4[58])+np.array(contagens_00_geant4[66]))
    sinal_25_geant4 = (np.array(contagens_25_geant4[58])+np.array(contagens_25_geant4[66]))
    sinal_50_geant4 = (np.array(contagens_50_geant4[58])+np.array(contagens_50_geant4[66]))
    sinal_75_geant4 = (np.array(contagens_75_geant4[58])+np.array(contagens_75_geant4[66]))
    sinal_100_geant4 = (np.array(contagens_100_geant4[58])+np.array(contagens_100_geant4[66]))

    sinal_00_geant4_cint = (np.array(contagens_00_geant4_cint[65])+np.array(contagens_00_geant4_cint[74]))
    sinal_25_geant4_cint = (np.array(contagens_25_geant4_cint[65])+np.array(contagens_25_geant4_cint[74]))
    sinal_50_geant4_cint = (np.array(contagens_50_geant4_cint[65])+np.array(contagens_50_geant4_cint[74]))
    sinal_75_geant4_cint = (np.array(contagens_75_geant4_cint[65])+np.array(contagens_75_geant4_cint[74]))
    sinal_100_geant4_cint = (np.array(contagens_100_geant4_cint[65])+np.array(contagens_100_geant4_cint[74]))


    sinal_00_openmc = (np.array(pht_00.espectroPulso[58])+np.array(pht_00.espectroPulso[66]))*33
    sinal_25_openmc = (np.array(pht_25.espectroPulso[58])+np.array(pht_25.espectroPulso[66]))*33
    sinal_50_openmc = (np.array(pht_50.espectroPulso[58])+np.array(pht_50.espectroPulso[66]))*33
    sinal_75_openmc = (np.array(pht_75.espectroPulso[58])+np.array(pht_75.espectroPulso[66]))*33
    sinal_100_openmc = (np.array(pht_100.espectroPulso[58])+np.array(pht_100.espectroPulso[66]))*33

    sinal_geant4 = [sinal_00_geant4, sinal_25_geant4, sinal_50_geant4, sinal_75_geant4, sinal_100_geant4]
    sinal_geant4_std = [1/np.sqrt(sinal_00_geant4), 1/np.sqrt(sinal_25_geant4), 1/np.sqrt(sinal_50_geant4), 1/np.sqrt(sinal_75_geant4), 1/np.sqrt(sinal_100_geant4)]
    sinal_openmc = [sinal_00_openmc, sinal_25_openmc, sinal_50_openmc, sinal_75_openmc, sinal_100_openmc]
    sinal_openmc_std = [1/np.sqrt(sinal_00_openmc), 1/np.sqrt(sinal_25_openmc), 1/np.sqrt(sinal_50_openmc), 1/np.sqrt(sinal_75_openmc), 1/np.sqrt(sinal_100_openmc)] 


    sinal_geant4_cint = [sinal_00_geant4_cint, sinal_25_geant4_cint, sinal_50_geant4_cint, sinal_75_geant4_cint, sinal_100_geant4_cint]
    sinal_geant4_cint_std = [1/np.sqrt(sinal_00_geant4_cint), 1/np.sqrt(sinal_25_geant4_cint), 1/np.sqrt(sinal_50_geant4_cint), 1/np.sqrt(sinal_75_geant4_cint), 1/np.sqrt(sinal_100_geant4_cint)]

    total_pulso_geant4 = [contagens_00_geant4.sum(), contagens_25_geant4.sum(), contagens_50_geant4.sum(), contagens_75_geant4.sum(), contagens_100_geant4.sum()]
    total_pulso_geant4_std = [1/np.sqrt(contagens_00_geant4.sum()), 1/np.sqrt(contagens_25_geant4.sum()), 1/np.sqrt(contagens_50_geant4.sum()), 1/np.sqrt(contagens_75_geant4.sum()), 1/np.sqrt(contagens_100_geant4.sum())]
    
    total_pulso_geant4_cint = [contagens_00_geant4_cint.sum(), contagens_25_geant4_cint.sum(), contagens_50_geant4_cint.sum(), contagens_75_geant4_cint.sum(), contagens_100_geant4_cint.sum()]
    total_pulso_geant4_cint_std = [1/np.sqrt(contagens_00_geant4_cint.sum()), 1/np.sqrt(contagens_25_geant4_cint.sum()), 1/np.sqrt(contagens_50_geant4_cint.sum()), 1/np.sqrt(contagens_75_geant4_cint.sum()), 1/np.sqrt(contagens_100_geant4_cint.sum())]
    
    # gráfico completo
  
    plot_padrao(altura_lista, [total_pulso_geant4, sinal_geant4, total_pulso_geant4_cint, sinal_geant4_cint],vetor_eixo_y_std=[total_pulso_geant4_std, sinal_geant4_std, total_pulso_geant4_cint_std, sinal_geant4_cint_std], vetor_legenda=["Modelo DPE-total", "Modelo DPE-sinal", "Modelo RO-total", "Modelo RO-sinal"], titulo="Contagens do Espectro de Altura de Pulso\nSimulação Geant4", xlabel="Altura Útil do Tarugo (%)", ylabel="Energia Depositada no Cristal (MeV)", estilo="linhas")
