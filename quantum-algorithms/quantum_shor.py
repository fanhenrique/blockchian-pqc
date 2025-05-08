from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from math import gcd
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt

def controlled_modular_exponentiation(a, x, N):
    """
    Simula uma operação controlada de multiplicação modular a^x mod N
    OBS: esta é uma representação didática, apenas para N=15
    """
    U = QuantumCircuit(4)
    for i in range(x):
        # Roda os registradores (apenas para simular uma transformação)
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
        # Inverte os bits (arbitrário)
        for q in range(4):
            U.x(q)

    U = U.to_gate()
    U.name = f"{a}^{x} mod {N}"
    return U.control()

def qft_dagger(n):
    """
    Retorna um circuito da QFT inversa (QFT†) sobre n qubits
    """
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2 ** (j - m)), m, j)
        qc.h(j)
    qc.name = "QFT Reversa"
    return qc

def create_shor_circuit(a, N, n_count):
    """
    Cria o circuito quântico para o algoritmo de Shor
    """
    qc = QuantumCircuit(n_count + 4, n_count)

    # Aplica Hadamard nos qubits de contagem
    for q in range(n_count):
        qc.h(q)

    # Inicializa o registrador como |1> (padrão usado na parte f(x))
    qc.x(n_count + 3)

    # Aplica as operações controladas de a^{2^i} mod N
    for i in range(n_count):
        qc.append(
            controlled_modular_exponentiation(a, 2 ** i, N),
            [i] + [j + n_count for j in range(4)]
        )

    # Aplica a QFT inversa
    qc.append(qft_dagger(n_count), range(n_count))

    # Mede os qubits de contagem
    qc.measure(range(n_count), range(n_count))

    return qc

def postprocess_results(counts, N, n_count, a):
    """
    Processa os resultados da medição para estimar o período r
    """
    measured = max(counts, key=counts.get)
    measured_val = int(measured, 2)
    print(f"Medida (bin): {measured}, (dec): {measured_val}")

    frac = Fraction(measured_val, 2 ** n_count).limit_denominator(N)
    r = frac.denominator
    # print(f"Fração estimada: {frac}")
    print(f"Período estimado r = {r}")

    if r % 2 == 0:
        p = gcd(pow(a, r // 2) - 1, N)
        q = gcd(pow(a, r // 2) + 1, N)
        print(f"Fatores de {N}: {p}, {q}")
    else:
        print("Período ímpar ou inválido, tente novamente.")

def main():

    N = 15               # Número a ser fatorado
    a = 7                # Inteiro aleatório tal que gcd(a, N) = 1
    n_count = 4          # Número de qubits para contagem
    
    # Construção do circuito
    qc = create_shor_circuit(a, N, n_count)
    print(qc.draw("text"))

    # Simulação
    sim = Aer.get_backend('aer_simulator')
    compiled = transpile(qc, sim)
    result = sim.run(compiled).result()
    counts = result.get_counts()

    # Visualiza o histograma de resultados
    plot_histogram(counts)
    plt.show()

    # Pós-processamento dos resultados
    postprocess_results(counts, N, n_count, a)

if __name__ == '__main__':
    main()
