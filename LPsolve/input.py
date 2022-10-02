#!/bin/python3.9
    
# MUST USE STDIN & STDOUT
def main():
    """ Volume reservatorio: Vini, Vmin, Vmax
        Volume adicionado p/ cada mes: yn
        MWatt gerado por -1m3: k
        custo ambiental p/ variacao 1m3: ca
        
        Maxima geracao termoeletrica: Tmax
        custo termoeletrica: ct
        
        Demanda da cidade p/ cada mes: dn

    """
    # read number of months 
    num_month = int(input())
    # print(f'numero de meses: {num_month}')

    # read energy demands & volume increase 
    demanda     =   [float(d) for d in input().split(' ')]
    afluencia   =   [float(d) for d in input().split(' ')]

    # check
    if(len(demanda) + len(afluencia) != 2*num_month):
        print(f'ERROR: wrong number of parameters, expected data for {num_month} months ')
        return

    # read given hidroeletric constants
    constantesH  =   [float(c) for c in input().split(' ')]
    if(len(constantesH) != 4):   # check
        print(f'ERROR: wrong number of parameters, expected 4 but got {len(constantesH)} constants')
        return

    # read given termoeletric constants
    constantesT =   [float(c) for c in input().split(' ')]
    if(len(constantesT) != 2):  #check
        print(f'ERROR: wrong number of parameters, expected 2 but got {len(constantesT)} constants')
        return


    # custo ambiental por 1m3 turbinado 
    ca = float(input())

    # print(demanda, afluencia, constantesH, constantesT, ca)

    # distribute all variables
    vini        =   constantesH[0]      # volume inicial da hidreletrica
    vmin        =   constantesH[1]      # volume minimo da hidreletrica
    vmax        =   constantesH[2]      # volume maximo da hidreletrica
    Kgeracao    =   constantesH[3]      # (k) geracao de energia por metro cubico turbinado
    tmax        =   constantesT[0]      # geracao maxima da termoeletrica
    T_cost      =   constantesT[1]      # custo para geracao de energia termoeletrica
    H_cost      =   ca                  # custo ambiental da variacao de volume hidreletrico

    volume      =   list()      # volume final da hidreletrica no mes
    turbinado   =   list()      # volume usado para gerar energia
    gen_termo   =   list()      # energia termoeletrica gerada

    ## MODELAGEM ##

       
    # Sujeito A:
    sa   =   str()

    # Vi - Vi-1 = Ai - Bi -> A:incremento & B:decremento
    #|Vi - Vi-1|= Ai + Bi
    # sa
    # Vi - Vi-1 = Ai - Bi -> Vi = Ai + Vi-1 - Bi
    # Vi, Ai, Bi >= 0
    """
    yi : afluencia mes i
    di : demanda mes i
    Vi : volume total hidreletrica mes i
    Gi : geracao de energia termoeletrica mes i
    Ti : volume turbinado (energia) hidreletrica mes i
    Ai : incremento no volume total da hidreletrica 
    Bi : decremento no volume total da hidreletrica
    """
    # MES 1 (INICIO)
    sa += f'd1 <= {Kgeracao}*T1 + G1;\n'    # demanda mes i <= Geracao_hidro + Geracao_Termo
    sa += f'V1 = {vini} + y1 - T1;\n'       # Volume = inicial + afluente - turbinado
    sa += f'A1 = y1 - T1 + B1;\n'           # restricao sem modulo
    
    sa += f'y1 = {afluencia[0]};\n'         # yi afluencia mes i
    sa += f'd1 = {demanda[0]};\n'           # valor dado da demanda
    sa += f'V1 >= {vmin};\n'                # volume total hidro minimo mensal
    sa += f'V1 <= {vmax};\n'                # volume total hidro maximo mensal   
    sa += f'G1 <= {tmax};\n'                # geracao maxima termoeletrica
    sa += f'A1 >= 0;\n'
    sa += f'B1 >= 0;\n'
    sa += f'G1 >= 0;\n'                     # energia Termo gerada maior q 0
    sa += f'T1 >= 0;\n'                     # Volume turbinado maior q 0

    # MES [2..n]
    for i in range(2, num_month+1):             
        sa += f'd{i} <= {Kgeracao}*T{i} + G{i};\n'  # demanda mes i <= Geracao_hidro + gen_termo
        sa += f'V{i} = V{i-1} + y{i} - T{i};\n'     # Volume = mes passado + afluente - turbinado
        sa += f'A{i} = y{i} - T{i} + B{i};\n'       # restricao sem modulo

        sa += f'y{i} = {afluencia[i-1]};\n'         # yi afluencia mes i
        sa += f'd{i} = {demanda[i-1]};\n'           # valor dado da demanda
        sa += f'V{i} >= {vmin};\n'                  # volume total hidro minimo mensal
        sa += f'V{i} <= {vmax};\n'                  # volume total hidro maximo mensal   
        sa += f'G{i} <= {tmax};\n'                  # geracao maxima termoeletrica
        sa += f'A{i} >= 0;\n'
        sa += f'B{i} >= 0;\n'
        sa += f'G{i} >= 0;\n'                       # energia Termo gerada maior q 0
        sa += f'T{i} >= 0;\n'                       # Volume turbinado maior q 0



    # Funcao objetifo:
    fobj = "min: "
    for i in range(1, num_month+1):
        fobj += f'{T_cost}*G{i} + '                     # custo da geracao anual termo
        fobj += f'{H_cost}*A{i} + {H_cost}*B{i} + '     #cuso geracao anual hidro
    fobj = fobj[:-3]        # remove ultimo '_+_' 
    fobj += ';'             # fecha min f();


    print(fobj)
    print(sa)

if __name__ == '__main__':
    main()