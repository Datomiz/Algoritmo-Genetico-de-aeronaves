# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:27:21 2022

@author: datomi
"""

#Código de controle geral das operações

from GerarAsas import gerar_asas,gerar_nomes,gerar_dimens,cal_dimens
from Genetico import muta_asas,gerar_notas,cruza_asas,resetar_notas,organizar_por_nota,elitismo,graf_final,graf_da_asa
from Analises import CL,analise_controle,CD,MTOW,Calculo_do_peso,Carga_paga,estabilidade
import time
import numpy as np
import pandas as pd
import os
import shutil

def Codigo_genetico(
        pop:int,
        elitism:int,
        probmut:float,
        probcru:float,
        quangen:int,
        bmin:float,
        bmax:float,
        ARmin:float,
        ARmax:float,
        TRmin:float,
        TRmax:float,
        imin:float,
        imax:float,
        tormin:float,
        tormax:float,
        didmin:float,
        didmax:float,
        velocidade:float,
        densidade:float,
        atrito:float,
        potencia:float,
        altura:float,
        Peso_CP:float,
        Peso_Estabilidade:float,
        Peso_Controle:float,
        Peso_CG
        ):
    
    
    folder = 'Resultados'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    tempofeito=time.asctime()
    tempofeito=tempofeito[10:19] + tempofeito[7:10] + tempofeito[3:7] + tempofeito[19:] # marca o tempo q o código foi rodado

    com = time.time()

    #Loop genético

    df,melhores_asas = gerar_asas(pop)    #gerou o df da asas e tabela de melhores asas
    df = gerar_nomes(df)                  #colocou nomes
    df = gerar_dimens(df,bmax,bmin,ARmax,ARmin,TRmax,TRmin,imin,imax,tormin,tormax,didmin,didmax) #colocou dimensões inicial
    
    media_de_notas=[]
    
    for _ in range(quangen):
        
        print('\nGeração Número: %s \n'%(_+1))
        
        df = cal_dimens(df)           #calculou dimensões complexas

        df = CL(df,velocidade)        #calculo do CL

        df = CD(df,velocidade,altura)

        df = analise_controle(df,densidade,velocidade)     #calculo de controle
        
        df = Calculo_do_peso(df,altura)

        df = MTOW(df,potencia,velocidade,densidade,atrito,altura,imax)
        
        df = Carga_paga(df)
        
        df = estabilidade(df)
        
        df = gerar_notas(df,Peso_CP,Peso_Estabilidade,Peso_Controle,Peso_CG)          #gerou notas
        df = organizar_por_nota(df)   #organizou as notas pelas melhores primeiro
                        
        media = np.mean(list(df.iloc[:,28])) #pega a media das notas
        media_de_notas.append(media)
        
        p = df.iloc[0].to_dict()
        prim = pd.DataFrame(p, index=[0])
        melhores_asas = pd.concat([melhores_asas,prim],ignore_index=True, axis = 0) #guardando a melhor asa
        
        df.to_excel('Resultados/Geração '+str(_+1)+' .xlsx',index=False)
        
        df = elitismo(df,pop,elitism) #multiplicou as melhores asas
        
        df = cruza_asas(probcru,df)   #cruzou as asas
        df = resetar_notas(df)        #resetou as notas
        
        df = muta_asas(probmut,df,bmax,bmin,ARmax,ARmin,TRmax,TRmin,imin,imax,tormin,tormax,didmin,didmax) #realizou a mutação de asas
        
        if _ == quangen - 1:
            
            print("Terminando...")
            df = cal_dimens(df)
            df = CL(df,velocidade) 
            df = CD(df,velocidade,altura)
            df = analise_controle(df,densidade,velocidade)
            df = Calculo_do_peso(df,altura)
            df = MTOW(df,potencia,velocidade,densidade,atrito,altura,imax)
            df = Carga_paga(df)
            df = estabilidade(df)
            df = gerar_notas(df,Peso_CP,Peso_Estabilidade,Peso_Controle,Peso_CG) 
            df = organizar_por_nota(df)
            
    
    graf_final(melhores_asas,media_de_notas) # faz o grafico
        
    melhores_asas = organizar_por_nota(melhores_asas) # faz o gráfico da asa
    
    graf_da_asa(melhores_asas)

    melhores_asas.to_excel('Resultados/Melhores asas de cada geração.xlsx',index=False)
    
    fim = time.time()
    
    print('\nTempo de processamento: %s segundos'%round(fim-com,1))
    print('Execução efetuada em:',tempofeito)
    


