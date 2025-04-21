from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from math import gcd
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

# f(x)=a^x mod N
# Simulação da multiplicação modular controlada por potências de a
def controlled_mul_mod15(a, power):
    U = QuantumCircuit(4)
    if a**power % 15 == 7:
        U.swap(2, 3)
        U.swap(1, 2)
        U.swap(0, 1)
    elif a**power % 15 == 4:
        U.swap(0, 2)
        U.swap(1, 3)
    elif a**power % 15 == 13:
        U.swap(0, 1)
        U.swap(1, 2)
        U.swap(2, 3)
    return U


# Transformada de Fourier Quântica Reversa
# QFT inversa
def qft_dagger(n):
    qc = QuantumCircuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / 2 ** (j - m), m, j)
        qc.h(j)
    return qc


# Parâmetros do problema
N = 15
a = 7
n_count = 4  # número de qubits para estimar o período

# Circuito de Shor
qc = QuantumCircuit(n_count + 4, n_count)

# Aplicar Hadamard aos qubits de contagem
for q in range(n_count):
    qc.h(q)

# Inicializa f(x) = 1 no registrador de 4 qubits
qc.x(n_count + 3)

# Aplica as operações controladas para cada qubit de contagem
for i in range(n_count):
    power = 2**i
    U = controlled_mul_mod15(a, power).to_gate()
    U.name = f"{a}^{power} mod {N}"
    controlled_U = U.control()
    qc.append(controlled_U, [i] + [j + n_count for j in range(4)])


# Aplica QFT inversa
qc.append(qft_dagger(n_count), range(n_count))

# Medição
qc.measure(range(n_count), range(n_count))

print(qc)

############# Quantum instance (simulação) ###########
# Simulação
sim = Aer.get_backend('aer_simulator')
compiled = transpile(qc, sim)
result = sim.run(compiled).result()
counts = result.get_counts()

# Visualiza o resultado
plot_histogram(counts)
plt.show()



#### Fatoração (extração dos fatores a partir do período) ####

# Pós-processamento do resultado
measured = max(counts, key=counts.get)
measured_val = int(measured, 2)
print(f"Medida (bin): {measured}, (dec): {measured_val}")

frac = Fraction(measured_val, 2**n_count).limit_denominator(N)
r = frac.denominator
print(f"Estimativa do período r: {r}")

# Tenta extrair os fatores
if r % 2 == 0:
    # Greatest Common Divisor / Máximo Divisor Comum (MDC)
    guess1 = gcd(pow(a, r//2) - 1, N)
    guess2 = gcd(pow(a, r//2) + 1, N)
    print(f"Fatores potenciais de {N}: {guess1}, {guess2}")
else:
    print("Período ímpar ou inválido, tente novamente.")
