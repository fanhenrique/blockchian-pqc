# Avaliação dos algoritmos pós-quânticos

## Instalação da liboqs e do liboqs-python

Conceder permissão ao arquivo de instalação.
```
chmod +x install.sh
```

Para instalar o liboqs e o liboqs-python.
```
./install.sh
```

>É recomendado que use a mesma versão da liboqs e liboqs-python.
>
>Confira as versões em [install.sh](./install.sh)


## Ambiente virtual
Antes de executar os algoritmos é precisos ativar o ambiente virtual.

Criar o ambiente virtual.
```
python -m venv venv
```

Ativar o ambiente virtual
```
source venv/bin/activate
```

Instale as dependências
```
pip install -r requirements.txt
```

Para desativar o ambiente virtual.
```
deactivate
```

## Exemplos

Antes de executar os algoritmos use o exemplos de teste da liboqs-python.

Exemplo de algoritmo de KEM.
```
python liboqs-python/examples/kem.py
```

Exemplo de algoritmo de assinatura digital.
```
python liboqs-python/examples/sig.py
```

## Execução

### Execução dos algoritmos KEM

Tempos dos algoritmos KEM.
```
python kem_performance.py <quantidade-de-execuções>
```

Tamanhos dos algoritmos KEM.
```
python kem_sizes.py
```

### Execução dos algoritmos de assinatura digital

Tempos dos algoritmos de assinatura digital.
```
python sig_performance.py <quantidade-de-execuções>
```

Tamanhos dos algoritmos assinatura digital.
```
python sig_sizes.py
```

## Geração dos gráficos

Gerar gráficos dos algoritmos KEM.
```
python kem_graphics.py
```

Gerar gráficos dos algoritmos assinatura digital.
```
python sig_graphics.py
```
