import numpy as np
from math import gcd
import sys
import argparse

def is_coprime(a, N):
    """
    Verifica se os inteiros 'a' e 'N' são coprimos.

    Dois números são coprimos se o único divisor comum entre eles é 1.
    Retorna True se forem coprimos, False caso contrário.
    """
    return gcd(a, N) == 1

def get_random_coprime(N):
    """
    Gera e retorna um inteiro aleatório 'a' tal que 1 < a < N e 'a' é coprimo com N.
    """
    while True:
        a = np.random.randint(2, N)
        if is_coprime(a, N):
            return a

def get_period(a, N):
    """
    Busca o menor inteiro r tal que a^r ≡ 1 mod N.

    Esse r é chamado de ordem ou período de a módulo N.

    Usa pow(a, r, N), que é exponenciação modular eficiente: calcula a^r mod N.

    A período da função de um número a módulo N:

        f(x) = a^x mod N

    Esta é a parte quântica do algoritmo de Shor, responsável por encontrar o 
    período r de forma eficiente utilizando um computador quântico.

    Nesta versão clássica do algoritmo de Shor, a função realiza a tarefa usando uma busca linear.
    uma abordagem simples, porém ineficiente para números grandes devido ao seu alto custo computacional.
    """
    r = 1
    while pow(a, r, N) != 1:
        r +=1
    return r

def shor(a, N):
    """
    Etapas:
    1. Verifica se a e N são coprimos

    2. Calcula o período r da função f(x)=a^x mod N

    3. Verifica se r é par
    
    4. Usa r para tentar encontrar fatores não-triviais de N

    """
    # Se N for par o número 2 já é um dos fatores
    if N % 2 == 0:
        sys.exit("Caso trivial: número par, já tem fator 2")

    # Verifica se o a está no intervalo 1 < a < N
    if not (1 < a < N):
        print("'a' deve estar no intervalo 1 < a < N")
        return

    # Verifica se a é coprimo com N
    if not is_coprime(a, N):
        print(f"a={a} nao é coprimo de N={N}")
        return
    
    r = get_period(a, N)

    # Se r for ímpar, o algoritmo recomeça
    # O r precisa ser par para continuar
    if r % 2 != 0:
        print(f"O r={r} precisa ser par para continuar")
        return

    # Se r é par e a^r ≡ 1 (mod N), então:
    # a^(r/2) ≠ ±1 (mod N) (condição importante),
    # então (a^(r/2) - 1)(a^(r/2) + 1) ≡ 0 (mod N),
    # ou seja, algum desses termos compartilha fator com N.
    p = gcd(pow(a, r//2) - 1, N)
    q = gcd(pow(a, r//2) + 1, N)

    # Se não encontrou fator interessante, tenta de novo
    if p == 1 or p == N:
        print(f"p=1 ou p=N esses não são fatores interessantes")
        return

    return p, q

def main():

    parser = argparse.ArgumentParser(
        description="Classical Shor's Algorithm",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-n", help="Find the factors of N", required=True, type=int)
    parser.add_argument("-a", help="randomly choose a value of a", type=int)

    args = parser.parse_args()

    N = args.n

    if args.a:

        result = shor(args.a, N)

        if result:
            p, q = result
            print(f"{N} = {p} * {q}")
        else:
            print("Não foi possível encontrar fatores com os parâmetros fornecidos.")

    else:    
        while True:
            
            # Escolhe um a aleatório no intervalo 1 < a < N
            a = get_random_coprime(N)

            print(f"Tentando com a = {a}")

            result = shor(a, N)

            if result:
                p, q = result
                print(f"{N} = {p} * {q}")
                break
    
        
if __name__ == '__main__':
    main()