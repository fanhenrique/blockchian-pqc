# Algoritmo de Shor

Dado um número inteiro $N$ composto (ou seja, não primo), para encontrar os dois inteiros $p$ e $q$ tal que $N = p * q$

Etapas do algoritmo de Shor

| Etapa | Parte    | Descrição                                                        |
|-------|----------|------------------------------------------------------------------|
| 1     | Clássica | Escolher $a$ aleatoriamente e verificar $mdc(a, N)$              |
| 2     | Quântica | Encontrar o período $r$ de $f(x) = a^x \mod N$ usando QFT        |
| 3     | Clássica | Verificar se $r$ é útil (par, e $a^{r/2} \not\equiv -1 \mod N $) |
| 4     | Clássica | Calcular $mdc(a^{r/2} \pm 1, N)$ para obter os fatores           |

## 1. Escolha de um número aleatório $a$

Escolha um número aleatório inteiro $a$, tal que:

$$
1 < a < N
$$

Se $a$ for um divisor de $N$, o primeiro fator de $N$ foi encontrado.

Caso contrário, verifique se $a$ é coprimo de $N$. Se $mdc(a, N) \not= 1$, então o primeiro fator de $N$ foi encontrado. Fim do algoritmo.

>$mdc$: Máximo divisor comum

>Se você encontrou um fator $p$ de $N$ tal que $1<p<N$, então o segundo fator $q$ é simplesmente:
>
>$$
>q = N/p
>$$

## 2. Encontrar o período $r$.

## 3. Testar o valor de $r$

Depois de obter $r$, verifique:

* Se $r$ for ímpar -> Tente novamente com outro $a$.

* Se $a^{r/2} \equiv -1 \mod N$ -> Também tente novamente com outro $a$.


## 4. Encontrar os fatores

Se o $r$ encontrado for par e $a^{r/2} \equiv -1 \mod N$, então os fatores de $N$ são dados por:

$$
p = mdc(a^{r/2}-1, N) \quad \text{e} \quad  q = mdc(a^{r/2}+1, N)
$$

Esses são fatores não triviais de $N$. A função $mdc$ pode ser calculada eficientemente com o algoritmo de Euclides.