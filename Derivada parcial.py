import pandas as pd
import math


#--- CALCULANDO VARIACÃO DAS CARGA NO ELETROSCÓPIO 
#QUANDO SUBMETIDO A DIFERENTES ÂNGULOS DE ABERTURA

#----------Conceitos matemáticos/ estatísticos utilizados: 

#Derivação de uma função de múltiplas variaveis (Método: Derivadas Parciais)

#Desvio padrão médio, Propagação de erros

lista_angulos = [38,38,39,41,37,41,39,35,38,39]
lista_incerteza = [1,2,2,1,1,1,2,1,2,2]

lista_cargas = []
lista_result_inc = []
for i, x in enumerate(lista_angulos):    
    angulo = x/2

    ince_angulo = math.radians((lista_incerteza[i]/2))

    tag = math.tan(math.radians(angulo))
    sen = math.sin(math.radians(angulo))
    cos = math.cos(math.radians(angulo))

    distancia = 6.7e-02
    ince_dist = 1e-3

    massa = 7.5e-05

    ince_massa = 1e-6

    grav = 9.8

    const = 9e9
    
    #--------------VALOR CARGA------------------
    num = (distancia**2)*massa*(sen**2)*tag*grav
    q = math.sqrt(num/const)
    lista_cargas.append(q)


    #-------------derivada parcial theta-------------------


    reco = math.sqrt(grav*const*massa*cos*sen)

    a = 2*distancia*reco*sen*(cos**2)

    b = (distancia**2)*reco*sen

    c = 2*const*(cos**2)*abs(distancia)*abs(sen)


    dv_theta = (a+b)/c

    #------------------------------------

    #-------------derivada parcial distancia-------------------

    d = distancia*grav*massa*(math.sqrt(cos*const))*(sen**3)

    e = abs(sen)*abs(distancia)*(math.sqrt(grav*massa*sen))*cos* const

    dv_dista = d/e


    #-------------derivada parcial massa-------------------

    f = (distancia**2)*reco*(sen**2)

    g = 2*const*cos*(abs(distancia))*(abs(sen))

    dv_massa = f/g 


    #---------PROPAGACAO ERRO -----


    t_massa = (dv_massa*ince_massa)**2

    t_distancia = (dv_dista*ince_dist)**2

    t_theta = (dv_theta*ince_angulo)**2

    ince_carga = math.sqrt((t_massa+ t_distancia + t_theta))

    lista_result_inc.append(ince_carga)

#dataframe com resultados

resultados = pd.DataFrame(list(zip(lista_angulos, lista_cargas, lista_result_inc)),
               columns =["Angulo", 'Carga', 'Incerteza'])
print(resultados)


#----------------------D E S V I O  P A D R A O  M E D I O ----------------------

def DesvioPadraoMedio(lista, medio):
    n = 0
    for x in lista:
        diferenca = (x - medio)**2
        n = n + diferenca
    
    media = n/(len(lista)-1)
    final = math.sqrt(media)
    return final


#calculando valor medio angulo

valor_angulo = sum(lista_angulos)/len(lista_angulos)

incerteza_angulo_medio = DesvioPadraoMedio(lista_angulos,valor_angulo)

#calculando valor medio carga

valor_carga = sum(lista_cargas)/ len(lista_cargas)

incerteza_carga_media = DesvioPadraoMedio(lista_cargas,valor_carga)

#criando df com resultados

dic = {"Angulo":[ valor_angulo, incerteza_angulo_medio], "Carga":[valor_carga,incerteza_carga_media  ]}
df_medio = pd.DataFrame(dic)