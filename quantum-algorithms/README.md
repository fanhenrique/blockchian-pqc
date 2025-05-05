# Algoritmo de Shor Clássico

Esse é uma implementação clássica do algoritmo de Shor, em Python. 

Ele encontra fatores de um número composto $N$, desde que você forneça um número $a$ tal que $1 < a < N$ e a seja coprimo com $N$.

Etapas do algoritmo de Shor clássico

| Etapa | Parte    | Descrição                                                                                   |
|-------|----------|---------------------------------------------------------------------------------------------|
| 1     | Clássica | Escolher $a$ aleatoriamente, tal que $gcd(a, N) = 1$, ou seja, $a$ e $N$ devem ser coprimos |
| 2     | Clássica | Encontrar o período $r$ de $f(x) = a^x \mod N$ por busca linear                             |
| 3     | Clássica | Verificar se $r$ é par e $a^{r/2} \not\equiv -1 \mod N $                                    |
| 4     | Clássica | Calcular $mdc(a^{r/2} \pm 1, N)$ para obter os fatores                                      |


## Como executar

```bash
python shor.py -n <N> [-a <a>]
```

Para informações de como usar utilize o `--help`

```bash
python classical_shor.py --help
```

# Algoritmo de Shor

## Ideia principal

O algoritmo de Shor transforma o problema da fatoração em um problema de encontrar o período de uma função, e usa um computador quântico para achar esse período de forma eficiente.

Dado um número inteiro $N$ composto (ou seja, não primo), para encontrar os dois inteiros $p$ e $q$ tal que $N = p * q$

Etapas do algoritmo de Shor quântico

| Etapa | Parte    | Descrição                                                                                   |
|-------|----------|---------------------------------------------------------------------------------------------|
| 1     | Clássica | Escolher $a$ aleatoriamente, tal que $gcd(a, N) = 1$, ou seja, $a$ e $N$ devem ser coprimos |
| 2     | Quântica | Encontrar o período $r$ de $f(x) = a^x \mod N$ usando QFT Inversa                           |
| 3     | Clássica | Verificar se $r$ é par e $a^{r/2} \not\equiv -1 \mod N $                                    |
| 4     | Clássica | Calcular $mdc(a^{r/2} \pm 1, N)$ para obter os fatores                                      |

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

Use a computação quântica para encontrar o menor inteiro positivo $r$ tal que:

$$
a^r \mod N = 1
$$

$r$ chamado de período da função $f(x) = a^x \mod N$.

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