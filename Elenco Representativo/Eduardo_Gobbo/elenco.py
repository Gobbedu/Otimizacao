#!/bin/python

"""
Feito por 
    - Eduardo Gobbo Willi Vasconcellos Goncalves - GRR20203892
"""

import sys                  # argumentos na linha de comando 
import time                 # analisa tempo de execucao
from cmath import inf       # infinito (valor inicial de Opt, Minimizar)
fprintf = sys.stderr.write  # atalho para saida esperada

# globais: P, A, G, actors, groups 
# (P, actors, groups) in int 
# A in dict(int: list()) 
# G in set()

def main():
    """
    Bounding    (estima valor dos nodos em subarvore)
    Viabilidade (viavel sse [atores == persons && Unitorio de elenco contem G])
    Otimalidade (otimal sse [Solucao atual respeita restricoes do problema])
    """
    otimal, viavel = options()
    init()

    if(P > actors or not G.issubset(get_group(A))):     # mais personagens que atores
        print("Inviavel")                               # atores nao contem todos os grupos
        return -1;

    global OptEscolhas, OptPrice, Nnodos            # var globais
    OptEscolhas = []
    OptPrice = inf
    Nnodos = 0

    X = []
    start = time.time()                                  
    BranchEbound(X, 0, otimal, viavel)      
    end = time.time()
    
    # saida: resultado
    for i, x in enumerate(OptEscolhas, start=1):
        if x == 1:
            print(i, end = ' ')
    print(f"\n{OptPrice}")
    
    fprintf(f"foram visitados {Nnodos} nodos na arvore de busca\n")
    fprintf(f"A execucao da busca durou {(end-start) * 10**3} ms\n")

    return 0

    
def BranchEbound(X, nivel, Bound, Viavel):
    global OptEscolhas, OptPrice, Nnodos    # globais
    Nnodos += 1                             # numero de nodos visitados na arvore
    # print(f"ESCOLHAS X: {X}")

    if(Solucao_Viavel(X)):      
        custo = custo_elenco(get_elenco(X))
        if(custo < OptPrice):               
            OptPrice = custo
            OptEscolhas = X.copy()
        # print(f"CUSTO PARCIAL: {custo}, ELENCO: {get_elenco(X)}")
    
    
    # Cl : COMPUTA ESCOLHAS, BRANCH ou PODA Nodo 
    choice = [0, 1]
    if(not Viavel(X)):          # Poda por viabilidade
        choice.pop()

    if nivel == actors:         # base
        choice = []

    # print(f"NEXT CHOICES: {choice}")

    nextchoice = []
    nextbounds = []
    for a in choice:
        X.append(a)
        nextchoice.append(a)
        nextbounds.append(Bound(X)); X.pop()
        
    for i in range(len(nextchoice)):
        if(nextbounds[i]) >= OptPrice:
            return
        X.append(nextchoice[i])
        BranchEbound(X, nivel+1, Bound, Viavel); X.pop()
        
    
    return 0 # fim BranchEbound()


def viabilidade(X):
    return sum(X) < P     # viavel sse menos atores que personagens (for child node)

def Solucao_Viavel(X: list):
    Acts = get_elenco(X)
    grupos = set()
    for d in Acts:
        for c, g in d.items():
            grupos.update(g)    
    # possui um ator para cada personagem & representa todos os grupos
    return (sum(X) == P) and (G.issubset(grupos))


def meu_limitante(X: list):
    """Se falta serem cobertos n papeis,
    soma custo dos n atores mais baratos
    """
    custo = custo_elenco(get_elenco(X))     # elenco escolhido
    Sobra = A.copy()                        # todos os atores
    
    Escolhidos = get_elenco(X)
    Sobra = [ator for ator in Sobra if ator not in Escolhidos]

    falta = P - sum(X)                      # numero de papeis a serem cobertos
    orcamentos = get_costs(Sobra)           # custo dos atores que sobraram
    orcamentos.sort()                       # em ordem crescente
    
    estimado = sum(orcamentos[:falta])      # soma dos n atores mais baratos
    
    bound = custo + estimado                # custo atual + n atores mais baratos

    # print(f"bound of {Sobra} is {custo} + {estimado} == {bound}")
    return bound


def limitante_dada(X: list):
    custo = custo_elenco(get_elenco(X))     # elenco escolhido
    Sobra = A.copy()                        # todos os atores

    Escolhidos = get_elenco(X)
    Sobra = [ator for ator in Sobra if ator not in Escolhidos]

    mcost = min(get_costs(Sobra))           # custo minimo dos atores NAO no elenco
    falta = P - sum(X)                      # numero de papeis a serem cobertos
    bound = custo + falta*mcost

    # print(f"bound of {Sobra} is {custo}+({falta}*{mcost}) == {bound}")
    return bound


def options():
    # defaults
    viab = viabilidade
    otim = meu_limitante
    
    # verifica command line arguments
    argv = sys.argv[1:]
    for i in argv:
        if(i == "-o"):
            otim = disabled
        if(i == "-a"):
            otim = limitante_dada
        if(i == "-f"):
            viab = disabled

    return otim, viab

    # informe as opcoes escolhidas no terminal
    if(otim == limitante_dada):
        fprintf("HABILITANDO FUNCAO LIMITANTE DADA\n")
    elif(otim == meu_limitante):
        fprintf("HABILITANDO FUNCAO LIMITANTE PROPRIA\n")
    else:
        fprintf("DESABILITANDO CORTES POR OTIMALIDADE\n")

    if(viab == disabled):
        fprintf("DESABILITANDO CORTES POR VIABILIDADE\n")
    else:
        fprintf("HABILITANDO CORTES POR VIABILIDADE\n")

    return otim, viab
    

def init():
    # elenco = Elenco()
    global P, A, G, actors, groups
    A = []
    G = set()
    lmn = list(map(int,input().strip().split()))[:3] # uwu

    P = lmn.pop()    # numero de personagens
    actors  = lmn.pop()    # inicia tamanho conjunto de Atores
    groups  = lmn.pop()    # inicia tamanho conjunto de Grupos

    # inicializa grupos
    for i in range(1, groups+1):
        G.add(i)

    for j in range(1, actors+1):
        vs = list(map(int,input().strip().split()))[:2] # uwu

        g = []          # grupos do ator
        s = vs.pop()    # numero de grupos
        for k in range(s):
            g.append(int(input()))
            
        # Adiciona ator {custo: [grupos]}
        A.append({vs.pop(): g})        

    return 
    print(f"Grupos: {G}")
    print(f"Atores: {A}")
    print(f"Personagens: {P}")
    return


### =========== FUNCOES AUXILIARES ===========
def get_elenco(X: list):
    """Dada uma lista de opcoes X, 
    retorna atores indicados pelo valor booleano i em X
    """
    elenco = []
    for i in range(len(X)):
        if X[i]:
            elenco.append(A[i])
            
    return elenco

def custo_elenco(A: list):
    """Dado uma lista de Atores, 
    retorna custo total dos atores na lista
    """
    return sum(get_costs(A))

def get_costs(A: list):
    cost = []
    for d in A:
        for c, g in d.items():
            cost.append(c)
            
    return cost

def get_group(A: list):
    groups = set()
    for d in A:
        for c, g in d.items():
            groups.update(g)
            
    return groups


def disabled(X):
    return True

if __name__ == '__main__':
    main()
    