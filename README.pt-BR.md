# llm-learning

Projeto de estudo para construir um agente de código com chamadas de função usando Gemini.

Este repositório demonstra como um LLM pode:

- receber um prompt do usuário,
- decidir chamar ferramentas locais,
- executar operações de arquivo com segurança em um diretório restrito,
- e retornar uma resposta final.

O projeto inclui um app sandbox (`calculator/`) que o agente pode inspecionar, executar e modificar via tool calls.

## Versões de Idioma

- Inglês: `README.md`
- Português (Brasil): este arquivo (`README.pt-BR.md`)

## O Que Este Projeto Faz

Em tempo de execução, `main.py` envia o prompt para o Gemini com:

- um prompt de sistema (`promps.py`),
- um conjunto de declarações de ferramentas (`call_function.py`),
- e o histórico da conversa.

O Gemini pode solicitar uma ou mais chamadas de função. Cada chamada é executada localmente, o resultado volta para o Gemini, e o loop continua até o modelo retornar uma resposta final (ou atingir o limite de iterações).

As quatro ferramentas expostas ao modelo são:

1. `get_files_info`: lista arquivos de um diretório.
2. `get_file_content`: lê conteúdo de arquivo texto.
3. `write_file`: cria/sobrescreve arquivos.
4. `run_python_file`: executa um script Python.

## Modelo de Segurança

Todos os caminhos das ferramentas são restritos a um diretório de trabalho (`./calculator`) injetado em `call_function.py`.

A validação de caminhos é centralizada em `functions/path_validation.py`:

- caminhos são normalizados com `os.path.abspath(os.path.join(...))`,
- `os.path.commonpath` garante que o alvo está dentro da raiz permitida,
- acesso fora da raiz (por exemplo `../` ou `/bin`) é bloqueado.

Esse é o principal mecanismo de segurança para evitar directory traversal e acesso acidental a áreas arbitrárias do sistema de arquivos.

## Estrutura do Repositório

### Raiz

- `main.py`: app de CLI e loop do agente.
- `call_function.py`: registro e dispatcher de funções.
- `promps.py`: prompt de sistema usado pelo Gemini.
- `config.py`: constantes (`MAX_CHARACTERS`).
- `pyproject.toml`: metadados do projeto e dependências.
- `test_*.py`: scripts manuais de teste para cada ferramenta.

### Ferramentas (`functions/`)

- `functions/path_validation.py`: guarda reutilizável de segurança de caminho.
- `functions/get_files_info.py`: listagem de diretório com tamanho e flag de pasta.
- `functions/get_file_content.py`: leitura de arquivo com comportamento de truncamento.
- `functions/write_file.py`: escrita de arquivos texto, criando diretórios pai.
- `functions/run_python_file.py`: executa arquivos `.py` via subprocess e retorna stdout/stderr.

### App sandbox (`calculator/`)

- `calculator/main.py`: CLI de calculadora simples.
- `calculator/pkg/calculator.py`: avaliador de expressão infixa (`+ - * /`, precedência, parênteses).
- `calculator/pkg/render.py`: renderiza saída em JSON.
- `calculator/tests.py`: testes unitários do comportamento da calculadora.
- `calculator/lorem.txt`, `calculator/pkg/morelorem.txt`: arquivos de exemplo para escrita.

## Instalação

### 1. Requisitos

- Python 3.13+
- Chave de API do Gemini

### 2. Instalar dependências

Com `uv`:

```bash
uv sync
```

Ou com `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

### 3. Configurar variáveis de ambiente

Crie `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

## Uso

Uso básico:

```bash
python main.py "Liste os arquivos do diretório atual"
```

Modo verboso:

```bash
python main.py --verbose "Leia o main.py e explique"
```

### Fluxo ao executar

1. A CLI interpreta o prompt.
2. A mensagem é enviada ao Gemini com definição de ferramentas.
3. O Gemini pode solicitar chamadas de função.
4. A ferramenta local executa no escopo de `./calculator`.
5. O resultado da ferramenta é adicionado na conversa.
6. O loop repete até resposta final do modelo.

## Testes

Execute os scripts de teste das ferramentas:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_write_file.py
python test_run_python_file.py
```

### Comportamento observado atualmente

Os testes de ferramentas validam que caminhos bloqueados como `/bin`, `../` e `/tmp/temp.txt` são rejeitados.

`test_run_python_file.py` atualmente revela uma falha em um teste unitário da calculadora (`test_not_enough_operands`), porque a expressão `"+ 3"` levanta `IndexError` em vez do `ValueError` esperado.

## Observações e Limitações

- `get_file_content` atualmente lê os primeiros 1000 caracteres, enquanto a mensagem de truncamento menciona `MAX_CHARACTERS` (10000). Essa inconsistência é um bom candidato para refatoração futura.
- Nos módulos de ferramentas, o tratamento de exceção usa `return print(...)`, que retorna `None` após imprimir. Retornar strings de erro explícitas simplificaria o tratamento no chamador.
- O arquivo `promps.py` tem um typo no nome (`promps` vs `prompts`), mas funciona com o import atual.

## Objetivos de Aprendizado Cobertos

Este repositório é uma referência mínima útil para:

- fluxo de function calling com LLM,
- tooling de sistema de arquivos com segurança,
- execução de subprocesso com escopo restrito,
- loop iterativo de tool calls com estado de conversa,
- e exploração orientada a testes de casos de borda.
