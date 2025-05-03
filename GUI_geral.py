# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 14:49:49 2022

@author: datomi
"""

#GUI do algoritmo genético

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import threading
import pandas as pd

from Geral import Codigo_genetico

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)       #deixa as letras menos embassadas!
except:
    pass


'___________________________________________________________________________________________________'

GUI = tk.Tk()
GUI.title('Código genético AeroJampa 2022')
GUI.geometry('1360x660')
GUI.iconbitmap('Imagens\logo_aero_icon.ico')

# Logo_aero = ImageTk.PhotoImage(Image.open('Imagens\Sublogo_com_borda.png'))
Logo_aero   = Image.open('Imagens\Sublogo_com_borda.png')
resize      = Logo_aero.resize((503,118), Image.Resampling.LANCZOS) #multiplo de 1005,235
resize      = ImageTk.PhotoImage(resize)
imagem_logo = tk.Label(image=resize)
imagem_logo.grid(row=0,column=0,columnspan=5) #ocupa 5 colunas de espaço

#lembrando que padx e pady é o é espaço entre as linhas e colunas

'___________________________________________________________________________________________________'

#Frame de dados de população

dados_pop = tk.LabelFrame(GUI,text='População',padx=10,pady=10)
dados_pop.grid(row=1,column=0)

#texto

# tex_pop = tk.Label(dados_pop,text='Quantidade de individuos na população',font=('Times',12),width=30)
tex_pop = tk.Label(dados_pop,text='Quantidade de individuos na população',width=40)
tex_pop.grid(row=0,column=0)

tex_quangen = tk.Label(dados_pop,text='Quantidade de gerações que serão geradas',width=40)
tex_quangen.grid(row=1,column=0)

#valores

pop = tk.Entry(dados_pop,width=10,borderwidth=3)
pop.grid(row=0,column=1,padx=5,pady=5) 
pop.insert(0,"100")

quangen = tk.Entry(dados_pop,width=10,borderwidth=3)
quangen.grid(row=1,column=1,padx=5,pady=5)
quangen.insert(0,"10")

'___________________________________________________________________________________________________'

#Frame de dados de população

dados_prob = tk.LabelFrame(GUI,text='Probabilidades',padx=10,pady=10)
dados_prob.grid(row=2,column=0)

#texto

tex_elitism = tk.Label(dados_prob,
                       text='Quantas vezes o melhor será copiado', 
                       width=40, 
                       wraplengt=300)
tex_elitism.grid(row=0,column=0) 

tex_probmut = tk.Label(dados_prob,
                       text='Probablidade de mutação por indivíduo',
                       width=40, 
                       wraplengt=300)
tex_probmut.grid(row=1,column=0) 


tex_probcru = tk.Label(dados_prob,
                       text='Probablidade de cruzamento por indivíduo',
                       width=40, 
                       wraplengt=300)
tex_probcru.grid(row=2,column=0) 

#valores

elitism = tk.Entry(dados_prob,width=10,borderwidth=3)
elitism.grid(row=0,column=1,padx=5,pady=5) 
elitism.insert(0,'8')

probmut = tk.Entry(dados_prob,width=10,borderwidth=3)
probmut.grid(row=1,column=1,padx=5,pady=5)
probmut.insert(0,'0.6')

probcru = tk.Entry(dados_prob,width=10,borderwidth=3)
probcru.grid(row=2,column=1,padx=5,pady=5)
probcru.insert(0,'0.4')

'___________________________________________________________________________________________________'


#Frame dos valores máximos e mínimos

dados_limit = tk.LabelFrame(GUI,text='Limites',padx=10,pady=10)
dados_limit.grid(row=1,column=1,rowspan=2) #faz esse frame ocupar a row 1 e 2

#b,AR,TR,i,tor,did

#texto

# envergadura

tex_bmax = tk.Label(dados_limit,
                    text='bmax',
                    width=10, 
                    wraplengt=270)
tex_bmax.grid(row=0,column=2)

tex_bmin = tk.Label(dados_limit,
                    text='bmin',
                    width=10, 
                    wraplengt=270)
tex_bmin.grid(row=0,column=0)

# Aaspect Ratio

tex_ARmax = tk.Label(dados_limit,
                    text='ARmax',
                    width=10, 
                    wraplengt=270)
tex_ARmax.grid(row=1,column=2)

tex_ARmin = tk.Label(dados_limit,
                    text='ARmin',
                    width=10, 
                    wraplengt=270)
tex_ARmin.grid(row=1,column=0)

# Taper Ratio

tex_TRmax = tk.Label(dados_limit,
                    text='\u03BBmax',
                    width=10, 
                    wraplengt=270)
tex_TRmax.grid(row=2,column=2)

tex_TRmin = tk.Label(dados_limit,
                    text='\u03BBmin',
                    width=10, 
                    wraplengt=270)
tex_TRmin.grid(row=2,column=0)

# incidencia

tex_imax = tk.Label(dados_limit,
                    text='imax',
                    width=10, 
                    wraplengt=270)
tex_imax.grid(row=3,column=2)

tex_imin = tk.Label(dados_limit,
                    text='imin',
                    width=10, 
                    wraplengt=270)
tex_imin.grid(row=3,column=0)

# torção

tex_tormax = tk.Label(dados_limit,
                    text='\u03B1tmax',
                    width=10, 
                    wraplengt=270)
tex_tormax.grid(row=4,column=2)

tex_tormin = tk.Label(dados_limit,
                    text='\u03B1tmin',
                    width=10, 
                    wraplengt=270)
tex_tormin.grid(row=4,column=0)

# didedro

tex_didmax = tk.Label(dados_limit,
                    text='\u0393max',
                    width=10, 
                    wraplengt=270)
tex_didmax.grid(row=5,column=2)

tex_didmin = tk.Label(dados_limit,
                    text='\u0393min',
                    width=10, 
                    wraplengt=270)
tex_didmin.grid(row=5,column=0)

#valores

# b

bmin = tk.Entry(dados_limit,width=10,borderwidth=3)
bmin.grid(row=0,column=1,padx=5,pady=5) 
bmin.insert(0,'2.25')

bmax = tk.Entry(dados_limit,width=10,borderwidth=3)
bmax.grid(row=0,column=3,padx=5,pady=5)
bmax.insert(0,'2.3')

# AR

ARmin = tk.Entry(dados_limit,width=10,borderwidth=3)
ARmin.grid(row=1,column=1,padx=5,pady=5) 
ARmin.insert(0,'3')

ARmax = tk.Entry(dados_limit,width=10,borderwidth=3)
ARmax.grid(row=1,column=3,padx=5,pady=5) 
ARmax.insert(0,'8')

# TR

TRmin = tk.Entry(dados_limit,width=10,borderwidth=3)
TRmin.grid(row=2,column=1,padx=5,pady=5) 
TRmin.insert(0,'0.2')

TRmax = tk.Entry(dados_limit,width=10,borderwidth=3)
TRmax.grid(row=2,column=3,padx=5,pady=5) 
TRmax.insert(0,'1')

# i

imin = tk.Entry(dados_limit,width=10,borderwidth=3)
imin.grid(row=3,column=1,padx=5,pady=5) 
imin.insert(0,'0')

imax = tk.Entry(dados_limit,width=10,borderwidth=3)
imax.grid(row=3,column=3,padx=5,pady=5) 
imax.insert(0,'6')

# tor

tormin = tk.Entry(dados_limit,width=10,borderwidth=3)
tormin.grid(row=4,column=1,padx=5,pady=5) 
tormin.insert(0,'-3')

tormax = tk.Entry(dados_limit,width=10,borderwidth=3)
tormax.grid(row=4,column=3,padx=5,pady=5) 
tormax.insert(0,'0')

# did

didmin = tk.Entry(dados_limit,width=10,borderwidth=3)
didmin.grid(row=5,column=1,padx=5,pady=5) 
didmin.insert(0,'-2')

didmax = tk.Entry(dados_limit,width=10,borderwidth=3)
didmax.grid(row=5,column=3,padx=5,pady=5) 
didmax.insert(0,'2')

'___________________________________________________________________________________________________'

#Frame das constantes

const = tk.LabelFrame(GUI,text='Constantes',padx=10,pady=10)
const.grid(row=1,column=2,rowspan=2)

#texto

tex_V_ex = tk.Label(const,
                    text='V',
                    width=10, 
                    wraplengt=270)
tex_V_ex.grid(row=0,column=0)

tex_phi_ex = tk.Label(const,
                    text='\u03C6',
                    width=10, 
                    wraplengt=270)
tex_phi_ex.grid(row=1,column=0)

tex_mu_ex = tk.Label(const,
                    text='\u03BC',
                    width=10, 
                    wraplengt=270)
tex_mu_ex.grid(row=2,column=0)

tex_P_ex = tk.Label(const,
                    text='P',
                    width=10, 
                    wraplengt=270)
tex_P_ex.grid(row=3,column=0)

tex_h_ex = tk.Label(const,
                    text='H',
                    width=10, 
                    wraplengt=270)
tex_h_ex.grid(row=4,column=0)

#valores

V = tk.Entry(const,width=10,borderwidth=3)
V.grid(row=0,column=1,padx=5,pady=5) 
V.insert(0,'15')

phi = tk.Entry(const,width=10,borderwidth=3)
phi.grid(row=1,column=1,padx=5,pady=5) 
phi.insert(0,'1.155')

mu = tk.Entry(const,width=10,borderwidth=3)
mu.grid(row=2,column=1,padx=5,pady=5) 
mu.insert(0,'0.0658')

P = tk.Entry(const,width=10,borderwidth=3)
P.grid(row=3,column=1,padx=5,pady=5) 
P.insert(0,'700')

H = tk.Entry(const,width=10,borderwidth=3)
H.grid(row=4,column=1,padx=5,pady=5) 
H.insert(0,'0.35')

'___________________________________________________________________________________________________'

#Frame dos pesos

pesos = tk.LabelFrame(GUI,text='Pesos',padx=10,pady=10)
pesos.grid(row=1,column=3,rowspan=2)

#texto

tex_CP_ex = tk.Label(pesos,
                    text='Peso CP',
                    width=10, 
                    wraplengt=270)
tex_CP_ex.grid(row=0,column=0)

tex_Est_ex = tk.Label(pesos,
                    text='Peso Estab',
                    width=10, 
                    wraplengt=270)
tex_Est_ex.grid(row=1,column=0)

tex_Cont_ex = tk.Label(pesos,
                    text='Peso Contr',
                    width=10, 
                    wraplengt=270)
tex_Cont_ex.grid(row=2,column=0)

tex_Cont_ex = tk.Label(pesos,
                    text='Peso CG',
                    width=10, 
                    wraplengt=270)
tex_Cont_ex.grid(row=3,column=0)

#valores

CP = tk.Entry(pesos,width=10,borderwidth=3)
CP.grid(row=0,column=1,padx=5,pady=5) 
CP.insert(0,'3')

Est = tk.Entry(pesos,width=10,borderwidth=3)
Est.grid(row=1,column=1,padx=5,pady=5) 
Est.insert(0,'1')

Cont = tk.Entry(pesos,width=10,borderwidth=3)
Cont.grid(row=2,column=1,padx=5,pady=5) 
Cont.insert(0,'1')


CG = tk.Entry(pesos,width=10,borderwidth=3)
CG.grid(row=3,column=1,padx=5,pady=5) 
CG.insert(0,'1')

'___________________________________________________________________________________________________'

#Frame da legenda

legenda = tk.LabelFrame(GUI,text='Legenda',padx=10,pady=10)
legenda.grid(row=1,column=4,rowspan=4)

tex_b_ex = tk.Label(legenda,
                    text='b = Envergadura da asa',
                    width=30, 
                    wraplengt=270)
tex_b_ex.grid(row=0,column=0)

tex_AR_ex = tk.Label(legenda,
                    text='AR = Aspect Ratio',
                    width=30, 
                    wraplengt=270)
tex_AR_ex.grid(row=1,column=0)

tex_TR_ex = tk.Label(legenda,
                    text='\u03BB = Taper Ratio',
                    width=30, 
                    wraplengt=270)
tex_TR_ex.grid(row=2,column=0)

tex_i_ex = tk.Label(legenda,
                    text='i = Ângulo de incidência da asa',
                    width=30, 
                    wraplengt=270)
tex_i_ex.grid(row=3,column=0)

tex_tor_ex = tk.Label(legenda,
                    text='\u03B1t = Ângulo de torção da asa',
                    width=30, 
                    wraplengt=270)
tex_tor_ex.grid(row=4,column=0)

tex_did_ex = tk.Label(legenda,
                    text='\u0393 = Ângulo de diedro da asa',
                    width=30, 
                    wraplengt=270)
tex_did_ex.grid(row=5,column=0)

tex_V_ex = tk.Label(legenda,
                    text='V = Velocidade analisada',
                    width=30, 
                    wraplengt=270)
tex_V_ex.grid(row=6,column=0)

tex_phi_ex = tk.Label(legenda,
                    text='\u03C6 = Densidade do ar',
                    width=30, 
                    wraplengt=270)
tex_phi_ex.grid(row=7,column=0)

tex_g_ex = tk.Label(legenda,
                    text='\u03BC = Coef. de atrito das rodas',
                    width=30, 
                    wraplengt=270)
tex_g_ex.grid(row=8,column=0)

tex_P_ex = tk.Label(legenda,
                    text='P = Potência do motor',
                    width=30, 
                    wraplengt=270)
tex_P_ex.grid(row=9,column=0)

tex_Cont_ex = tk.Label(legenda,
                    text='H = Altura da asa até o chão',
                    width=30, 
                    wraplengt=270)
tex_Cont_ex.grid(row=10,column=0)

tex_MTOW_ex = tk.Label(legenda,
                    text='MTOW = Carga máxima',
                    width=30, 
                    wraplengt=270)
tex_MTOW_ex.grid(row=11,column=0)

tex_CP_ex = tk.Label(legenda,
                    text='CP = Carga paga estimada',
                    width=30, 
                    wraplengt=270)
tex_CP_ex.grid(row=12,column=0)

tex_Est_ex = tk.Label(legenda,
                    text='Estab = Estabilidade',
                    width=30, 
                    wraplengt=270)
tex_Est_ex.grid(row=13,column=0)

tex_Cont_ex = tk.Label(legenda,
                    text='Contr = Controle',
                    width=30, 
                    wraplengt=270)
tex_Cont_ex.grid(row=14,column=0)

tex_Cont_ex = tk.Label(legenda,
                    text='CG = Centro gravitacional',
                    width=30, 
                    wraplengt=270)
tex_Cont_ex.grid(row=15,column=0)

'___________________________________________________________________________________________________'

#Frame de esclarecimentos

esclare = tk.LabelFrame(GUI,text='Esclarecimentos',padx=10,pady=10)
esclare.grid(row=4,column=0,columnspan=4)

tex_uni_ex = tk.Label(esclare,
                    text='Todas unidades estão no SI, então [m], [m/s²], [°], Kg, Kg/m³, W.',
                    width=155, 
                    wraplengt=1000)
tex_uni_ex.grid(row=0,column=0)

tex_elitsm_ex = tk.Label(esclare,
                    text='O elitismo é definido na seção "Quantas vezes o melhor será copiado", e ele funciona copiando o melhor indivíduo quantas vezes foi definido, o segundo melhor vai ser copiado metade dessa quantidade, e o terceiro 20%.',
                    width=155, 
                    wraplengt=1000)
tex_elitsm_ex.grid(row=1,column=0)

tex_pesos_ex = tk.Label(esclare,
                    text='A seção de pesos define o quão relevante o valor alcançado será para a nota final da asa. A nota final da asa será a média ponderada onde cada peso afetará seu respectivo valor.',
                    width=155, 
                    wraplengt=1200)
tex_pesos_ex.grid(row=2,column=0)

tex_pesos_ex = tk.Label(esclare,
                    text='Use uma velocidade levemente acima da velocidade de stall (1.1 a 1.3 x Vs) para conseguir valores próximos dos reais nas análises.',
                    width=155, 
                    wraplengt=1200)
tex_pesos_ex.grid(row=3,column=0)

tex_pesos_ex = tk.Label(esclare,
                    text='A seção sobre o CG é para verificar se o CG vazio teórico está próximo do centro aerodinâmico da asa, facilitando algumas decisões de projeto, se isso não lhe importa, coloque o peso igual a 0',
                    width=155, 
                    wraplengt=1200)
tex_pesos_ex.grid(row=4,column=0)

tex_aprox_ex = tk.Label(esclare,
                    text='Esse código utiliza uma pequena aproximação na seção de MTOW, em que ele só encontra valores de 0,2 em 0,2 kg, portanto os valores de MTOW podem estar levemente diferentes dos reais.',
                    width=155, 
                    wraplengt=1200)
tex_aprox_ex.grid(row=5,column=0)

tex_aprox_ex = tk.Label(esclare,
                    text='O algoritmo genético deve ser usado somente como uma base, recomendação, ou fator de estudo para a decisão da asa. Não leve o resultado encontrado pelo algoritmo como absoluto.',
                    width=155, 
                    wraplengt=1200)
tex_aprox_ex.grid(row=6,column=0)


'___________________________________________________________________________________________________'

#Botão para rodar o programa

#função

def mostra():

    janela_grafico = tk.Toplevel(GUI)
    janela_grafico.title('Gráfico')
    janela_grafico.geometry('822x691')
    
    img_grafico = Image.open('Imagens\grafico_resultado.png')
    graf_resize = img_grafico.resize((822,691), Image.Resampling.LANCZOS) #multiplo de 3291,2763
    graf_resiz  = ImageTk.PhotoImage(graf_resize)
    
    imagem_graf = tk.Label(janela_grafico,image=graf_resiz)
    imagem_graf.grid(row=0,column=0)
    
    tk.grid() #por algum motivo o tkinter so mostra a gráfico se tiver um erro kkkkkkkkk

def resultado():
    
    janela_resultado = tk.Toplevel(GUI)
    janela_resultado.title('Melhor asa')
    janela_resultado.geometry('400x740')
    
    frame_resultado = tk.LabelFrame(janela_resultado,text='Melhor asa encontrada',padx=10,pady=10)
    frame_resultado.grid(row=0,column=0)
    
    melhores = pd.read_excel('Resultados\Melhores asas de cada geração.xlsx')
    melhores = melhores.sort_values("Nota",ascending=False,ignore_index=True)
    
    colunas = melhores.columns.tolist()
    
    melhor = list(melhores.iloc[0])
    
    for k in range(len(melhor)):
        if isinstance(melhor[k],float) == True: #verifica se é float
            melhor[k]=round(melhor[k],3)        #da round no float pra ficar bonito
        
    j=0
    for i in colunas:
        
        texto_coluna = tk.Label(frame_resultado,text=i,font=('Arial',12), width=10)
        texto_coluna.grid(row=j,column=0)
        
        texto_valor = tk.Label(frame_resultado,text=melhor[j],font=('Arial',12), width=30)
        texto_valor.grid(row=j,column=1)
        
        j=j+1
    
    janela_grafico = tk.Toplevel(GUI)
    janela_grafico.title('Gráfico')
    janela_grafico.geometry('791x226')
    
    img_grafico = Image.open('Imagens\grafico_da_asa.png')
    graf_resize = img_grafico.resize((791,226), Image.Resampling.LANCZOS) #multiplo de 7906,2255
    graf_resiz  = ImageTk.PhotoImage(graf_resize)
    
    imagem_graf = tk.Label(janela_grafico,image=graf_resiz)
    imagem_graf.grid(row=0,column=0)
    
    tk.grid() #por algum motivo o tkinter so mostra a gráfico se tiver um erro kkkkkkkkk
    

def rodar():
    
    
    framecarre = tk.LabelFrame(GUI,padx=10,pady=10)
    framecarre.grid(row=5,column=3,columnspan=3)

    carre = tk.Label(framecarre,text='carregando...')
    carre.grid(row=0,column=0)
    
    progressbar = ttk.Progressbar(framecarre, orient='horizontal', length=200,mode='indeterminate')
    progressbar.grid(row=0,column=3)
    
    progressbar.start(50)
    
    butao.config(state='disabled')
    
    def codi():
            
        popg        = int(pop.get())
        elitismg    = int(elitism.get())
        probmutg    = float(probmut.get())
        probcrug    = float(probcru.get())
        quangeng    = int(quangen.get())
        bming       = float(bmin.get())
        bmaxg       = float(bmax.get())
        ARming      = float(ARmin.get())
        ARmaxg      = float(ARmax.get())
        TRming      = float(TRmin.get())
        TRmaxg      = float(TRmax.get())
        iming       = float(imin.get())
        imaxg       = float(imax.get())
        torming     = float(tormin.get())
        tormaxg     = float(tormax.get())
        didming     = float(didmin.get())
        didmaxg     = float(didmax.get())
        velocidadeg = float(V.get())
        densidadeg  = float(phi.get())
        atritog     = float(mu.get())
        potenciag   = float(P.get())
        peso_CPg    = float(CP.get())
        peso_Estag  = float(Est.get())
        peso_Contrg = float(Cont.get())
        peso_CGg    = float(CG.get())
        alturag     = float(H.get())
        
        
        Codigo_genetico(popg,
                        elitismg,
                        probmutg,
                        probcrug,
                        quangeng,
                        bming,
                        bmaxg,
                        ARming,
                        ARmaxg,
                        TRming,
                        TRmaxg,
                        iming,
                        imaxg,
                        torming,
                        tormaxg,
                        didming,
                        didmaxg,
                        velocidadeg,
                        densidadeg,
                        atritog,
                        potenciag,
                        alturag,
                        peso_CPg,
                        peso_Estag,
                        peso_Contrg,
                        peso_CGg
                        )
        
        framecarre.grid_forget()
        
        frambut_graf = tk.LabelFrame(GUI,
                                highlightbackground="blue", 
                                highlightcolor="blue", 
                                highlightthickness=4)
        frambut_graf.grid(row=5,column=0,pady=25)

        butao_graf = tk.Button(frambut_graf, text='Mostrar Gráfico',command=mostra,height=2, width=30)
        butao_graf.grid(row=0,column=0)
        
        frambut_resul = tk.LabelFrame(GUI,
                                highlightbackground="green", 
                                highlightcolor="green", 
                                highlightthickness=4)
        frambut_resul.grid(row=5,column=3,columnspan=2,pady=25)
        
        butao_resul = tk.Button(frambut_resul, text='Mostrar Melhor Asa',command=resultado,height=2, width=30)
        butao_resul.grid(row=0,column=0,)
        
        butao.config(state='active')
        
    threading.Thread(target=codi).start()


#local e formato

frambut = tk.LabelFrame(GUI,
                        highlightbackground="orange", 
                        highlightcolor="orange", 
                        highlightthickness=4)
frambut.grid(row=5,column=1,columnspan=2,pady=25)

butao = tk.Button(frambut, text='Rodar o algoritmo genético',command=rodar,height=2, width=30)
butao.grid(row=0,column=0)



GUI.mainloop()
