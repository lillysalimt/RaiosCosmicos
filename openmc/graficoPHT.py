import numpy as np
import matplotlib.pyplot as plt
import importlib.util

if __name__ == "__main__":

    def carregar_modulo(nome_modulo, caminho_arquivo):
        spec = importlib.util.spec_from_file_location(nome_modulo, caminho_arquivo)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo

    pht_00 = carregar_modulo(
        "pht_00",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\finalmb_00\resultados_simuVariaTarugo.py")
    
    pht_25 = carregar_modulo(
        "pht_25",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\finalmb_25\resultados_simuVariaTarugo.py")

    pht_50 = carregar_modulo(
        "pht_50",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\finalmb_50\resultados_simuVariaTarugo.py")

    pht_75 = carregar_modulo(
        "pht_75",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\finalmb_75\resultados_simuVariaTarugo.py")

    pht_100 = carregar_modulo(
        "pht_100",
        r"c:\Users\Lili\OneDrive\Documentos\GitHub\GammaMass\sim\finalmb_100\resultados_simuVariaTarugo.py")

contagens_00  = np.array(pht_00.espectroPulso)*10
contagens_25  = np.array(pht_25.espectroPulso)*10
contagens_50  = np.array(pht_50.espectroPulso)*10
contagens_75  = np.array(pht_75.espectroPulso)*10
contagens_100 = np.array(pht_100.espectroPulso)*10


erro_00  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_00])
erro_25  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_25])
erro_50  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_50])
erro_75  = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_75])
erro_100 = np.array([1/(np.sqrt(i))  if i != 0 else 0.0 for i in contagens_100])

energia_maxima_simulada = 2.005 # MeV
energia_x = np.linspace(0.005, energia_maxima_simulada, 100)
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

plt.title('Espectro de Altura de Pulso - Simulação OpenMC', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Energia do canal (MeV)', fontsize=10, fontweight='bold')
plt.ylabel('Energia Depositada no Cristal (MeV)', fontsize=10, fontweight='bold')
plt.legend(fontsize=11, loc='upper right')

plt.savefig("espectro_barras.png", dpi=300, bbox_inches='tight')
plt.show()
