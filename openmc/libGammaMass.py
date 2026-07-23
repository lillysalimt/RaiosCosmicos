########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####           Biblioteca de simulação do Detector Gama             ####
####                      libGammaMass.py                           ####
####                                                                ####
####             Daniel de Almeida Magalhães Campolina              ####
####                      Lilly Salim Thein                         ####
####                 Thalles Oliveira Campagnani                    ####
####               Jefferson Quintão Campos Duarte                  ####
####                                                                ####
########################################################################

import openmc
import openmc.stats
import numpy as np
import openmc.model
from matplotlib import pyplot as plt
import os
from datetime import datetime
from PIL import Image

#Variáveis facilitadores de controle de execução
simu = True
plotar = True



# Criar pasta e mudar para a pasta criada:
def mkdir(nome="teste_sem_nome",data=True,voltar=False):
    if (voltar==True):
        os.chdir("../")
    if (data==True):
        agora = datetime.now()
        nome = agora.strftime(nome+"_%Y%m%d_%H%M%S")
    if not os.path.exists(nome):
        os.makedirs(nome)
    os.chdir(nome)




# Mudar para a pasta
def chdir(nome=None):
    if (nome != None):
        os.chdir(nome)
    else:
        diretorio_atual = os.getcwd()
        diretorios = [diretorio for diretorio in os.listdir(diretorio_atual) if os.path.isdir(os.path.join(diretorio_atual, diretorio))]

        data_mais_recente = 0
        pasta_mais_recente = None

        for diretorio in diretorios:
            data_criacao = os.path.getctime(os.path.join(diretorio_atual, diretorio))
            if data_criacao > data_mais_recente:
                data_mais_recente = data_criacao
                pasta_mais_recente = diretorio

        if pasta_mais_recente:
            os.chdir(os.path.join(diretorio_atual, pasta_mais_recente))
            print("Diretório mais recente encontrado:", pasta_mais_recente)
        else:
            print("Não foi possível encontrar um diretório mais recente.")


