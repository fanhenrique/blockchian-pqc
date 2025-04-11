# Avaliação dos algoritmos pós-quânticos

## Instalação da liboqs e do liboqs-python

```
./install.sh
```

>É recomendado que use a mesma versão da liboqs e liboqs-python
>
>Confira as versões em [install.sh](./install.sh)


## Execução

Antes de executar é precisos ativar o ambiente virtual

```
source ./venv/bin/activate
```

Tempos dos algoritmos KEM
```
python kem_performance.py <numero-de-execuções>
```

Tempos dos algoritmos de assinatura digital
```
python sig_performance.py <numero-de-execuções>
```

Tamanhos dos algoritmos KEM
```
python kem_sizes.py
```

Tamanhos dos algoritmos assinatura digital
```
python sig_sizes.py
```

## Geração dos gráficos

Gerar gráficos dos algoritmos KEM
```
python kem_graphics.py
```

Gerar gráficos dos algoritmos assinatura digital
```
python sig_graphics.py
```