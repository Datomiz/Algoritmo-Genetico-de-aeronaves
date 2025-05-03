# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:40:13 2022

@author: datomi
"""

#código de geração do data frame das asas e da nomes aleatórios e dimensões aleatórias

import pandas as pd
import random as rd
import math
import numpy as np

# Taper Ratio    = \u03BB   ou Afilamento       (0 a 1)
# Sweep angle    = \u039B   ou Enflechamento    (0 a 30)
# Twist angle    = \u03B1t  ou Ângulo de torção (0 a -5)
# Dihedral angle = \u0393   ou Ângulo de diedro (-10 a 10)

def gerar_asas(quantidade_de_asas:int):

    n = 'nada'
    
    asa = {
        'Nome':[n],
        'Perfil':[n],
        'b':[n],
        'AR':[n],
        '\u03BB':[n],      #TR
        '\u03BB eff':[n],  #TR eff
        'MAC':[n],
        'S':[n],
        'Cr':[n],
        'C1':[n],
        'C2':[n],
        'Ct':[n],
        'b1':[n],
        'b2':[n],
        'b3':[n],
        'i':[n],
        '\u039B eff':[n], # enflechamento eff
        '\u03B1t':[n],    # torção
        '\u0393':[n],     # diedro
        'CL0':[n],         
        'CL\u03B1':[n],   #CLalpha
        'CD':[n],
        'Peso':[n],
        'Estabilidade':[n],
        'Controle':[n],
        'CG':[n],
        'MTOW':[n],
        'Carga Paga':[n],
        'Nota':[n],
    }

    
    df=pd.DataFrame(asa)

    melhores_asas=pd.DataFrame(asa)

    asa = pd.DataFrame(asa)
 
    for i in range(quantidade_de_asas):

        df = pd.concat([df,asa],ignore_index=True, axis = 0)


    df=df.drop(index=0)
    
    melhores_asas=melhores_asas.drop(index=0)
    
    return(df,melhores_asas)

def gerar_nomes(df):

    Nomes_de_passaros = [
        'Beija flor',
        'Papagaio',
        'Bem te vi',
        'João de barro',
        'Coleiro',
        'Sabiá laranjeira',
        'Rolinha',
        'Tucano',
        'Coruja',
        'Pombo',
        'Pato',
        'Gaivota',
        'Alegrinho',
        'Anumará',
        'Araponga',
        'Azulão',
        'Azulinho',
        'Andorinha',
        'Bagageiro',
        'Bandoleta',
        'Barbudinho',
        'Bate pára',
        'Canário do campo',
        'Caneleiro',
        'Cardeal',
        'Catatau',
        'Catraca',
        'Chororó pocuá',
        'Curió',
        'Dançador de cauda graduada',
        'Dançarino oliváceo',
        'Diamante de Gould',
        'Diuca',
        'Dragão',
        'Enferrujado',
        'Entufado',
        'Estalador',
        'Estalador do norte',
        'Estalinho',
        'Felipe do tepui',
        'Ferreirinho da capoeira',
        'Figuinha amazônica',
        'Fim fim',
        'Flautim',
        'Freirinha',
        'Fruxu',
        'Garibaldi',
        'Gaturamo verdadeiro',
        'Gralha',
        'Grimpeiro',
        'Gritador',
        'Guaracavuçu',
        'Guarda floresta',
        'Guaxe',
        'Halls babbler',
        'Irré',
        'Iraúna do norte',
        'Ipecuá',
        'Inhapim',
        'Juruviara',
        'Joãozinho',
        'Japuaçu',
        'Japu',
        'Kadavu Fantail',
        'Lavadeira de cara',
        'Lenheiro',
        'Limpa folha coroado',
        'Maria preta de penacho',
        'Maú',
        'Melro',
        'Mineirinho',
        'Miudinho',
        'Maria te viu',
        'Não pode parar',
        'Neinei',
        'Noivinha',
        'Olho falso',
        'Patativa',
        'Pisco de peito ruivo',
        'Periquito arco íris',
        'Petrim',
        'Pia cobra',
        'Pitiguari',
        'Pula pula',
        'Polícia inglesa do norte',
        'Piu piu',
        'Pintassilgo',
        'Papa piri',
        'Quebra Nozes',
        'Quem te vestiu',
        'Quete do sul',
        'Rabo branco acanelado',
        'Rei do bosque',
        'Rendeira',
        'Risadinha',
        'Rouxinol do rio negro',
        'Sanhaço',
        'Saíra sete cores',
        'Soldadinho',
        'Suiriri',
        'Saurá',
        'Tempera viola',
        'Tentilhão',
        'Tesoura do brejo',
        'Tico tico',
        'Tiê de topete',
        'Tiziu',
        'Trinca ferro',
        'Triste pia',
        'Tucano',
        'Trovoada',
        'Tuim',
        'Uirapuru de peito',
        'Uí pi',
        'Urumutum',
        'Uirapuruzinho',
        'Verdelhão',
        'Vite vite',
        'Vissiá',
        'Vira folha',
        'Vira pedras',
        'Wrentit',
        'Xexéu',
        'Yelkouan shearwater',
        'Zagateiro da China',
        'Zidedê',
        'Zombeteiro de bico',  
        ]
    
    Pedras=['Ágata',
            'Alexandrita',
            'Amazonita',
            'Âmbar',
            'Ametista',
            'Água marinha',
            'Aventurina',
            'Pedra de Cristo',
            'Cornalina',
            'Calcedônia',
            'Crisoprásio',
            'Citrino',
            'Diamante',
            'Esmeralda',
            'Fluorita',
            'Jade',
            'Hematita',
            'Jaspe',
            'Kunzita',
            'Labradorita',
            'Lápis lazúli',
            'Larimar',
            'Malaquita',
            'Pedra da lua',
            'Ônix',
            'Opala',
            'Pérola',
            'Peridoto',
            'Opala Rosa',
            'Rodocrosita',
            'Quartzo rosa',
            'Rubi',
            'Safira',
            'Sardônica',
            'Quartzo fumê',
            'Espinélio',
            'Sugilita',
            'Tanzanita',
            'Olho de Tigre',
            'Topázio',
            'Turmalina negra',
            'Turmalina',
            'Turquesa',
            'Zircão',
            'Painita',
            'Cristal',
            'Morganita',
            'Madrepérola'     
            ]
    
    Cores=['amarelo',
           'azul',
           'azul marinho',
           'azul turquesa',
           'bege',
           'branco',
           'caramelo',
           'castanho',
           'preto',
           'cinza',
           'laranja',
           'lilás',
           'marrom',
           'mostarda',
           'rosa',
           'roxo',
           'salmão',
           'verde',
           'verde água',
           'vermelho',
           'vinho',
           'violeta',
           'arco íris'      
           ]
        
    for i in range(len(df)):
        
        Nome_total = rd.choice(Nomes_de_passaros) +'-'+ rd.choice(Pedras) +'-'+ rd.choice(Cores)
        
        df.iloc[i,0] = Nome_total
    
    # print('Nome escolhido!')
    
    return(df)

def cal_TR(        #interno
        Cr:float,
        Ct:float,
        b:float,   
        ):
    
    TR=Ct/Cr
    cmac=(2/3)*Cr*((1+TR+(TR**2))/(1+TR))
    S=b*cmac
    
    S = S*2 #isso pq os valores de b são pra só um lado
    
    return(TR,S)

def cal_TR_eff(    #interno
        Cr:float,
        C1:float,
        C2:float,
        Ct:float,
        b1:float,
        b2:float,
        b3:float,       
        ):
    
    lista_Cr = [Cr,C1,C2]
    lista_Ct = [C1,C2,Ct]
    lista_b  = [b1,b2,b3]
    
    R_TR = []
    R_S  = []

    lista_contar = range(len(lista_Cr))

    for i in lista_contar:
        
        Cr = lista_Cr[i]
        Ct = lista_Ct[i]
        
        if i == 0:
            b  = lista_b[i]
        else:
            b = lista_b[i] - lista_b[i-1]
        
        TR,S = cal_TR(Cr,Ct,b)
        
        R_TR.append(TR)
        R_S.append(S)

    soma = sum(R_S)
    
    me = 0
    for i in lista_contar:
        me = R_S[i]*R_TR[i] + me

    m = me/soma
    
    return(m)

def gerar_dimens(
        df,
        bmax: float,
        bmin: float,
        ARmax: float,
        ARmin: float,
        TRmax: float,
        TRmin: float, 
        imin: int,
        imax: int,
        tormin: int,
        tormax: int,
        didmin: int,
        didmax: int
        ):
    
    lista_de_perfis = pd.read_excel('Perfil/Perfil_df.xlsx')
    
    lista_de_nomes_dos_perfis = lista_de_perfis['Nome']
    

    for i in range(len(df)):
        
        b = round(rd.uniform(bmin,bmax),3)
        
        AR = round(rd.uniform(ARmin,ARmax),3)
        
        TR = round(rd.uniform(TRmin,TRmax),3)
                        
        inc = rd.randint(imin,imax)
        
        tor = rd.randint(tormin,tormax)
        
        did = rd.randint(didmin,didmax)
                
        perfil = rd.choice(lista_de_nomes_dos_perfis)
        
        df.iloc[i,1] = perfil
        df.iloc[i,2] = b
        df.iloc[i,3] = AR
        df.iloc[i,4] = TR
        df.iloc[i,15] = inc 
        df.iloc[i,17] = tor
        df.iloc[i,18] = did
        
        
    # print('Dimensões definidas!')
    
    return(df)

def cal_dimens(df):
    
    for i in range(len(df)):
    
        b = df.iloc[i,2]
        
        AR = df.iloc[i,3]
        
        TR = df.iloc[i,4]
        
        'Calculos gerais'
        
        S = (b**2)/AR
        
        b3 = round(b/2,3)
        
        MAC = round(S/b,3)
        
        Cr = round((1.5 * (1 + TR) * MAC) / (1 + TR + TR ** 2),3)
        
        Ct = round(Cr*TR,3)
        
        'Escolha do b1'
        
        if type(df.iloc[i,12]) == float:
            
            b1 = df.iloc[i,12]
        
        else: 
            
            b1 = round(rd.uniform(0,b3*0.5),3)
            # b1 = round(rd.uniform(0,b3),3) #sem restrição
        
        'Escolha do b2'
        
        if type(df.iloc[i,13]) == float:
            
            b2 = df.iloc[i,13]
            
        else:
            
            b2 = round(rd.uniform(b1,b3*0.8),3)     
        
        'Calculo do C1 e C2 para que eles se encaixem no MAC'
        
        if type(df.iloc[i,9]) == float and type(df.iloc[i,10]) == float:

            C1 = df.iloc[i,9]
            
            C2 = df.iloc[i,10]
        
        else: #calculo do C1 e C2 caso não exista
            
            if round(TR,3) == 1:
                
                C1,C2 = Cr,Cr
            
            else:

                valores_validos_de_C1eC2 = np.arange(Ct,Cr*1.2,0.001)
                
                rd.shuffle(valores_validos_de_C1eC2)
                
                valores_validos_de_C1 = list(reversed(valores_validos_de_C1eC2))
                
                for k in valores_validos_de_C1:
                    
                    C1i = k    
                
                    macs=[]
                    
                    for C2i in valores_validos_de_C1eC2:
                        
                        
                        lista_Cr = [Cr,C1i,C2i]
                        lista_Ct = [C1i,C2i,Ct]
                        lista_b  = [b1,b2,b3]
                        
                        lista_S = []
                        lista_C = []
        
                        for l in range(len(lista_b)):
                            
                            TR_i = lista_Ct[l]/lista_Cr[l]
                            cmac=(2/3)*lista_Cr[l]*((1+TR_i+(TR_i**2))/(1+TR_i))
                            
                            if l == 0:
                                S_i = lista_b[l]*cmac
                            if l > 0:
                                S_i = (lista_b[l]-lista_b[l-1])*cmac
                            
                            lista_C.append(cmac)
                            lista_S.append(S_i)
        
                        soma = sum(lista_S)
                        soma_cima = 0
                        
                        for j in range(len(lista_C)):
                            
                            soma_cima = soma_cima + (lista_C[j]*lista_S[j])
    
                        MAC_i = round((soma_cima/soma),3)
                        
                        macs.append(MAC_i)
                        
                        if MAC_i == MAC and C1i > C2i:
                            break
                        
                    if MAC_i == MAC and C1i > C2i:
                        C2 = round(C2i,3)
                        C1 = round(C1i,3)
                        break  
        
        
        lista_Cr = [Cr,C1,C2]
        lista_Ct = [C1,C2,Ct]
        lista_b  = [b1,b2,b3]
        
        lista_S = []
        lista_C = []
        
        for n in range(len(lista_b)):
            
            TR_i = lista_Ct[n]/lista_Cr[n]
            cmac=(2/3)*lista_Cr[n]*((1+TR_i+(TR_i**2))/(1+TR_i))
            
            if n == 0:
                S_i = lista_b[n]*cmac
            if n > 0:
                S_i = (lista_b[n]-lista_b[n-1])*cmac
            
            S_i = 2*S_i
            
            lista_C.append(cmac)
            lista_S.append(S_i)
        
        soma = sum(lista_S)
        soma_cima = 0
        for n in range(len(lista_C)):
            
            soma_cima = soma_cima + (lista_C[n]*lista_S[n])
            
        MAC = round(soma_cima/soma,3) #verificação
        
        S = round(soma,4) #verificação
        
        AR = round(b/MAC,3) #verificação
        
        'Taper Ratio efetivo'
        
        TR_eff = round(cal_TR_eff(Cr,C1,C2,Ct,b1,b2,b3),3)
        
        Cr_eff = 3*MAC/(2*((1+TR_eff+(TR_eff**2))/(1+TR_eff)))
        Cp_eff = Cr_eff*TR_eff
        
        'Enflechamento efetivo'
        
        lamb = int((math.tan((Cr_eff-Cp_eff)/b))*180/math.pi)  #enflechamento efetivo
        
        df.iloc[i,3] = AR
        df.iloc[i,5] = TR_eff
        df.iloc[i,6] = MAC
        df.iloc[i,7] = S
        df.iloc[i,8] = Cr
        df.iloc[i,9] = C1
        df.iloc[i,10] = C2
        df.iloc[i,11] = Ct
        df.iloc[i,12] = b1
        df.iloc[i,13] = b2
        df.iloc[i,14] = b3
        df.iloc[i,16] = lamb

    # print('Dimensões calculadas!')
    
    return(df)



