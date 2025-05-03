# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:35:51 2022

@author: datomi
"""

#código que faz operações genéticas com o data frame da asa

import random as rd
import pandas as pd
import pylab as plt
import math
import numpy as np
import sympy as sy

def escolha_melhor(df): #interno
    
    lista = list(df['Nota'])
    
    for u in range(len(lista)):
        
        if lista[u] < 0:
            lista[u] = 1
        
    escolha = rd.choices(
        population = range(len(df)),
        weights = lista,
        # k=int(len(df)/2)     
        k=2
        )
    
    if escolha[0] == escolha[1]:
        if escolha[0] == 0:
            escolha[0] = 1
        if escolha[0] == len(df)-1:
            escolha[0] = len(df)-2
        if escolha[0] != 0 and escolha[0] != len(df)-1:
            escolha[0] = rd.randrange(0,len(df)-1,1)
    
    return(escolha)

def muta_asas(Chance_de_mutacao_por_individuo: float,
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
        
        r = rd.uniform(0,1)
        
        b = df.iloc[i,2]
        
        AR = df.iloc[i,3]
        
        TR = df.iloc[i,4]
        
        b1 = df.iloc[i,12]
        
        b2 = df.iloc[i,13]
        
        b3 = df.iloc[i,14]
        
        iw = df.iloc[i,15]
        
        to = df.iloc[i,17]
        
        di = df.iloc[i,18]
        
        
        
        if r <= Chance_de_mutacao_por_individuo:
            
            vtot=[]
            
            for j in range(9):
                
                sinal=rd.choice([1,-1])
                
                valor=rd.uniform(0,0.2)
                
                tot=sinal*valor
                
                vtot.append(tot)
            
            #perfil:
            
            perfil = rd.choice(lista_de_nomes_dos_perfis)
            
            df.iloc[i,1] = perfil
            
            #b:
            
            if b + (b * vtot[1]) >= bmax:
                b = bmax
            if b + (b * vtot[1]) <= bmin:
                b = bmin            
            if b + (b * vtot[1]) < bmax and b + (b * vtot[1]) > bmin:               
                b = round(b + (b * vtot[1]),3)
                
            #AR:
            
            if AR + (AR * vtot[2]) >= ARmax:
                AR = ARmax
            if AR + (AR * vtot[2]) <= ARmin:
                AR = ARmin            
            if AR + (AR * vtot[2]) < ARmax and AR + (AR * vtot[2]) > ARmin:               
                AR = round(AR + (AR * vtot[2]),3)
            
            #TR
            
            if TR + (TR * vtot[3]) >= TRmax:
                TR = TRmax
            if TR + (TR * vtot[3]) <= TRmin:
                TR = TRmin            
            if TR + (TR * vtot[3]) < TRmax and TR + (TR * vtot[3]) > TRmin:               
                TR = round(TR + (TR * vtot[3]),3)
            
            #b1
            
            if b1 + (b1 * vtot[4]) >= b2:
                b1 = b2
            if b1 + (b1 * vtot[4]) <= 0: #se for 0 o primeiro segmento n existe
                b1 = 0            
            if b1 + (b1 * vtot[4]) < b2 and b1 + (b1 * vtot[4]) > 0:               
                b1 = round(b1 + (b1 * vtot[4]),3) #b1

            #b2     
            
            if b2 + (b2 * vtot[5]) >= b3:
                b2 = b3
            if b2 + (b2 * vtot[5]) <= b1:
                b2 = b1         
            if b2 + (b2 * vtot[5]) < b3 and b2 + (b2 * vtot[5]) > b1:               
                b2 = round(b2 + (b2 * vtot[5]),3)  #b2

            #b3

            b3 = round(b/2,3)
            
            #incidencia
            
            if iw + (iw * vtot[6]) >= imax:
                iw = imax
            if iw + (iw * vtot[6]) <= imin:
                iw = imin            
            if iw + (iw * vtot[6]) < imax and iw + (iw * vtot[6]) > imin:               
                iw = round(iw + (iw * vtot[6]),3)  #incidência
            
            #torção
            
            if to + (to * vtot[7]) >= tormax:
                to = tormax
            if to + (to * vtot[7]) <= tormin:
                to = tormin            
            if to + (to * vtot[7]) < tormax and to + (to * vtot[7]) > tormin:               
                to = round(to + (to * vtot[7]),3)  #torção
            
            #diedro
            
            if di + (di * vtot[8]) >= didmax:
                di = didmax
            if di + (di * vtot[8]) <= didmin:
                di = didmin            
            if di + (di * vtot[8]) < didmax and di + (di * vtot[8]) > didmin:               
                di = round(di + (di * vtot[8]),3)  #diedro
            
                        
            #mutação do nome
            
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
            
            
            nome = df.iloc[i,0]
            
            indx1 = nome.find('-')
            indx2 = nome.rfind('-')
            
            rn = rd.randint(0,2)
            
            if rn == 0:

                nomef = rd.choice(Nomes_de_passaros) + nome[indx1:indx2] + nome[indx2:]
            
            if rn == 1:
                
                nomef = nome[:indx1] +'-'+ rd.choice(Pedras) + nome[indx2:]
            
            if rn == 2:
                
                nomef = nome[:indx1] + nome[indx1:indx2] +'-'+ rd.choice(Cores)
                
            df.iloc[i,0] = nomef
            
            df.iloc[i,2] = b
            df.iloc[i,3] = AR
            df.iloc[i,4] = TR
            df.iloc[i,12] = b1 
            df.iloc[i,13] = b2
            df.iloc[i,14] = b3 
            df.iloc[i,15] = iw
            df.iloc[i,17] = to
            df.iloc[i,18] = di

   
            n = 'nada' 
   
            df.iloc[i,5] = n
            df.iloc[i,6] = n
            df.iloc[i,7] = n
            df.iloc[i,8] = n
            df.iloc[i,9] = n
            df.iloc[i,10] = n
            df.iloc[i,11] = n
            df.iloc[i,16] = n
            df.iloc[i,19] = n
            df.iloc[i,20] = n
            df.iloc[i,21] = n
            df.iloc[i,22] = n
            df.iloc[i,23] = n
            df.iloc[i,24] = n
            df.iloc[i,25] = n
            df.iloc[i,26] = n
            df.iloc[i,27] = n
            
    # print('Mutação executada!')
    
    return(df)

def gerar_notas(df,
                Peso_CP,
                Peso_Estabilidade,
                Peso_Controle,
                Peso_CG):
    
    for i in range(len(df)):
        
        esta = df.iloc[i,23]
        
        contro = df.iloc[i,24]
        
        CG = df.iloc[i,25]
        
        CP = df.iloc[i,27]
        
        nota_Estabilidade = Peso_Estabilidade*esta
        
        nota_Controle     = Peso_Controle*(6.333*contro**4 - 64.833*contro**3 + 235.667*contro**2 - 388.1667*contro + 311.0)
        
        nota_CP           = Peso_CP*(-13566.518*math.exp(-CP) + 0.0387*CP**3 + 2755.415*CP*math.exp(-CP) - 6.149)
        
        nota_CG           = Peso_CG*(-0.16*CG**2 + 8.0*CG)
        
        if nota_CP < 0:
            nota_CP = 0
        
        nota_final = (nota_Controle + nota_Estabilidade + nota_CP + nota_CG) / (Peso_Controle + Peso_Estabilidade + Peso_CP + Peso_CG)
        
        nota_final = round(nota_final,3)
        
        df.iloc[i,28] = nota_final
        
    # print('Notas calculadas!')
    
    return(df)

def resetar_notas(df):
    
    for i in range(len(df)):
        
        n = 'nada'
        
        df.iloc[i,28] = n
    
    # print('Notas resetadas!')
    
    return(df)
    
def cruza_asas(Chance_de_cruzamento_por_individuo: float,
               df,     
        ):
    
    
    for i in range(len(df)):
        
        r = rd.uniform(0,1)
        
        if r <= Chance_de_cruzamento_por_individuo:
            # print(df._get_value(i+1,'b3'))
            
            #cruzamento de um valor da asa
            
            escolha = escolha_melhor(df)
            
            escolha_valor_lista = [2,3,4,15,17,18] # [b,AR,TR,i,torção,diedro]
            
            escolha_valor = rd.choice(escolha_valor_lista)
            
            temp = df.iloc[escolha[0],escolha_valor]
            
            df.iloc[escolha[0],escolha_valor] = df.iloc[escolha[1],escolha_valor]
            df.iloc[escolha[1],escolha_valor] = temp
            
            #fazendo cruzamento dos nomes
            
            nome1 = df.iloc[escolha[0],0]
            nome2 = df.iloc[escolha[1],0]

            
            indx1_1 = nome1.find('-') 
            indx1_2 = nome1.rfind('-') 
            indx2_1 = nome2.find('-') 
            indx2_2 = nome2.rfind('-') 
            
            quebra1_1 = nome1[:indx1_1]
            quebra1_2 = nome1[indx1_2:]
            quebra2_1 = nome2[:indx2_1]
            quebra2_2 = nome2[indx2_2:]
            
            nomeconst1 = nome1[indx1_1:indx1_2]
            nomeconst2 = nome2[indx2_1:indx2_2]
            
            ra = rd.randint(0,1)
            
            if ra == 1:
                novo1 = quebra1_1 + nomeconst1 + quebra2_2
                novo2 = quebra2_1 + nomeconst2 + quebra1_2
            
            if ra == 0:
                novo1 = quebra2_1 + nomeconst1 + quebra1_2
                novo2 = quebra1_1 + nomeconst2 + quebra2_2
            
            df.iloc[escolha[0],0] = novo1
            df.iloc[escolha[1],0] = novo2
            
            
            n = 'nada'
            
            df.iloc[i,5] = n
            df.iloc[i,6] = n
            df.iloc[i,7] = n
            df.iloc[i,8] = n
            df.iloc[i,9] = n
            df.iloc[i,10] = n
            df.iloc[i,11] = n
            df.iloc[i,16] = n
            df.iloc[i,19] = n
            df.iloc[i,20] = n
            df.iloc[i,21] = n
            df.iloc[i,22] = n
            df.iloc[i,23] = n
            df.iloc[i,24] = n
            df.iloc[i,25] = n
            df.iloc[i,26] = n
            df.iloc[i,27] = n
    
            #MAIS COISA PRA RESETAR DPS!!!!        
    
    
    # print('Cruzamento efetuado!')
    
    return(df)

def organizar_por_nota(df):
    
    df = df.sort_values("Nota",ascending=False)
    
    # print("Tabela organizada!")
    
    return(df)

def elitismo(df,
             quantidade_de_asas: int,
             quantidade_da_melhor_asa_copiada: int
             ):
    
    #fazer somente após organizar a tabela
    
    total = quantidade_da_melhor_asa_copiada + int(quantidade_da_melhor_asa_copiada*0.5) + int(quantidade_da_melhor_asa_copiada*0.2)

    piores = range(quantidade_de_asas - total,quantidade_de_asas)
    
    df = df.drop(df.index[piores])
    
    p = df.iloc[0].to_dict()
    s = df.iloc[1].to_dict()
    t = df.iloc[2].to_dict()

    
    prim = pd.DataFrame(p, index=[0])
    segu = pd.DataFrame(s, index=[0])
    terc = pd.DataFrame(t, index=[0])
       
    
    for i in range(quantidade_da_melhor_asa_copiada):
        df = pd.concat([df,prim],ignore_index=True, axis = 0)

    for i in range(int(quantidade_da_melhor_asa_copiada*0.5)):
        df = pd.concat([df,segu],ignore_index=True, axis = 0)
        
    for i in range(int(quantidade_da_melhor_asa_copiada*0.2)):
        df = pd.concat([df,terc],ignore_index=True, axis = 0)
    
    # print('Elitismo realizado!')
    
    return(df)         

def graf_final(df,
               media_de_notas:list):
        
    try:
        plt.style.use('extensys-gd')
    except:
        pass
    
    lista_mel = list(df.iloc[:,28])
    
    plt.figure(num=None, figsize=(7, 5), dpi=200, facecolor='w', edgecolor='k')
    plt.xlabel('Geração')
    plt.ylabel('Nota')
    plt.plot(range(len(df)),media_de_notas,label='média',color='b')
    plt.plot(range(len(df)),lista_mel,label='melhor nota',color='orange')
    plt.legend(bbox_to_anchor=(0.45, 1.05, 0.25, 0.1), ncol=3)
    plt.savefig('Imagens\grafico_resultado.png')
    plt.show()

def graf_da_asa(df):
    
    try:
        plt.style.use('extensys-gd')
    except:
        pass
    
    
    nome_da_asa = df.iloc[0,0]
    
    mac = df.iloc[0,6]
    
    Cr = df.iloc[0,8]
    
    C1 = df.iloc[0,9]
    
    C2 = df.iloc[0,10]
    
    Ct = df.iloc[0,11]
    
    b1 = df.iloc[0,12]
    
    b2 = df.iloc[0,13]
    
    b3 = df.iloc[0,14]
    
    porc = df.iloc[0,25]
    
    lista_Cr = [Cr,C1,C2]
    lista_Ct = [C1,C2,Ct]
    lista_b  = [b1,b2,b3]
    
    x=sy.symbols('x')

    segmentos=[]

    for i in range(len(lista_b)):
        if i == 0:
            linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/(lista_b[i]+0.001))*(x-0))
        if i > 0:     
            linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/((lista_b[i]-lista_b[i-1])+0.001))*(x-lista_b[i-1]))
        
        segmentos.append(linha)

    listax = np.linspace(0,lista_b[len(lista_b)-1],1000)
    listay = []
    listacont = np.arange(1,len(lista_b),1)

    for x in listax:
        
        if x < lista_b[0]:
            y = eval(str(segmentos[0]))
        
        if x > lista_b[0]:
            for i in listacont:
                if x > lista_b[i-1] and x < lista_b[i]:
                    y = eval(str(segmentos[i]))
                    
        listay.append(y)

    listax2 = []

    for i in range(len(listay)):
        listax2_v = -listax[i]      
        listax2.append(listax2_v)

    for i in range(len(listay)):
        listay[i] = -listay[i]
    
    px = [-lista_b[len(lista_b)-1],-lista_b[len(lista_b)-1]]
    py = [0,-lista_Ct[len(lista_Ct)-1]]

    bx = [lista_b[len(lista_b)-1],lista_b[len(lista_b)-1]]
    by = [0,-lista_Ct[len(lista_Ct)-1]]

    cx = [-lista_b[len(lista_b)-1],lista_b[len(lista_b)-1]]
    cy = [0,0]

            
    graf_a = plt.figure(num=None, figsize=(19, 13.5), dpi=200, facecolor='w', edgecolor='k')

    plt.plot(listax,listay,color='blue')
    plt.plot(listax2,listay,color='blue')
    plt.plot(cx,cy,color='b')
    plt.plot(px,py,color='b')
    plt.plot(bx,by,color='b',label='asa')

    plt.axhline(mac*3/4-lista_Cr[0],linestyle = '--',label='CA')
    plt.scatter(0,-(porc*Cr/100),label='CG')

    plt.title('Desenho da Asa '+nome_da_asa)
    plt.axis([-0.1-lista_b[len(lista_b)-1],lista_b[len(lista_Ct)-1]+0.1,-max(lista_Cr)-0.05,0.05])
    plt.xlabel('b[m]')
    plt.ylabel('C[m]')
    plt.legend(bbox_to_anchor=(0.75, 1, 0.25, 0.1), ncol=3)
    ax = plt.gca()
    ax.set_aspect('equal',adjustable = 'box')
    plt.show()

    graf_a.savefig('Imagens\grafico_da_asa.png')


            
            