################################################
########      Classe do Detector        ########
################################################
class Detector:
    ################################################
    ############       Construtor        ###########
    ################################################
    def __init__(self,
            particulas=1000,
            ciclos=100
            ):
        
        # Criando xml padrão de materiais, geometria e configurações
        self.materiais()
        self.geometria()
        self.configurações(particulas, ciclos)






    ################################################
    ############        Destrutor        ###########
    ################################################

    def __del__(self):
        print(f"Objeto destruído.")









    ################################################
    ############ Definição dos Materiais ###########
    ################################################
    def materiais(self):

        #Cria objeto para armazenar os materiais criados
        materials = openmc.Materials()

        #Já definir as cores dos materiais para os 'plots'
        self.colors = {}

        # Material 1 - Fonte de Cobalto (Co-60)
        self.m_cobalto = openmc.Material(name='Fonte de Cobalto')
        self.m_cobalto.add_nuclide('Co59', 1.0)
        self.m_cobalto.set_density('g/cm3', 8.9)
        materials.append(self.m_cobalto)
        self.colors[self.m_cobalto] = "red"

        # Material 2 - Aço
        self.m_aco = openmc.Material(name='Aço')
        self.m_aco.add_element('Fe', 0.98)
        self.m_aco.add_element('C', 0.02)
        self.m_aco.set_density('g/cm3', 7.85)
        materials.append(self.m_aco)
        self.colors[self.m_aco] = "black"

        # Material 3 - Detector de Cristal de Iodeto de Cesio
        self.m_csi = openmc.Material(name='Detector de CsI')
        self.m_csi.add_nuclide('Cs133', 0.5)
        self.m_csi.add_nuclide('I127', 0.5)
        self.m_csi.set_density('g/cm3', 4.51)
        materials.append(self.m_csi)
        self.colors[self.m_csi] = "yellow"

        # Material 4 - Água
        self.m_agua = openmc.Material(name='Água')
        self.m_agua.add_nuclide('H1', 2.0)
        self.m_agua.add_nuclide('O16', 1.0)
        self.m_agua.set_density('g/cm3', 1.0)
        materials.append(self.m_agua)
        self.colors[self.m_agua] = "blue"

        # Material 5 - Ar
        self.m_ar = openmc.Material(name='Ar')
        self.m_ar.add_nuclide('N14', 0.755)
        self.m_ar.add_nuclide('O16', 0.231)
        self.m_ar.add_nuclide('Ar40', 0.013)
        self.m_ar.set_density('g/cm3', 0.001225)
        materials.append(self.m_ar)
        self.colors[self.m_ar] = (173, 216, 230)

        # Marterial 6 - Carvão
        self.m_carvao = openmc.Material(name='m_carvao Hulha')
        self.m_carvao.set_density('g/cm3', 0.793)  
        self.m_carvao.add_element('C', 0.78)
        self.m_carvao.add_element('H', 0.05)
        self.m_carvao.add_element('O', 0.13)
        self.m_carvao.add_element('N', 0.02)
        self.m_carvao.add_element('S', 0.02)
        materials.append(self.m_carvao)
        self.colors[self.m_carvao] = "grey"

        # Material 7 - Minério de ferro
        self.m_ore = openmc.Material(name='Minério de Ferro')
        self.m_ore.add_element('Fe', 0.6)
        self.m_ore.add_element('O', 0.3)
        self.m_ore.add_element('Si', 0.05)
        self.m_ore.add_element('Al', 0.04)
        self.m_ore.add_element('Mn', 0.01)
        self.m_ore.set_density('g/cm3', 3.5)  # densidade média com umidade e porosidade
        materials.append(self.m_ore)
        self.colors[self.m_ore] = "brown"

        
        # Material 8 - Chumbo
        self.m_pb = openmc.Material(name='Chumbo')
        self.m_pb.add_nuclide('Pb208', 0.524)
        self.m_pb.add_nuclide('Pb207', 0.221)
        self.m_pb.add_nuclide('Pb206', 0.241)
        self.m_pb.add_nuclide('Pb204', 0.014)
        self.m_pb.set_density('g/cm3', 11.34)
        materials.append(self.m_pb)
        self.colors[self.m_pb] = (45, 79, 56)


        # Material 9 - Concreto (cimento Portland comum)
        cao = openmc.Material()
        cao.add_elements_from_formula('CaO')
        sio = openmc.Material()
        sio.add_elements_from_formula('SiO2')
        alo = openmc.Material()
        alo.add_elements_from_formula('Al2O3')
        feo = openmc.Material()
        feo.add_elements_from_formula('Fe2O3')
        mgo = openmc.Material()
        mgo.add_elements_from_formula('MgO')
        ko = openmc.Material()
        ko.add_elements_from_formula('K2O')
        nao = openmc.Material()
        nao.add_elements_from_formula('Na2O')
        so = openmc.Material()
        so.add_elements_from_formula('SO3')

        self.m_concreto = openmc.Material.mix_materials(
            [cao,     sio,   alo,   feo,   mgo,    ko,    nao,    so],
            [0.665,  0.20,  0.05,  0.04,  0.02,  0.01,  0.005,  0.01],
            'wo',
            name = 'Concreto'
        )

        self.m_concreto.set_density('g/cm3', 2.4)
        materials.append(self.m_concreto)
        self.colors[self.m_concreto] = (230, 162, 131)

        # Criação do conjunto de materiais
        materials.export_to_xml()

















    ################################################"
    ############ Definição da Geometria ############"
    ################################################"
    def geometria(
        self,
        
        # Parâmetros do tarugo
        tarugo_esteira_pos = 0, #centralizado em cima da fonte
        tarugo_comprimento = 10,
        tarugo_largura     = 10,
        tarugo_altura      = 10,
        
        # Parâmetros do colimador
        colimador_espessura = 2.8, #Espessura nominal do colimador LB-4700
        colimador_abertura  = 7.8,  #Diametro do detector
        colimador_impureza  = 0,
        
        # Parãmetros das fontes
        fonte_cobalto_intensidade    = 7.4e6, ########### Atividade de 3.7e7 x2 pois são 2 fótons
        fonte_raiosCosmicos_mes      = 1,
        fonte_raiosCosmicos_latitude = 0,
        fonte_raiosCosmicos_intensidade = 1.09e5,
        
        # Parametros do detector
        detectores_numero           = 1,
        detectores_altura_meio      = 52.35,
        detectores_altura_esquerda  = 52.35,
        detectores_altura_direita   = 52.35,

        #Parametros concreto
        fonte_Concreto_intensidade = 1.0058e5           ### 10 m² de chão concreto

        ):
        
    ###############################################
    # Convenções
    ###############################################
    
    # Eixo X: Aonde corre a esteira (comprimento)
    # Eixo Y: Altura da esteira (alinhada com gravidade)
    # Eixo Z: Largura da esteira (alinhada com as fontes)
        
        
        
    ###############################################
    # Generalidades
    ###############################################
        
        # Cria objeto Universo para armazenar as células
        universe_1 = openmc.Universe()
        
        # Cria uma lista de fontes em self para ser usada em configurações()
        self.fontes = []
        
        
    
    
    
    ############################################# 
    # Definindo células do universe_1
    ############################################# 
        
        # Dica de OpenMC
        ## ======================
        ## region = 
        ##          & intersection
        ##          > union
        ##          ~ complement
        ## ======================
        
    #############################################
        
        # Fonte de Co-60
        ## Formato: cilindrico
        ## Posição: 0,0,0
        ## Tamanho: 60 de comprimento (Y) por 0.35 de raio (XZ)
        
        fonte_diametro = 0.70
        fonte_comprimento = 60
        
        
        ### Definição de "geometria" do material da fonte
        Co60_cyl    = openmc.ZCylinder( r =  fonte_diametro/2)
        plane_y_min = openmc.ZPlane(   z0 = -fonte_comprimento/2)
        plane_y_max = openmc.ZPlane(   z0 =  fonte_comprimento/2)

        fonte_cell = openmc.Cell(name='Fonte Co60')
        fonte_cell.region = -Co60_cyl & +plane_y_min & -plane_y_max
        fonte_cell.fill = self.m_cobalto
        
        universe_1.add_cell(fonte_cell)
        
        
        
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()

        print("|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")
        print("|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")
        print("|--|--|--|--|--|                    fonte_cobalto_intensidade = ", fonte_cobalto_intensidade)
        print("|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")
        print("|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|")

        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()

        ### Definição da "distribuição" da origem e características dos raios gama da fonte    
        fonte_cobalto = openmc.IndependentSource(
            space       =   openmc.stats.CylindricalIndependent(
            r   =openmc.stats.Uniform(a=0,                        b=fonte_diametro),
            phi =openmc.stats.Uniform(a=0,                        b=2*np.pi),
            z   =openmc.stats.Uniform(a= -fonte_comprimento/2,    b=fonte_comprimento/2)
            ),
            angle       =   openmc.stats.Isotropic(),                                               # Ângulo isotrópico
            energy      =   openmc.stats.Discrete([1.1732e6, 1.3325e6], [0.5, 0.5]),                # Espectro de energia para Co-60
            strength    =   fonte_cobalto_intensidade,                                              # Intensidade da fonte
            particle    =   'photon'
        )
        
        ##### Adicionar a lista de fontes em self
        if not fonte_cobalto_intensidade==0:
            self.fontes.append(fonte_cobalto)

    
    
    
    
    ###############################################
        
        # Esteira
        ## Formato: Paralelepipedo
        ## Posição: 0,0,10.45
        ## Tamanho: Fixo em XYZ
        
        esteira_espessura       = 0.1
        esteira_altura_sup      = 10.45 #esteira_altura_sup será reaproveitado posteriormente, por isso não está centralizada como as outras
        esteira_altura_inf      = esteira_altura_sup - esteira_espessura
        esteira_largura         = 50
        esteira_comprimento     = 150
        
        
        esteira_min_x = openmc.XPlane(x0 = -esteira_comprimento/2)
        esteira_max_x = openmc.XPlane(x0 =  esteira_comprimento/2)
        esteira_min_y = openmc.YPlane(y0 =  esteira_altura_inf)
        esteira_max_y = openmc.YPlane(y0 =  esteira_altura_sup)
        esteira_min_z = openmc.ZPlane(z0 = -esteira_largura/2)
        esteira_max_z = openmc.ZPlane(z0 =  esteira_largura/2)

        esteira_cell = openmc.Cell(name='Esteira')
        esteira_cell.region = -esteira_max_z & +esteira_min_z & -esteira_max_x & +esteira_min_x & -esteira_max_y & +esteira_min_y
        esteira_cell.fill = self.m_aco

        universe_1.add_cell(esteira_cell)
        
        
        
        
        
    #############################################
    
        # Tarugo de carvão
        ## Formato: Paralelepipedo
        ## Posição: variável em X, fixo em YZ = 0,0
        ## Tamanho: variável em XYZ
        ### Convenção: comprimento X, largura Y, altura Z
        
        plane_x_min_tarugo = openmc.XPlane(x0 =  tarugo_esteira_pos  -  tarugo_comprimento/2)
        plane_x_max_tarugo = openmc.XPlane(x0 =  tarugo_esteira_pos  +  tarugo_comprimento/2)
        plane_y_min_tarugo = openmc.YPlane(y0 =  esteira_altura_sup)
        plane_y_max_tarugo = openmc.YPlane(y0 =  esteira_altura_sup  +  tarugo_altura)#sempre começar encostado na esteira
        plane_z_min_tarugo = openmc.ZPlane(z0 = -tarugo_largura/2)
        plane_z_max_tarugo = openmc.ZPlane(z0 =  tarugo_largura/2) 

        tarugo_cell = openmc.Cell(name='Tarugo de Aço')
        tarugo_cell.region = +plane_x_min_tarugo & -plane_x_max_tarugo & +plane_y_min_tarugo & -plane_y_max_tarugo & +plane_z_min_tarugo & -plane_z_max_tarugo
        tarugo_cell.fill = self.m_ore
    
        universe_1.add_cell(tarugo_cell)
        


    ###############################################


        # Detector de Cristal de CsI com "suporte" e colimador de tamanho variável
        
        self.detector_altura = detectores_altura_meio
        
        ## Formato: cilindrico
        
        ## Posição do conjunto em Z: 52.35
        ### Posicionamento: Tampa - Cristal - Suporte
        
        ## Tamanho: diametro de 7.6 (todos)
        ### Suporte: comprimento de 
        ### Cristal: comprimento de 
        ### Tampa: comprimento de 
        
        ## ToDo List:
        ### - Criar detectores laterais opcionais (universo detector? retirar esse suporte para não atrapalhar (colidir)?)
        ### - Criar espaço interno de ar dentro do colimador
        ### - Usar colimador_espessura e colimador_impureza para calcular intensidade da fonte gama originária do próprio chumbo (vai precisar de CylindricalIndependent, logo rotacionar todo código)
        
        cristal_diametro = 7.6
        
        NaI_cyl         = openmc.ZCylinder( y0 = self.detector_altura, r = cristal_diametro/2)
        disco_cyl       = openmc.ZCylinder( y0 = self.detector_altura, r = cristal_diametro/2)
        plane_y_min     = openmc.ZPlane(    z0 = -2.5)
        plane_y_max     = openmc.ZPlane(    z0 =  2.5)
        plane_y_disco   = openmc.ZPlane(    z0 = -4.3)
        plane_y_clmp    = openmc.ZPlane(    z0 =  31.6)


        # Cristal
        self.detector_cell = openmc.Cell(name='Detector de CsI')
        self.detector_cell.region = -NaI_cyl & +plane_y_min & -plane_y_max
        self.detector_cell.fill = self.m_csi

        universe_1.add_cell(self.detector_cell)


        # Tampa
        disco_cell = openmc.Cell(name='Disco do detector')
        disco_cell.region = +plane_y_disco & -plane_y_min & -disco_cyl
        disco_cell.fill = self.m_aco

        universe_1.add_cell(disco_cell)
        
        
        # Suporte
        clamping_cell = openmc.Cell(name='Região do suporte')
        clamping_cell.region = -disco_cyl & +plane_y_max & -plane_y_clmp
        clamping_cell.fill = self.m_aco

        universe_1.add_cell(clamping_cell)
        
     
        # Colimador        
        # Para tirar o colimador, basta trocar o material para ar, mas é preciso definir um valor diferente de 0 para o diâmetro externo
        if colimador_espessura>0:
            colimador_diametro_ext = (cristal_diametro/2 + colimador_espessura)*2
        else:
            colimador_diametro_ext = 1 #Definindo com um valor qualquer para não dar erro

        
        # Janela do colimador
        
        plane_x_max_janela = openmc.XPlane(x0 =  colimador_abertura/2)
        plane_x_min_janela = openmc.XPlane(x0 = -colimador_abertura/2)
        plane_y_max_janela = openmc.YPlane(y0 =  self.detector_altura)
        plane_y_min_janela = openmc.YPlane(y0 =  self.detector_altura-colimador_diametro_ext/2)
        plane_z_max_janela = openmc.ZPlane(z0 =  3.0)
        plane_z_min_janela = openmc.ZPlane(z0 = -3.0)

        janela_cell = openmc.Cell(name='Janela do colimador')

        janela_cell.region = +plane_y_min_janela & -plane_y_max_janela & +plane_z_min_janela & -plane_z_max_janela & +plane_x_min_janela & -plane_x_max_janela
        janela_cell.fill = self.m_ar
        
        universe_1.add_cell(janela_cell)
        
        
        
        # Colimador em sí
        
        colimador_cell  = openmc.Cell(name='Colimador de Chumbo')
        raiocol_i       = openmc.ZCylinder( y0 =  self.detector_altura, r = 3.8)
        raiocol_e       = openmc.ZCylinder( y0 =  self.detector_altura, r = colimador_diametro_ext/2)
        plane_y_max_col = openmc.ZPlane(    z0 =  7.3)
        plane_y_min_col = openmc.ZPlane(    z0 = -6.4)
        casca_pb = -raiocol_e & +plane_y_min_col & -plane_y_max_col
        interior_col = janela_cell.region | clamping_cell.region | self.detector_cell.region | disco_cell.region
        colimador_cell.region = casca_pb & ~interior_col
        
        
        # Se a espessura do colimador for maior que 0, então o material é chumbo, caso contrário ele não existe, então é ar.
        if colimador_espessura>0:
            colimador_cell.fill = self.m_pb
        else:
            colimador_cell.fill = self.m_ar
            
        
        universe_1.add_cell(colimador_cell)

    ###############################################

        # Ar - Criar uma célula de ar ao redor de todas as outras - Froteira de vácuo
        ## Formato: Paralelepipedo
        ## Tamanho: Por padrão 200x200x200, mas pode aumentar a dimensão X se o comprimento do tarugo for maior
    
        borda_dir = tarugo_esteira_pos + tarugo_comprimento / 2
        plane_x_max_vazio = openmc.XPlane(x0=borda_dir+10 if borda_dir >= 200 else 200, boundary_type='vacuum')

        borda_esq = tarugo_esteira_pos - tarugo_comprimento / 2
        plane_x_min_vazio = openmc.XPlane(x0=borda_esq-10 if borda_esq <= -200 else -200, boundary_type='vacuum')
            
        plane_y_max_vazio = openmc.YPlane(y0=  200, boundary_type='vacuum')
        plane_y_min_vazio = openmc.YPlane(y0= -200, boundary_type='vacuum')
        plane_z_max_vazio = openmc.ZPlane(z0=  200, boundary_type='vacuum')
        plane_z_min_vazio = openmc.ZPlane(z0= -200, boundary_type='vacuum')

        box = (-plane_y_max_vazio & +plane_y_min_vazio & -plane_x_max_vazio & +plane_x_min_vazio & -plane_z_max_vazio & +plane_z_min_vazio)
        inner = (self.detector_cell.region | tarugo_cell.region | fonte_cell.region | esteira_cell.region | janela_cell.region 
                 | colimador_cell.region | clamping_cell.region | disco_cell.region)

        ar_region = ar_region = box & ~inner

        ar_cell = openmc.Cell(name='Ar', fill=self.m_ar, region=ar_region)
        
        universe_1.add_cell(ar_cell)




    ###############################################
    ###############################################

        # Criar a geometria contendo 
        geometry = openmc.Geometry()
        geometry.root_universe = universe_1
        geometry.export_to_xml()





    ###############################################
    # Fonte de raios cósmicos
    ###############################################
    
        # Distribuição de fonte de raios cósmicos
        
        ## ToDo list:
        ### - Usar fonte_raiosCosmicos_mes e fonte_raiosCosmicos_latitude para calcular intensidade e espectro de energia
        ### - Variar posição da fonte de raios cósmicos de acordo com a posição do detector
        ### - Verificar influência de considerar folha com raios monodirecionais. 
        ### -- Acredito que uma semi-esfera ao redor do detector seja mais realista, mas pode precisar de mais particulas.
        ### -- Talvez a opção mais sensata e/ou otimizada seja uma casca cilindrica usando CylindricalIndependent, logo é preciso rotacionar todo código
        
        
        
        ## Código simplificado
        ### Formato: Hemisférico
        ### Tamanho: raio externo de 1m, espessura de 10cm
        ### Posição: centralizada em torno do sistema
        
        # Espectro de energia de raios cósmicos
