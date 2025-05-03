# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 20:09:03 2022

@author: datomi
"""

import pandas as pd
import numpy as np
import math
import sympy as sy

#Código das análises e cáculos do código geral do artigo

def LLT_interno(b:float,       #interno
                mac:float,
                twist:float,
                Cla:float,
                alpha_0:float,
                i_w:float,
                Cr:float,
                C1:float,
                C2:float,
                Ct:float,
                b1:float,
                b2:float,
                b3:float
                ):
    
    N = 10
    pi = math.pi
    
    lista_Cr = [Cr,C1,C2]
    lista_Ct = [C1,C2,Ct]
    lista_b  = [b1,b2,b3]
    
    x=sy.symbols('x')
    
    segmentos=[]

    for i in range(len(lista_b)):
        if i == 0:
            linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/((lista_b[i]-0)+0.001))*(x-0))
        if i > 0:     
            linha = lista_Cr[i] + (((lista_Ct[i]-lista_Cr[i])/((lista_b[i]-lista_b[i-1])+0.001))*(x-lista_b[i-1]))
        
        segmentos.append(linha)

    listax = np.linspace(0,lista_b[len(lista_b)-1],N) #divido N vezes
    listay = []
    listacont = np.arange(1,len(lista_b),1)

    for x in listax:
        
        if x <= lista_b[0]:
            y = eval(str(segmentos[0]))
        
        if x >= lista_b[0]:
            for i in listacont:
                if x > lista_b[i-1] and x < lista_b[i]:
                    y = eval(str(segmentos[i]))
                    
        listay.append(y)
    

    alpha_twist = twist         

    theta = np.linspace((pi / (2 * N)), (pi / 2), N, endpoint=True)

    alpha = np.linspace(i_w + alpha_twist, i_w, N) 
    
    listay = listay[::-1]
    
    c = np.array(listay)

    mu = c * Cla / (4 * b)

    LHS = (mu * (np.array(alpha) - alpha_0))/(180/pi)

    RHS = []
    for i in range(1, 2 * N + 1, 2):
        RHS_iter = np.sin(i * theta) * (1 + (mu * i) / (np.sin(list(theta))))
        RHS.append(RHS_iter)

    test = np.asarray(RHS)
    x = np.transpose(test)
    inv_RHS = np.linalg.inv(x)
        
    A = np.matmul(inv_RHS, LHS) 
    
    AR = b/mac
    
    CL_wing = (pi * AR * A[0])

    return(CL_wing)



def peso_de_superf(pontos,
                   TReff:float,
                   lista_Cr:list,
                   lista_Ct:list,
                   lista_b:list,
                   ):
    
    phi=159.52            #[kg/m³] densidade do material da asa
    phil=159.52           #[kg/m³] densidade do material da longarina
    phi_monk = 0.067812   #[kg/m²] densidade(EM AREA) do monokote
    esp=0.002             #[m]     Espessura da asa
    espn=0.002            #[m]     Espessura da nervura 
    Acir=0.01             #[%]     Área retirada do perfil com os circulos nas nervuras
    
    perfil = pontos
    
    TR = TReff
    
    b = lista_b[-1]*2
    
    '___________________________________________________________________________'
    
    'calculo da corda média'
    
    lista_S = []
    lista_C = []

    for i in range(len(lista_b)):
        
        TR_i = lista_Ct[i]/lista_Cr[i]
        cmac=(2/3)*lista_Cr[i]*((1+TR_i+(TR_i**2))/(1+TR_i))
        
        if i == 0:
            S_i = lista_b[i]*cmac
        if i > 0:
            S_i = (lista_b[i]-lista_b[i-1])*cmac
        
        S_i = S_i*2
        
        lista_C.append(cmac)
        lista_S.append(S_i)

    soma = sum(lista_S)
    soma_cima = 0
    for i in range(len(lista_C)):
        
        soma_cima = soma_cima + (lista_C[i]*lista_S[i])
    
    cmac = soma_cima/soma

    '___________________________________________________________________________'
    
    
    Alon=(cmac*b)/2300             #[m²] Área da longarina APROXIMAÇÃO
    q=math.ceil(b*12)              #[Nº] Quantidade de nervuras APROXIMAÇÃO
        
    listacontar = np.arange(1,70,1)

    if TR == 1:

        xa=perfil.iloc[:,0]
        ya=perfil.iloc[:,1]
        
        vx=list(map(lambda i: float(i)*cmac,xa))
        vy=list(map(lambda i: float(i)*cmac,ya))
                
        
        listac=range(len(vy)-1)
        ht=0
        for i in listac:
            
            h=(((vy[i+1]-vy[i])**2)+(vx[i+1]-vx[i])**2)**0.5
            
            ht=ht+h                                                     #comprimento
        
        at=0
        for i in listac:
 
            A1 = min([abs(vy[i]),abs(vy[i+1])]) * abs(vx[i+1] - vx[i])  #retangulo
            
            A2 = abs(vy[i] - vy[i+1]) * abs(vx[i+1] - vx[i])            # triangulo
            
            at=at+A1+A2
            
        
        area_molhada = ht * b
        
        area_lateral = at
        
    if TR != 1:             
        
        area_molhada = 0
        
        area_lateral = 0
        
        n_segmentos = len(lista_b)
        
        def calc(ht1,at1):
            for i in listac:
                
                h=(((vy[i+1]-vy[i])**2)+(vx[i+1]-vx[i])**2)**0.5

                A1 = min([abs(vy[i]),abs(vy[i+1])]) * abs(vx[i+1] - vx[i])  #retangulo
                
                A2 = abs(vy[i] - vy[i+1]) * abs(vx[i+1] - vx[i])            # triangulo
                
                at1=at1+A1+A2   #área lateral do perfil
                ht1=ht1+h       #perimetro do perfil
                
            return (ht1,at1)
                
        for k in range(n_segmentos):
            
            if k > 0:
                bi = lista_b[k] - lista_b[k-1]
            else:
                bi  = lista_b[k]
            
            b_local = round(bi * 2,3)
            
            Cr_local = lista_Cr[k]
            
            Ct_local = lista_Ct[k]
            
            x = sy.symbols('x')
            
            eq = Cr_local + ((Ct_local - Cr_local)/(b_local+0.0000001)*x)
            
            ht=0
            at=0
            
            for j in listacontar:
                
                x = b_local * (j/len(listacontar))
                
                cmacd = eval(str(eq))

                vx=[]
                vy=[]
                
                ht1=0
                
                xa=perfil.iloc[:,0]
                ya=perfil.iloc[:,1]
             
                vx=list(map(lambda m: float(m)*cmacd,xa)) #mesma coisa q um for loop..
                vy=list(map(lambda m: float(m)*cmacd,ya)) #com oq tem dps do lambda

                              
                listac=range(len(vy)-1)
                
                ht1,at1=calc(0,0)
    
                ht=ht+ht1     
                at=at+at1
            
            at=at/(len(listacontar))     #área lateral do perfil média
            ht=ht/(len(listacontar))     #perimetro do perfil

            area_molhada = area_molhada + ht*b_local
            
            area_lateral = area_lateral + at
        
        area_lateral = area_lateral/n_segmentos

    V1 = ((area_lateral*(1-Acir))-Alon)*espn*(q-2)

    V2 = area_lateral*espn*2

    V3=area_molhada*esp
    
    m_monokote = area_molhada * phi_monk
    
    m=(V1+V2+V3)*phi
    
    ml=b*Alon*phil

    mt = m + ml + m_monokote
    
    return(mt,area_molhada)

def CL(df,
       velocidade:float):
    
    lista_de_perfis = pd.read_excel('Perfil/Perfil_df.xlsx')
    
    for i in range(len(df)):
        
        perfil = df.iloc[i,1]
                
        b = df.iloc[i,2]
                
        mac = df.iloc[i,6]
        
        Cr = df.iloc[i,8]
        
        C1 = df.iloc[i,9]
        
        C2 = df.iloc[i,10]
        
        Ct = df.iloc[i,11]
        
        b1 = df.iloc[i,12]
        
        b2 = df.iloc[i,13]
        
        b3 = df.iloc[i,14]
        
        twist = df.iloc[i,17]

        for j in range(len(lista_de_perfis)):
            if lista_de_perfis.iloc[j,0] == perfil:
                index_do_perfil = j
                break
        
        Re = mac*velocidade/0.000015111
        
        x = Re/10000
        
        alpha0  = float(eval(str(lista_de_perfis.iloc[index_do_perfil,3])))
        
        Cl0  = float(eval(str(lista_de_perfis.iloc[index_do_perfil,4])))
        
        Clalpha = float(eval(str(lista_de_perfis.iloc[index_do_perfil,6])))
        
        Clalpha = Clalpha*180/math.pi
                
        CL1 = LLT_interno(b,mac,twist,Clalpha,alpha0,3,Cr,C1,C2,Ct,b1,b2,b3)

        CL2 = LLT_interno(b,mac,twist,Clalpha,alpha0,7,Cr,C1,C2,Ct,b1,b2,b3)

        CLalpha = (CL2 - CL1) / (7 - 3)
        CL0 = CL2 - (CLalpha*7)
        
        if alpha0 == 0 and Cl0 == 0 :
            
            CL0 = 0
        
        df.iloc[i,19] = round(CL0,4)
        df.iloc[i,20] = round(CLalpha,4)
        
        Re=x #só pra tirar o aviso de erro chato        
        
    return(df)


def CD(df,
       velocidade:float,
       altura:float,):
    
    lista_de_perfis = pd.read_excel('Perfil/Perfil_df.xlsx')
        
    for i in range(len(df)):
        
        perfil = df.iloc[i,1]
        
        for j in range(len(lista_de_perfis)):
            if lista_de_perfis.iloc[j,0] == perfil:
                index_do_perfil = j
                break
        
        Cd0_w   = str(lista_de_perfis.iloc[index_do_perfil,7])
        
        t_cw    = lista_de_perfis.iloc[index_do_perfil,10]
        
        b = df.iloc[i,2]
        
        AR = df.iloc[i,3]
        
        mac = df.iloc[i,6]
        
        S = df.iloc[i,7]
        
        i_w = df.iloc[i,15]
       
        CL0 = df.iloc[i,19]
        
        CLalpha = df.iloc[i,20]
        
        h = altura
        
        V = velocidade
        
        C1 = 10.6264982037274*(1/(2*math.pi)**0.5)*math.exp(-((AR**2)/2)) + 0.106013870344867*math.atan(AR)*180/math.pi + 0.455690445917242*AR**2 - 5.11788525427153*AR + 7.76073604035651

        if AR > 6:
            
            C1 = 0
        
        '______________________________________________________'
        
        #estabilizadores
        
        ARh = (2/3)*(b/mac)  #aproximação de Sadraey
        
        bh = (b)/2.5           #aproximação
        
        ch = bh/ARh
        
        Sh  = ((bh**2)/ARh)
        
        Sv = 2*(0.6645*Sh - 0.05948) #valor aproximado vendo os outros projetos
        
        ARv = 1.5  #aproximação de Sadraey
            
        macv = (Sv/ARv)**0.5    
        
        for j in range(len(lista_de_perfis)):
            if lista_de_perfis.iloc[j,0] == 'NACA 0015':
                index_do_perfil = j
                break
        
        Cd0_ht    = str(lista_de_perfis.iloc[index_do_perfil,7])
        
        Cd0_vt    = Cd0_ht
        
        t_cht     = lista_de_perfis.iloc[index_do_perfil,10]
        
        t_cvt     = t_cht
        
        '______________________________________________________'
        
        #fuselagem
        
        alt = h/2
        
        dff = 0.15
        
        largura = 0.1
        
        dist_nariz_a_asa = 0.4
        
        lh = (0.4*S*mac/Sh)
        
        dist_nariz_cg = dist_nariz_a_asa + mac*1/4 # [m]
        
        lf = (dist_nariz_cg + lh) * 0.7 #ajuste de projeto
        
        area_molhada_lados = 2 * lf * alt 
        
        area_molhada_horizontais = 2 * lf * largura
        
        Swetf = area_molhada_lados + area_molhada_horizontais
        
        '______________________________________________________'

        Re = V*mac/0.000015111
        Reht = V*ch/0.000015111
        Revt = V*macv/0.000015111
        Ref  = V*lf//0.000015111
        
        '______________________________________________________'
        
        #Cd0s
        
        x = Re/10000
        
        Cd0w = eval(Cd0_w)
        
        x = Reht/10000
        
        Cd0ht = eval(Cd0_ht)
        
        x = Revt/10000
        
        Cd0vt = eval(Cd0_vt)
        
        Cd0f  = 1.2         #paralelepipedo 
        
        '______________________________________________________'

        M = V/343
        
        CFw  = 0.42/(math.log10(Re)**2.58)
        CFht = 0.42/(math.log10(Reht)**2.58)
        CFvt = 0.42/(math.log10(Revt)**2.58)
        CFf  = 0.42/(math.log10(Ref)**2.58)

        fM = 1 - 0.08*(M**1.45)

        fld = 1 + (60/((lf/dff)**3))+(0.0025*(lf/dff))

        ftcw  = 1 + (2.7*(t_cw))  + (100*(t_cw**4))
        ftcht = 1 + (2.7*(t_cht)) + (100*(t_cht**4))
        ftcvt = 1 + (2.7*(t_cvt)) + (100*(t_cvt**4))

        CD0w   = CFw  * ftcw  * fM * 2.1   * ((Cd0w/0.004)**0.4)
        CD0ht  = CFht * ftcht * fM * 2  * ((Cd0ht/0.004)**0.4)
        CD0vt  = CFvt * ftcvt * fM * 2  * ((Cd0vt/0.004)**0.4)
        CD0f   = CFf  * fld   * fM * (Swetf/S)   * ((Cd0f/0.004)**0.4)

        CD0_Total = CD0w + CD0ht + CD0vt + CD0f
        
        '______________________________________________________'
        
        #calculo do CD
                
        CLmax = (CLalpha * i_w) + CL0 + (C1*(i_w*math.pi/180)**2)

        e = 1/(1.05+(0.007*math.pi*AR)) #oswald.pdf

        CDi = (CLmax**2)/(math.pi*e*AR)

        solo = ((16*h/b)**2)/(1+((16*h/b)**2))

        CDi_decolagem = solo*CDi

        CD = CDi_decolagem + CD0_Total
        
        df.iloc[i,21] = round(CD,4)
        
        solo = x #IGNORA!!   isso só para tirar uma mensagem irritante
    
    return(df)

def CLmax_velocidade(mac:float,
                     S:float,
                     b:float,
                     taper:float,
                     twist:float,
                     velocidade:float,
                     lista_de_perfis,
                     perfil,
                     a_s:float,
                     i_w:float,
                     imax:float,
                     enflechamento:float,
                     Cr:float,
                     C1:float,
                     C2:float,
                     Ct:float,
                     b1:float,
                     b2:float,
                     b3:float
                     ):
    
    Re = mac*velocidade/0.000015111

    x=Re/10000
    
    AR = b/mac
    
    C1r = 10.6264982037274*(1/(2*math.pi)**0.5)*math.exp(-((AR**2)/2)) + 0.106013870344867*math.atan(AR)*180/math.pi + 0.455690445917242*AR**2 - 5.11788525427153*AR + 7.76073604035651

    if AR > 6:
        
        C1r = 0
    
    for j in range(len(lista_de_perfis)):
        if lista_de_perfis.iloc[j,0] == perfil:
            index_do_perfil = j
            break
    
    alpha0  = float(eval(str(lista_de_perfis.iloc[index_do_perfil,3])))
    
    Clalpha = float(eval(str(lista_de_perfis.iloc[index_do_perfil,6])))
    
    CL1 = LLT_interno(b,mac,twist,Clalpha,alpha0,3,Cr,C1,C2,Ct,b1,b2,b3)

    CL2 = LLT_interno(b,mac,twist,Clalpha,alpha0,7,Cr,C1,C2,Ct,b1,b2,b3)

    CLalpha = (CL2 - CL1) / (7 - 3)
    CL0 = CL2 - (CLalpha*7)
    
    if a_s > 21 :
        a_s = 1
    
    CLmax = (CLalpha * a_s) + CL0  + (C1r*(a_s*math.pi/180)**2)
    
    CLmax = CLmax * (1-(0.002*abs(enflechamento)))
    
    Re=x

    
    return(CLmax)

def analise_controle(df,
                     densidade:float,
                     velocidade:float):
    
    
    for i in range(len(df)):
    
        S = df.iloc[i,7]
        
        b = df.iloc[i,2]
        
        mac = df.iloc[i,6]
        
        CLalpha = (df.iloc[i,20])*180/3.14159265358979
        
        cr = df.iloc[i,8]
        
        TR = df.iloc[i,5]
        
        phi0 = densidade
        
        Vc = velocidade
        
        yDr=0.4*(b/2)     #Centro de arrasto, de acordo com a linha de referência da fuselagem eixo y
        poi=0.7*(b/2)     #posição inicial do aileron em uma só asa (eixo y): entre 0.5 e 0.65
        pof=0.9*(b/2)     #posição final do aileron em uma só asa   (eixo y): entre 0.8 e 0.95
        cac=0.20          #razão entre o comprimento do aileron e o comprimeito da asa eixo(x)
        deltaa=20         #deflexão dos ailerons
        
        bank=30     #bank angle escolhido para os ailerons EM GRAUS
        treq3=2.6   #lv 3 tempo requerido para alcançar o bank angle
        treq2=1.8   #lv 2 tempo requerido para alcançar o bank angle
        treq1=1.3   #lv 1 tempo requerido para alcançar o bank angle
        Cdr=1.2     #Coeficiente de arrasto durante a rolagem (entre 0.7 e 1.2)
        
        yi=poi                         #Posição do início do aileron, eixo y(do cg até a ponta da asa)
        y0=pof                         #Posição do fim do aileron, eixo y
        
        ARh = (2/3)*(b/mac)  #aproximação de Sadraey
        
        if ARh < 3:
            ARh = 3      #recomendação
        
        Sh  = (((b/3)**2)/ARh)
        
        Sv = 0.66454*Sh - 0.05948 #valor aproximado vendo os outros projetos
        
        Ixx = 0.9905*S - 0.5633  #valor aproximado vendo os outros projetos
        
        At=0.962* (cac)**(1/2) - 0.0321
    
        Cl_delta_A = ((2*CLalpha*At*cr)/(S*b))*((((y0**2)/2)+(2/3)*((TR-1)/b)*(y0**3))-(((yi**2)/2)+(2/3)*((TR-1)/b)*(yi**3)))
    
        deltaa=deltaa/57.3 #transformação em rad
    
        C1=Cl_delta_A*deltaa
    
        LA=0.5*phi0*(Vc**2)*S*C1*b 
    
        Pss=(2*LA/(phi0*(S+Sh+Sv)*Cdr*(yDr**3)))**0.5
    
        bank1=(Ixx/(phi0*(yDr**3)*(S+Sh+Sv)*Cdr))*math.log((Pss)**2) #lembrar que esse log é ln
    
        Pponto=(Pss**2)/(2*bank1) 
    
        teste = (((bank*math.pi/180)*2)/Pponto)

        if (bank1*180/3.14) >= bank:
            if teste < 0:
                tf = 5
            if teste > 0:
                tf=(((bank*math.pi/180)*2)/Pponto)**0.5    #Sadraey n fala, mas no exemplo ele transforma o bank em rad
    
        if (bank1*180/3.14) < bank:
            if teste < 0:
                tf = 5
            if teste > 0:
                tss=(((bank1*math.pi/180)*2)/Pponto)**0.5
                t2=(((bank*math.pi/180)*2)/Pponto)**0.5
                bank2=Pss*(t2-tss)+bank1
                tf=tss+((bank2-bank1)/Pss)
        
        try:
            if tf<=treq1:
                nivel = 1
            if tf<=treq2 and tf>treq1:
                nivel = 2
            if tf<=treq3 and tf>treq2:
                nivel = 3
            if tf<=treq3+0.5 and tf>treq3:
                nivel = 3.5
            if tf>treq3+0.5:
                nivel = 4
        except:
            nivel = 4
        
        df.iloc[i,24] = nivel
    
    return(df)

def simps(f,m,a,b,N=50):
    
    dx = (b-a)/N
    V = np.linspace(a,b,N+1)
    y = eval(f)
    l = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    return l,V

def MTOW(df,
         potencia:float,
         velocidade:float,
         densidade:float,
         atrito:float,
         altura:float,
         imax:float):
    
    
    V = velocidade
    rho = densidade
    
    # T = potencia*0.6/V
    T = -0.04907*(V**2) + 0.3868*V + 37.12                               #Tração do Elétrico + 17x10
    # T = -0.08447*(V**2) + 1.053*V + 35.14                                #nova hélice
    
    mu =  atrito                   #Coeficiente de atrito []
    g = 9.81                       #Aceleração gravitacional [m/s²]
    S_max = 58 - 0.7               #Restrição de pista [m]
    h = altura                     #[m] altura da asa em relação ao solo

    Δm = 0.2
    
    h_obs = 0.7 #altura do obstaculo

    lista_de_perfis = pd.read_excel('Perfil/Perfil_df.xlsx')

    for i in range(len(df)):
        
        perfil = df.iloc[i,1]
        
        for j in range(len(lista_de_perfis)):
            if lista_de_perfis.iloc[j,0] == perfil:
                index_do_perfil = j
                break
        
        b = df.iloc[i,2]    
        
        AR = df.iloc[i,3]
        
        taper = df.iloc[i,5]
        
        mac = df.iloc[i,6]
        
        S = df.iloc[i,7]
        
        Cr = df.iloc[i,8]
        
        C1 = df.iloc[i,9]
        
        C2 = df.iloc[i,10]
        
        Ct = df.iloc[i,11]
        
        b1 = df.iloc[i,12]
        
        b2 = df.iloc[i,13]
        
        b3 = df.iloc[i,14]
        
        i_w = df.iloc[i,15]
        
        lamb = df.iloc[i,16]
        
        twist = df.iloc[i,17]
        
        CL0 = df.iloc[i,19]
        
        CLa = df.iloc[i,20]
        
        CD = df.iloc[i,21]
        
        Re = mac*velocidade/0.000015111
        
        x = Re/10000
        
        a_s_perfil = float(eval(str(lista_de_perfis.iloc[index_do_perfil,2])))
        
        a_s = round(a_s_perfil,0)*0.9
        
        if a_s > 21 :
            a_s = 1
        
        C1r = 10.6264982037274*(1/(2*math.pi)**0.5)*math.exp(-((AR**2)/2)) + 0.106013870344867*math.atan(AR)*180/math.pi + 0.455690445917242*AR**2 - 5.11788525427153*AR + 7.76073604035651

        if AR > 6:
            
            C1r = 0
        
        '___________________efeito solo___________________'
        
        didiv_AR = 0.195729679631324*(2*h/b) - 2.54016228375777e-5*(2*h/b)**(-3) + 1.04883297007381*(2*h/b)*math.exp(-(2*h/b)) + 0.336121232721402
        
        if 2*h/b > 2:
            
            didiv_AR = 1
        
        M = V/343
        
        beta = (1 - M**2)**0.5
        
        CLa1 = (2*math.pi*AR)/(2+(4+(AR**2 * beta**2 *(1+(0/beta**2))))**0.5)
        
        AR_temp = AR/didiv_AR
        
        CLa2 = (2*math.pi*AR_temp)/(2+(4+(AR_temp**2 * beta**2 *(1+(0/beta**2))))**0.5)
        
        CL_solo_conservativo = CLa2/CLa1
        
        '___________________CL___________________'
        
        CLa = CLa * CL_solo_conservativo
        
        CLR = (CLa * i_w) + CL0 + (C1r*(i_w*math.pi/180)**2)
        
        CL = CLR * (1-(0.002*abs(lamb)))
                
        got_mtow = False
        _trigger = False    
        
        V = sy.symbols('V')
        m = sy.symbols('m')
        
        para_por_favor = False
        
        T = -0.04907*(V**2) + 0.3868*V + 37.12                        #Tração do Elétrico + 17x10

        L = (rho * (V**2) * S * CL)/2
        D = (rho * (V**2) * S * CD)/2
        
        W = m*g
        Fat = mu*(W-L)   
        
        ΣFx = T - Fat - D 
        ΣFy = L - W                      
          
        ΣFx = T - Fat - D 
        ΣFy = str(L - W)                      
        ΣFx = str(T - Fat - D )
        
        q = .5*rho*V**2
        Equation = str(V/( g*( (T/W - mu) - (CD -mu*CL)*q/(W/S)) ) )
        
        contagem = list(np.arange(8,30,0.1))
        
        m = df.iloc[i,22] * 3             #começa o MTOW com 3x o peso pra acelerar o processo
        
        while got_mtow is not True:
            
            if L == 0:
                got_mtow = True
                _trigger = True
                m = 5

            for V in contagem:
                if eval(ΣFy)>=0:
                    V_to = V
                    break
            
            try:
                CL_max = CLmax_velocidade(mac,S,b,taper,twist,V_to,lista_de_perfis,perfil,a_s,i_w,imax,lamb,Cr,C1,C2,Ct,b1,b2,b3)
            except:
                V_to=velocidade
                CL_max = CLmax_velocidade(mac,S,b,taper,twist,V_to,lista_de_perfis,perfil,a_s,i_w,imax,lamb,Cr,C1,C2,Ct,b1,b2,b3)
            
            V_estol = ( 2*W/(rho*S*CL_max))**0.5
            
            ΔCL = eval(str(0.5*((V_to/V_estol)**2 - 1)*(CL*((V_estol/V_to)**2 - 0.53) + 0.38)))
            R_tr = eval(str(2*((W/S)/(rho*g*ΔCL))))
            
            try:
                
                SG,nada = simps(Equation,m,0,V_to)                                 #Comprimento de pista [m] [Eq. 10.8 Roskam]
                θCL = eval(str((eval(ΣFx))/W))                                     #[rad] angulo de subida   
                
                if θCL < 0:
                    got_mtow = True
                    _trigger = True
                    m = 5
                
                S_tr = R_tr*math.sin(θCL)*0.3048   #de ft pra metro
                
                H_tr =  S_tr*θCL/2


                if H_tr > h_obs:
                    
                    S_CL = 0
                    
                else:
                    
                    S_CL = (h_obs - H_tr)/math.tan(θCL)
                    

                S_total = SG + S_tr + S_CL
                
                
            except :
                for V in contagem:
                    if eval(ΣFy)>=0:
                        V_to = V
                        break
                    
                m-= Δm
                _trigger = True
                
                
            "Correção caso passe do limite"
            if S_total > S_max:
                m -= Δm 
                
                _trigger = True
                 
            else:
                pass
                 
            if _trigger is True:
                 
                    MTOW = round(m,3)
                    
                    got_mtow = True
            
                    _trigger = False
                    
                    if MTOW == round((df.iloc[i,22] * 3),3) or MTOW == round((df.iloc[i,22] * 3) - 0.2,3): #ajuste feito pra quando o avião já é muito pesado
                        
                        if para_por_favor == True:
                                # print('parei!')
                                got_mtow = True
                                
                                MTOW = round(m,3)
                        
                                _trigger = False
                                
                                break
                        else:
                            
                            m = df.iloc[i,22]*1
                            
                            para_por_favor = True
                            
                            got_mtow = False
                            
                            _trigger = False
                            # print('oi')
                            # pass
                        
                    
                    
            m += Δm
        
        # while got_mtow is not True:
            
        #     if L == 0:
        #         got_mtow = True
        #         _trigger = True
        #         m = 5


        #     "Obtém velocidade de decolagem, i.e L>W"    
        #     for V in np.arange(1,30,0.1):
        #         if eval(ΣFy)>=0:
        #             V_to = V
        #             break
            
        #     print('\n',V_to)
        #     print(eval(ΣFy))
            
        #     try:
        #         CL_max = CLmax_velocidade(mac,S,b,taper,twist,V_to,lista_de_perfis,perfil,a_s,i_w,imax,lamb,Cr,C1,C2,Ct,b1,b2,b3)
        #     except:
        #         V_to=velocidade
        #         CL_max = CLmax_velocidade(mac,S,b,taper,twist,V_to,lista_de_perfis,perfil,a_s,i_w,imax,lamb,Cr,C1,C2,Ct,b1,b2,b3)

        #     V_estol = ( 2*W/(rho*S*CL_max))**0.5
            
        #     if math.isnan(V_estol):
        #         V_estol = 14
            
        #     ΔCL = 0.5*((V_to/V_estol)**2 - 1)*(CL*((V_estol/V_to)**2 - 0.53) + 0.38)
        #     R_tr = 2*((W/S)/(rho*g*ΔCL))
            
        #     # print('V =',round(V_to,1))
            
        #     "Comprimento de pista para decolar"
        #     try:

                
        #         SG,nada = simps(Equation,0,V_to)                                    #Comprimento de pista [m] [Eq. 10.8 Roskam]
        #         θCL = (eval(ΣFx))/W                       #[rad] angulo de subida 
                                  
        #         S_tr = R_tr*math.sin(θCL)*0.3048   #de ft pra metro

        #         H_tr =  S_tr*θCL/2
                              
             
        #         if H_tr > h_obs:
                    
        #             S_CL = 0
                    
        #         else:
                    
        #             S_CL = (h_obs - H_tr)/math.tan(θCL)
                    
        #         S_total = SG + S_tr + S_CL
                
        #     except :
        #         for V in np.arange(1,30,0.1):
        #             if eval(ΣFy)>=0:
        #                 V_to = V
        #                 break
                    
        #         m-= Δm
        #         _trigger = True
                
                
        #     "Correção caso passe do limite"
        #     if S_total > S_max:
        #         m -= Δm 
                
        #         _trigger = True
                 
        #     else:
        #         pass
                 
        #     if _trigger is True:
             
        #         MTOW = round(m,3)
                
        #         got_mtow = True
        
        #         _trigger = False
                
        #         if MTOW == round((df.iloc[i,22] * 3),3) or MTOW == round((df.iloc[i,22] * 3) - 0.2,3): #ajuste feito pra quando o avião já é muito pesado
                    
        #             if para_por_favor == True:
        #                     # print('parei!')
        #                     got_mtow = True
                            
        #                     MTOW = round(m,3)
                    
        #                     _trigger = False
                            
        #                     break
        #             else:
                        
        #                 m = df.iloc[i,22]*1
                        
        #                 para_por_favor = True
                        
        #                 got_mtow = False
                        
        #                 _trigger = False
        #                 # print('oi')
        #                 # pass
                    
                
                
        #     m += Δm
        #     # print('m =',round(m,1))

        
        df.iloc[i,26] = MTOW
        Re=x

    return(df)



def Calculo_do_peso(df,
                    altura:float):

    lista_de_perfis = pd.read_excel('Perfil/Perfil_df.xlsx')
    
    phi_fita = 970        #[kg/m³] densidade da fita adesiva
    
    #peso dos componentes fixos
    
    dist_nariz_a_asa = 0.4
    
    P_bequilha = 0.2
    
    CG_bequilha  = 0.15
    
    P_bateria = 0.52 + 0.1218  #motor + servos
    
    CG_bateria = 0.3
    
    P_Helices = 0.02
    
    CG_helice = 0.0165
    
    P_motor = 0.408
    
    CG_motor = 0.061
    
    P_fios = 0.22
    
    P_servos = 4*0.06
    
    P_fixos = P_bateria + P_Helices + P_motor + P_fios + P_servos + P_bequilha
    
    for i in range(len(df)):
        
        perfil = df.iloc[i,1]
        
        for j in range(len(lista_de_perfis)):
            if lista_de_perfis.iloc[j,0] == perfil:
                index_do_perfil = j
                break
        
        nome_do_arquivo_do_perfil = str(lista_de_perfis.iloc[index_do_perfil,1])
        
        pontos = pd.read_csv('Perfil/desenho dos perfis/'+nome_do_arquivo_do_perfil+'.dat',delimiter=' ')
        
        b = df.iloc[i,2]    
        
        S = df.iloc[i,7]   
        
        taper = df.iloc[i,5]
        
        mac = df.iloc[i,6]
        
        Cr = df.iloc[i,8]
        
        C1 = df.iloc[i,9]
        
        C2 = df.iloc[i,10]
        
        Ct = df.iloc[i,11]
        
        b1 = df.iloc[i,12]
        
        b2 = df.iloc[i,13]
        
        b3 = df.iloc[i,14]
        
        CG_fios = dist_nariz_a_asa + mac*1/4
        
        CG_servos = dist_nariz_a_asa + mac*1/4
         
        #peso da asa
        
        lista_Cr = [Cr,C1,C2]
        lista_Ct = [C1,C2,Ct]
        lista_b = [b1,b2,b3]
        
        P_asa,Sweta = peso_de_superf(pontos,taper,lista_Cr,lista_Ct,lista_b)
        
        CG_asa = dist_nariz_a_asa + mac*1/4
        
        #peso da cauda
        
        ARh = (2/3)*(b/mac)  #aproximação de Sadraey
        
        bh = (b)/2.5           #aproximação
        
        ch = bh/ARh
        
        lista_Crh = [ch,ch]
        lista_Cth = [ch,ch]
        lista_bh = [0,bh/2]
        
        P_cauda_h,Sweth = peso_de_superf(pontos,1,lista_Crh,lista_Cth,lista_bh)
        
        Sh  = ((bh**2)/ARh)
        
        Sv = 2*(0.6645*Sh - 0.05948) #valor aproximado vendo os outros projetos
        
        ARv = 1.5  #aproximação de Sadraey
            
        macv = (Sv/ARv)**0.5
        
        bv = Sv/macv
        
        lista_Crv = [macv,macv]
        lista_Ctv = [macv,macv]
        lista_bv = [0,bv/2]
        
        P_cauda_v,Swetv = peso_de_superf(pontos,1,lista_Crv,lista_Ctv,lista_bv)
                
        #aproximação do peso da fuselagem
        
        dist_nariz_cg = dist_nariz_a_asa + mac*1/4 # [m]
        
        lh = (0.4*S*mac/Sh)              # [m]
        
        largura = 0.1 # [m]
        alt = altura/2  # [m]
        
        densidade = 1451   #[kg/m³] está na lista de inputs!!!
        kg_resina_por_suporte = 0.02 # [kg]
        
        diametro_interno = 0.003 # [m]
        diametro_externo = 0.005 # [m]
        
        dist_para_suporte = 0.15 # [m]
        
        area_externa_certa = math.pi*(diametro_externo**2)/4
        area_interna_certa = math.pi*(diametro_interno**2)/4
        
        area_total = area_externa_certa - area_interna_certa
        
        Comprimento_da_fuselagem_total = (dist_nariz_cg + lh) * 0.7 #ajuste de projeto
        
        CG_h = Comprimento_da_fuselagem_total + ((1/4)*ch)  #CG
        
        CG_v = Comprimento_da_fuselagem_total + ((1/4)*macv)  #CG
        
        volume_tubos_no_eixo_x = Comprimento_da_fuselagem_total * 4 * area_total
        
        qtd_de_suportes = Comprimento_da_fuselagem_total // dist_para_suporte 
        
        volume_tubos_no_eixo_y =  2 * qtd_de_suportes * largura * area_total
        
        comprimento_do_tubo_de_suporte = ((dist_para_suporte**2) + (alt**2))**0.5
        
        volume_tubos_de_suporte_vertical = 2 * qtd_de_suportes * comprimento_do_tubo_de_suporte * area_total
        
        volume_total = volume_tubos_no_eixo_x + volume_tubos_no_eixo_y + volume_tubos_de_suporte_vertical
        
        massa_fuselagem = volume_total * densidade
                
        massa_da_resina = 4 * qtd_de_suportes * kg_resina_por_suporte
        
        P_fus = massa_fuselagem + massa_da_resina
        
        CG_fus = Comprimento_da_fuselagem_total/2
        
        # entelagem de fita na fuselagem:
        
        area_molhada_lados = 2 * Comprimento_da_fuselagem_total * alt 
        
        area_molhada_horizontais = 2 * Comprimento_da_fuselagem_total * largura
        
        volume_molhado = (area_molhada_lados + area_molhada_horizontais) * 0.00015 #  0.00015 é a espessura da fita
        
        Peso_fita = 2 * volume_molhado * phi_fita
        
        CG_fita = CG_fus
        
        #peso total

        P_total = P_fixos + P_asa + P_cauda_h + P_cauda_v + P_fus + Peso_fita
        
        CG_vazio = ((5 * ((dist_nariz_a_asa)+mac*1/4)) + (CG_bateria*P_bateria) + (CG_helice*P_Helices) + (CG_motor*P_motor) + (CG_fios*P_fios) + (CG_servos*P_servos) + (CG_asa*P_asa) + (CG_h*P_cauda_h) + (CG_v*P_cauda_v) + (CG_fus*P_fus) + (Peso_fita*CG_fita) + (P_bequilha + CG_bequilha))/(P_total + 5)
        
        porc = round(100*(CG_vazio-dist_nariz_a_asa)/mac,2)
        
        df.iloc[i,22] = round(P_total,3)  
        
        df.iloc[i,25] = porc

    return(df)



def Carga_paga(df):
    
    for i in range(len(df)):
    
        P = df.iloc[i,22]
        
        MTOW = df.iloc[i,26]
        
        Carga_paga = MTOW - P
        
        df.iloc[i,27] = round(Carga_paga,3)
    
    return(df)


def estabilidade(df):
 
    pi = 3.1415
    
    d = 0.0850  #[m] largura da fuselagem eixo y 
    
    vEH = 0.4
    
    eta = 0.97
    
    for i in range(len(df)):

                
        b = df.iloc[i,2]    
        
        AR = df.iloc[i,3]

        mac = df.iloc[i,6]
        
        S = df.iloc[i,7]
        
        c = df.iloc[i,8]
        
        CLa = df.iloc[i,20]
        
        Xcg = df.iloc[i,25] * c/100
        
        cg = 0.4 + df.iloc[i,25] * c/100
        
        Xac = c/4
        
        ARh = (2/3)*(b/mac)  #aproximação de Sadraey
        
        if ARh < 3:
            ARh = 3      #recomendação
        
        bh = (b)/3           #aproximação
        
        Sh  = ((bh**2)/ARh)
        
        lh = (vEH*S*mac/Sh)              # [m]

        lb = cg + lh                    
        
        CLaEH = CLa/2                                                  # [1/grau] sustentação do EH
        
        dx1 = 0.0925                                                      # [m] comprimento da seção
        x1 = 0.14718                                                      # [m] comprimento da seção (medido do bordo de ataque)
        
        dx2 = 0.05468                                                     # [m] comprimento da seção
        x2 = 0.05468                                                      # [m] comprimento da seção (medido do bordo de ataque)
        
        dx3 = lb - 0.4 - c
        x3 = lb - 0.4 - c
        
        a2 = x1/c;
        a3 = x2/c;


        deu1 = 2.21-2.27*a2+1.59*a2**2-0.362*a2**3;
        deu2 = 5.13-8.6*a3+7.3*a3**2-2.09*a3**3;

        dep = 57.3*2*CLa/(pi*AR)

        deu3 = (x3/lb)*(1-dep)

        sa1 = d**2*deu1*dx1
        sa2 = d**2*deu2*dx2
        sa3 = d**2*deu3*dx3
        soma = sa1+sa2+sa3

        Cmaf = (1/(36.5*S*c))*soma

        PN = Xac-(Cmaf/CLa)+(vEH*eta*CLaEH/CLa)*(1-dep)
        ME = PN-Xcg
        
        if PN <= cg:
            nota_Estabilidade = (-156.25*ME**2 + 62.5*ME + 93.75)
        else:
            nota_Estabilidade = 0
        
        
        df.iloc[i,23] = round(nota_Estabilidade,1)
        
    return(df)


















