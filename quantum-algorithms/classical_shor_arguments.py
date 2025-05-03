import numpy as np
from math import gcd
import sys
import argparse

def is_coprime(a, N):
    """
    Verifica se `a` e `N` são coprimos, ou seja, se o máximo divisor comum 
    (greatest common divisor - gcd) entre eles é igual a 1.

    Dois números são considerados coprimos quando não compartilham nenhum divisor
    além de 1. Caso contrário, significa que já possuem um divisor comum,
    que pode ser um fator de `N`.
    """
    return gcd(a, N) == 1

def get_random_coprime(N):
    """
    Gera e retorna um inteiro aleatório `a` tal que `1 < a < N` e `a` é coprimo com `N`.
    """
    while True:
        a = np.random.randint(2, N)
        if is_coprime(a, N):
            return a

def get_period(a, N):
    """
    Calcula o período (ou ordem) `r` da função:

        f(x) = a^x mod N

    Ou seja, encontra o menor inteiro positivo `r` tal que:

        a^r ≡ 1 mod N

    No algoritmo de Shor quântico, o período `r` é encontrado de forma eficiente
    por meio da Transformada de Fourier Quântica (Quantum Fourier Transform - QFT).
    Nesta versão clássica, o cálculo é feito por busca linear, uma abordagem simples,
    porém ineficiente para números grandes devido ao seu alto custo computacional.

    Observação:
        As expressões `(a ** r) % N` e `pow(a, r, N)` produzem o mesmo resultado,
        ou seja, ambas realizam a exponenciação modular. No entanto, `pow(a, r, N)`
        é mais eficiente, pois evita calcular diretamente `a ** r`, o que pode gerar
        números intermediários muito grandes.
    """
    r = 1
    while pow(a, r, N) != 1:
        r +=1
    return r

def shor_algorithm(a, N):
    """
    Executa a versão clássica (não quântica) do algoritmo de Shor para fatorar um número composto `N`.

    O algoritmo segue os seguintes passos:

    1. Escolhe aleatoriamente uma base `a` tal que `gcd(a, N) = 1`, ou seja, `a` e `N` devem ser coprimos.
    2. Calcula o período `r` da função modular `f(x) = a^x mod N`.
    3. Verifica se `r` é par e se `a^(r/2) ≠ -1 mod N`.
    4. Calcula `gcd(a^(r/2) ± 1, N)` para tentar obter fatores não triviais de `N`.

    Retorna:
        tuple[int, int] | None: Uma tupla `(p, q)` com os fatores de `N`, ou `None` se não forem encontrados.
    """

    # Se `N` for par o número 2 já é um dos fatores
    if N % 2 == 0:
        sys.exit("Caso trivial: número par, já tem fator 2")

    print(f"\nTentando com a={a}")

    # Verifica se `a ∈ [2, N-1]`
    if not (1 < a < N):
        print("'a' deve estar no intervalo 1 < a < N")
        return

    # Verifica se `a` não é coprimo com `N`
    if not is_coprime(a, N):
        print(f"N={N} e a={a} não são coprimos")
        return
    else:
        print(f"N={N} e a={a} são coprimos")
    
    # Calcula o período `r` da função `f(x) = a^x mod N`
    # (ou seja, o menor `r` tal que `a^r ≡ 1 mod N`)
    r = get_period(a, N)

    print(f"Período r={r}")

    # Se `r` for ímpar, reinicia o processo
    if r % 2 != 0:
        print(f"r={r} é ímpar; reiniciando com outro valor de 'a'")
        return

    # Se `a^(r/2) ≡ -1 mod N`, fatores encontrados seriam triviais
    # `-1 mod N = N - 1`
    if pow(a, r // 2, N) == (N - 1):
        print("Condição inválida a^(r/2) ≡ -1 mod N")
        return

    # `(a^(r/2) - 1)(a^(r/2) + 1) ≡ 0 (mod N)`,
    # portanto, algum desses termos pode compartilhar um fator com `N`
    x = pow(a, r // 2, N)
    p = gcd(x - 1, N)
    q = gcd(x + 1, N)
    
    # Verificação pós-cálculo se os fatores são úteis
    if p in [1, N] and q in [1, N]:
        print(f"p={p}, q={q} - ambos são fatores triviais")
        return

    return p, q


def try_shor(a, N):
    """
    Tenta fatorar `N` usando a base `a` no contexto do algoritmo clássico de Shor.

    Se for bem-sucedido, exibe os fatores encontrados. Caso contrário, informa a falha.

    Retorna:
        bool: `True` se a fatoração foi bem-sucedida, `False` caso contrário.
    """

    factors = shor_algorithm(a, N)
    
    if factors:
        print(f"\nFatores de {N}: {factors}")
        return True

    return False

def main():

    parser = argparse.ArgumentParser(
        description="Classical Shor's Algorithm",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("-n", help="Find the factors of N", required=True, type=int)
    parser.add_argument("-a", help="Choose a value of a", type=int)

    args = parser.parse_args()

    N = args.n

    if N <= 2:
        sys.exit("Erro: N deve ser maior que 2")

    if args.a:
        success = try_shor(args.a, N)
        if not success:
            print("Não foi possível encontrar fatores com os parâmetros fornecidos.")
        
    else:   
        # Escolhe um `a` aleatório no intervalo `1 < a < N` 
        while not try_shor(get_random_coprime(N), N):
            continue
    
        
if __name__ == '__main__':
    main()
