# Algoritmo de Shor

Dado um número inteiro $N$ composto (ou seja, não primo), para encontrar os dois inteiros $p$ e $q$ tal que $N = p * q$
    
## 1. Escolha de um número aleatório $a$

Escolha um número aleatório inteiro $a$, tal que:

$$
1 < a < N
$$

Se $a$ for um divisor de $N$, o primeiro fator foi encontrado.

Caso contrário, continue para o próximo passo.

Verifique se $a$ é coprimo de $N$

Se $mdc(a, N) \not= 1$, então encontramos o segundo fator de $N$. Fim do algoritmo.

>$mdc$: Máximo divisor comum
