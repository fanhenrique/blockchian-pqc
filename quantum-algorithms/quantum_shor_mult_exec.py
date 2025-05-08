from qiskit import transpile
from qiskit_aer import Aer
from math import gcd
from fractions import Fraction
import matplotlib.pyplot as plt
import os

from quantum_shor import controlled_modular_exponentiation, qft_dagger, create_shor_circuit

def extract_factors(counts, N, n_count, a):
    measured = max(counts, key=counts.get)
    measured_val = int(measured, 2)
    frac = Fraction(measured_val, 2 ** n_count).limit_denominator(N)
    r = frac.denominator
    if r % 2 == 0:
        p = gcd(pow(a, r // 2) - 1, N)
        q = gcd(pow(a, r // 2) + 1, N)
        if 1 < p < N or 1 < q < N:
            return (p, q)
    return None

def main():

    N = 15               # Número a ser fatorado
    a = 7                # Inteiro aleatório tal que gcd(a, N) = 1
    n_count = 4          # Número de qubits para contagem
    
    factor_counts = {}

    for _ in range(1000):

        # Construção do circuito
        qc = create_shor_circuit(a, N, n_count)
        # print(qc.draw("text"))

        # Simulação
        sim = Aer.get_backend('aer_simulator')
        compiled = transpile(qc, sim)
        result = sim.run(compiled).result()
        counts = result.get_counts()

        factors = extract_factors(counts, N, n_count, a)
        factor_counts[factors] = factor_counts.get(factors, 0) + 1

    # Converter as chaves em strings para exibição
    labels = [str(k) if k is not None else "None (inválido)" for k in factor_counts.keys()]
    values = list(factor_counts.values())

    os.makedirs('outs', exist_ok=True)

    # Criar o histograma
    plt.figure(figsize=(16, 9))
    plt.bar(labels, values)
    plt.xlabel('Resultados possíveis', fontsize=22)
    plt.ylabel('Quantidade', fontsize=22)
    plt.title('Histograma dos Resultados', fontsize=22)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('outs/histogram.png')
    # plt.show()

if __name__ == '__main__':
    main()