# ------------------------------
# Espectro de energias (em eV)
# ------------------------------
        energias = [
    1.13E4, 1.42E4, 1.79E4, 2.25E4, 2.84E4, 3.57E4, 4.50E4, 5.66E4, 7.13E4, 8.97E4,
    1.13E5, 1.42E5, 1.79E5, 2.25E5, 2.84E5, 3.57E5, 4.50E5, 5.66E5, 7.13E5, 8.97E5,
    1.13E6, 1.42E6, 1.79E6, 2.25E6, 2.84E6, 3.57E6, 4.50E6, 5.66E6, 7.13E6, 8.97E6,
    1.13E7, 1.42E7, 1.79E7, 2.25E7, 2.84E7, 3.57E7, 4.50E7, 5.66E7, 7.13E7, 8.97E7,
    1.13E8, 1.42E8, 1.79E8, 2.25E8, 2.84E8, 3.57E8, 4.50E8, 5.66E8, 7.13E8, 8.97E8,
    ]
# ------------------------------
# Frações normalizadas
# ------------------------------
        fracoes = [
    4.75E-04, 1.40E-03, 4.10E-03, 1.20E-02, 3.44E-02, 9.03E-02, 1.76E-01, 2.03E-01, 1.57E-01, 1.06E-01,
    6.91E-02, 4.50E-02, 2.94E-02, 1.94E-02, 1.29E-02, 8.73E-03, 5.96E-03, 1.32E-02, 2.91E-03, 2.09E-03,
    1.52E-03, 1.12E-03, 8.41E-04, 6.39E-04, 4.90E-04, 3.79E-04, 2.95E-04, 2.30E-04, 1.79E-04, 1.38E-04,
    1.06E-04, 7.95E-05, 5.87E-05, 4.22E-05, 2.96E-05, 2.01E-05, 1.32E-05, 8.47E-06, 5.29E-06, 3.24E-06,
    1.95E-06, 1.16E-06, 6.83E-07, 3.99E-07, 2.32E-07, 1.35E-07, 7.77E-08, 4.48E-08, 2.58E-08, 1.49E-08,
    ]
        



        r_ext = 100.0
        origin_y = (0.0, 0.0, 0.0)

        hem_norte = openmc.stats.spherical_uniform(   # Esfera relativa aos raios cósmicos
        r_inner = 90.0,
        r_outer = r_ext,
        thetas=(0.0, np.pi),
        phis=(0.0, np.pi),
        origin=origin_y
        )

        hem_sul = openmc.stats.spherical_uniform(   # Esfera relativa ao concreto
        r_inner = 90.0,
        r_outer = r_ext,
        thetas=(0.0, np.pi),
        phis=(0.0, -np.pi),
        origin=origin_y
        )

    # Espectro discreto
        fonte_raiosCosmicos_espectro = openmc.stats.Discrete(energias, fracoes)
        fonte_raiosCosmicos_intensidade = 1.09e5


        fonte_raiosCosmicos = openmc.IndependentSource(
            space = hem_norte,
            angle = openmc.stats.Isotropic(),
            energy = fonte_raiosCosmicos_espectro,
            strength = fonte_raiosCosmicos_intensidade,
            particle = 'photon'
        )
        if not fonte_raiosCosmicos_intensidade==0:
            self.fontes.append(fonte_raiosCosmicos)


    ###############################################
    # Fonte de Concreto
    ###############################################

        ## Código simplificado
        ### Formato: hemisférico
        ### Tamanho: raio externo de 1m, espessura de 10cm
        ### Posição: centralizada em torno do sistema

        # Espectro de energia de concreto
        fonte_Concreto_espectro = openmc.stats.Discrete([1.46e6], [1.0])


        fonte_Concreto = openmc.IndependentSource(
            space = hem_sul,
            angle = openmc.stats.Isotropic(),
            energy = fonte_Concreto_espectro,
            strength = fonte_Concreto_intensidade,
            particle = 'photon'
        )

        if not fonte_Concreto_intensidade==0:
            self.fontes.append(fonte_Concreto)

        



    ################################################
    ########### Definição da Simulação  ############
    ################################################
    def configurações(self,particulas,ciclos):
        # ======================
        # Configurações
        # ======================
        self.settings = openmc.Settings()
        self.settings.output = {'tallies': False}
        self.settings.source = self.fontes
        self.settings.batches = ciclos  # Número de batches para simulação
        self.settings.particles = particulas
        self.settings.photon_transport=True
        self.settings.run_mode='fixed source'
        self.settings.export_to_xml()










    ################################################"
    ###########         Rodando         ############"
    ################################################"
    def simular(self):
        if simu:
            print("################################################")
            print("###########         Rodando         ############")
            print("################################################")
            openmc.run()
        else:
            print("################################################")
            print("###########   Rodando ~DESATIVADO~  ############")
            print("################################################")













    ################################################
    ###########         Plotagem        ############
    ################################################
    def plotagem(
            self,
            filename = 'plot.png',
            basis  = 'yz',
            width  = (200, 200),
            pixels = (800, 800),
            origin = None,
            rotacionar = False
            ):
        if plotar:
            print("################################################")
            print("###########        Plotagem         ############")
            print("################################################")
            plot = openmc.Plot()
            plot.filename = filename
            plot.basis = basis
            plot.width = width
            plot.pixels = pixels
            if origin != None:
                plot.origin = origin
            else:
                plot.origin = (0, self.detector_altura/2, 0) #metade da altura do detector
            plot.color_by = 'material'
            plot.colors = self.colors
            plots = openmc.Plots([plot])

            plots.export_to_xml()
            openmc.plot_geometry()
            
            if rotacionar:
                # Rotaciona 90 graus no sentido anti-horário | expand=True: ajusta o tamanho da imagem se não for quadrada
                Image.open(filename).rotate(90, expand=True).save(filename)
                
            

        else:
            print("################################################")
            print("###########  Plotagem ~DESATIVADA~  ############")
            print("################################################")














    ###########################################################
    ############ Definição e obtenção dos Tallies  ############
    ###########################################################

    def tallies(self, init=False, export=False):
        if init and export:
            print("Erro de configuração de tallies! Encerrando...")
            self.__del__()

        if init:
            self.Tallies = openmc.Tallies()

        if export:
            self.Tallies.export_to_xml()

    def tallies_detector(
            self,
            get     =   False,
            file    =   None,
            energia =   None,
            nome    =  "fluxo",
            score   =  "flux"
            ):
        
        if not get:
            tally = openmc.Tally(name=nome)
            tally.filters.append(openmc.CellFilter(self.detector_cell))
            if energia != None:
                tally.filters.append(openmc.EnergyFilter(energia))
            tally.scores.append(score)
            self.Tallies.append(tally)
            
        else:
            # ======================
            # statepoints
            # ======================
            if file==None:
                sp = openmc.StatePoint(f"statepoint.{self.settings.batches}.h5")
            else:
                sp = openmc.StatePoint(file)
            
            value            = sp.get_tally(scores=[score], name=nome)
            value_mean       = [float(elemento[0][0]) for elemento in value.mean]
            value_std_dev    = [float(elemento[0][0]) for elemento in value.std_dev]

            sp.close()
            
            return value_mean, value_std_dev
        
        
