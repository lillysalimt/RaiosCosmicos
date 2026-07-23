import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    dados_00  = pd.read_csv('Simulacao_00_h1_PHS.csv', skiprows=7, comment='#', 
                        names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
    dados_25  = pd.read_csv('Simulacao_25_h1_PHS.csv', skiprows=7, comment='#', 
                        names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
    dados_50  = pd.read_csv('Simulacao_50_h1_PHS.csv', skiprows=7, comment='#', 
                        names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
    dados_75  = pd.read_csv('Simulacao_75_h1_PHS.csv', skiprows=7, comment='#', 
                        names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
    dados_100 = pd.read_csv('Simulacao_100_h1_PHS.csv', skiprows=7, comment='#', 
                        names=['Contagens', 'Sw', 'Sw2', 'Sxw0', 'Sx2w0'])
except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado.")
    exit()

contagens_00  =  dados_00['Sw'].iloc[0:101].values
contagens_25  =  dados_25['Sw'].iloc[0:101].values
contagens_50  =  dados_50['Sw'].iloc[0:101].values
contagens_75  =  dados_75['Sw'].iloc[0:101].values
contagens_100 = dados_100['Sw'].iloc[0:101].values

erro_00  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_00])
erro_25  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_25])
erro_50  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_50])
erro_75  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_75])
erro_100 = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_100])

energia_maxima_simulada = 2.005 # MeV
energia_x = np.linspace(0.005, energia_maxima_simulada, 101)
plt.figure(figsize=(6, 5))


plt.errorbar(
    energia_x, 
    contagens_00, 
    yerr=erro_00, 
    fmt='-', 
    drawstyle='steps-mid',
    color='#F272C6',     
    ecolor='#7255A3', 
    elinewidth=2, 
    capsize=3, 
    alpha=0.8,
    label='00%'
)
plt.fill_between(
    energia_x, 
    contagens_00, 
    step="mid",
    color='#F272C6',
    alpha=0.2
)


# plt.errorbar(
#     energia_x, 
#     contagens_25, 
#     yerr=erro_25, 
#     fmt='-', 
#     drawstyle='steps-mid',
#     color='#ff7f0e',     
#     ecolor='red', 
#     elinewidth=2, 
#     capsize=3, 
#     alpha=0.8,
#     label='25%'
# )
# plt.fill_between(
#     energia_x, 
#     contagens_25, 
#     step="mid",
#     color='#ff7f0e',
#     alpha=0.2
# )


# plt.errorbar(
#     energia_x, 
#     contagens_50, 
#     yerr=erro_50, 
#     fmt='-', 
#     drawstyle='steps-mid',
#     color='#2ca02c',     
#     ecolor='red', 
#     elinewidth=2, 
#     capsize=3, 
#     alpha=0.8,
#     label='50%'
# )
# plt.fill_between(
#     energia_x, 
#     contagens_50, 
#     step="mid",
#     color='#2ca02c',
#     alpha=0.2
# )


# plt.errorbar(
#     energia_x, 
#     contagens_75, 
#     yerr=erro_75, 
#     fmt='-', 
#     drawstyle='steps-mid',
#     color='#d62728',     
#     ecolor='red', 
#     elinewidth=2, 
#     capsize=3, 
#     alpha=0.8,
#     label='75%'
# )
# plt.fill_between(
#     energia_x, 
#     contagens_75, 
#     step="mid",
#     color='#d62728',
#     alpha=0.2
# )


plt.errorbar(
    energia_x, 
    contagens_100, 
    yerr=erro_100, 
    fmt='-', 
    drawstyle='steps-mid',
    color='#099DBA',     
    ecolor='#7DA355', 
    elinewidth=2, 
    capsize=3, 
    alpha=0.8,
    label='100%'
)
plt.fill_between(
    energia_x, 
    contagens_100, 
    step="mid",
    color='#099DBA',
    alpha=0.2
)

cores = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7']
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
plt.xlim(0.1, 2.0) 
plt.ylim(bottom=0.1)
plt.yscale('log')

plt.title('Espectro de Altura de Pulso - Simulação Geant4', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Energia do canal (MeV)', fontsize=10, fontweight='bold')
plt.ylabel('Energia Depositada no Cristal (MeV)', fontsize=10, fontweight='bold')
plt.legend(fontsize=11, loc='upper right')

# plt.savefig("espectro_barras_cob.png", dpi=300, bbox_inches='tight')
plt.show()
