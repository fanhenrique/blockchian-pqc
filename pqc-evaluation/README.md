# Avaliação dos algoritmos pós-quânticos

## Instalação da `liboqs` e do `liboqs-python`

Conceda permissão de execução ao arquivo de instalação usando o comando
```bash
chmod +x install.sh
```

Execute o comando abaixo para instalar o `liboqs` e o `liboqs-python`.
```bash
./install.sh
```

>Recomenda-se utilizar a mesma versão do `liboqs` e do `liboqs-python`. Por padrão, estamos utilizando a versão `0.12.0`, definida nas variáveis no início do arquivo [install.sh](./install.sh).

## Ambiente virtual

Antes de executar os algoritmos, é preciso ativar o ambiente virtual.

Ativar o ambiente virtual.
```bash
source venv/bin/activate
```

Desativar o ambiente virtual.
```bash
deactivate
```

## Exemplos

Execute os exemplos de teste da `liboqs-python` para verificar se o `liboqs` e o `liboqs-python` estão funcionando corretamente.

Exemplo de algoritmo de KEM.
```bash
python liboqs-python/examples/kem.py
```

Exemplo de algoritmo de assinatura digital.
```bash
python liboqs-python/examples/sig.py
```

## Execução

Consulte os argumentos disponíveis utilizando a opção `--help`.

```bash
python main.py --help
```

### Lista de variantes dos algoritmos pós-quânticos

#### Lista de variantes dos algoritmos KEM

```bash
python main.py --list-kem --levels <levels_list>
```

#### Lista de variantes dos algoritmos de assinatura digital

```bash
python main.py --list-sig --levels <levels_list>
```

### Execução dos algoritmos de assinatura digital

```bash
python main.py --sig ecdsa mldsa sphincs-shake-f falcon --runs <number_of_executions> --warp-up <number_of_executions> --levels <levels_list>
```

### Execução dos algoritmos KEM

```bash
python main.py --kem bike mlkem hqc mceliece-f --runs <number_of_executions> --warp-up <number_of_executions> --levels <levels_list>
```
