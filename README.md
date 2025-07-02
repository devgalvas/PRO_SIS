# 🧮 Interpretador PRO-SIS

**Uma linguagem de domínio específico para manipulação de sistemas de equações lineares**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Lark](https://img.shields.io/badge/Parser-Lark-green.svg)](https://lark-parser.readthedocs.io/)
[![NumPy](https://img.shields.io/badge/Math-NumPy-orange.svg)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/Science-SciPy-red.svg)](https://scipy.org/)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Sintaxe da Linguagem](#-sintaxe-da-linguagem)
- [Exemplos](#-exemplos)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Arquitetura](#-arquitetura)
- [Funções Matemáticas](#-funções-matemáticas)
- [Contribuição](#-contribuição)
- [Autores](#-autores)

---

## 🎯 Sobre o Projeto

O **PRO-SIS** é um interpretador para uma linguagem de programação de domínio específico (DSL) desenvolvida especificamente para simplificar a manipulação, representação e resolução de sistemas de equações lineares. 

Este projeto foi desenvolvido como trabalho prático da disciplina de **Compiladores** na **Universidade Federal de Itajubá (UNIFEI)**, aplicando conceitos fundamentais de:

- ✅ **Análise Léxica** - Reconhecimento de tokens
- ✅ **Análise Sintática** - Construção de árvores sintáticas
- ✅ **Análise Semântica** - Interpretação e execução
- ✅ **Verificação de Tipos** - Sistema de tipos robusto

---

## ✨ Características

### 🔤 **Sintaxe Declarativa e Intuitiva**
- Declaração clara de variáveis com tipos específicos
- Sintaxe focada em problemas matemáticos
- Estruturas dedicadas para sistemas de equações

### 🎯 **Tipos de Dados Especializados**
- `int` - Números inteiros
- `float` - Números reais 
- `eq` - Equações/vetores unidimensionais
- `sis` - Sistemas de equações/matrizes bidimensionais

### 🧮 **Operações Matemáticas Avançadas**
- **Álgebra Linear**: inversão, transposição, determinante
- **Decomposição**: LU (P, L, U), diagonal
- **Resolução**: sistemas lineares automaticamente

### 🔍 **Análise Robusta**
- Parser baseado em **Lark** com gramática EBNF
- Detecção de erros léxicos, sintáticos e semânticos
- Geração de árvore sintática abstrata (AST)
- Verificação de compatibilidade de tipos

### 📊 **Saída Detalhada**
- Análise léxica completa com tokens
- Visualização da árvore sintática
- Logs de execução passo-a-passo

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+** ([Download](https://python.org))
- **pip** (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <https://github.com/devgalvas/PRO_SIS.git>
   cd compiladores/PRO_SIS
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
   
   Ou manualmente:
   ```bash
   pip install lark numpy scipy
   ```

3. **Verifique a instalação**
   ```bash
   python classes/pro_sis_interpreter.py --help
   ```

---

## 💻 Como Usar

### Execução Básica

```bash
python classes/pro_sis_interpreter.py <arquivo.psis>
```

### Exemplo Prático

1. **Crie um arquivo `exemplo.psis`:**
   ```pro-sis
   int x = 10
   
   eq vetor = [1, 2, 3]
   
   sis matriz = {[2, 1, 7], [1, -1, 1]}
   
   solve matriz end
   det matriz end
   ```

2. **Execute:**
   ```bash
   python classes/pro_sis_interpreter.py exemplo.psis
   ```

3. **Resultado:**
   ```
   Iniciando a compilação do arquivo 'exemplo.psis'...
   ------- Árvore Sintática Gerada --------
   [Árvore sintática detalhada]
   ----------------------------------------
   
   ------- Análise Léxica (Tokens Reconhecidos) --------
   [Lista de tokens reconhecidos]
   ---------------------------------------------------
   
   -> Variável 'x' (tipo: int) declarada e inicializada.
   -> Variável 'vetor' (tipo: eq) declarada e inicializada.
   -> Variável 'matriz' (tipo: sis) declarada e inicializada.
   
   -=-=- Executando 'solve' no sistema 'matriz' -=-=-
   [Resultado da resolução]
   
   -=-=- Executando 'det' no sistema 'matriz' -=-=-
   [Valor do determinante]
   
   Programa executado com sucesso!
   ```

---

## 📝 Sintaxe da Linguagem

### Declaração de Variáveis
```pro-sis
tipo nome = valor
```

### Tipos Suportados
| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `int` | Números inteiros | `int x = 42` |
| `float` | Números reais | `float pi = 3.14` |
| `eq` | Vetores/Equações | `eq v = [1, 2, 3]` |
| `sis` | Matrizes/Sistemas | `sis m = {[1,2], [3,4]}` |

### Comandos de Função
```pro-sis
funcao variavel end
```

### Estruturas de Dados

**Equações (vetores):**
```pro-sis
eq nome = [elemento1, elemento2, elemento3]
```

**Sistemas (matrizes):**
```pro-sis
sis nome = {[linha1_col1, linha1_col2], [linha2_col1, linha2_col2]}
```

---

## 🧮 Funções Matemáticas

| Função | Descrição | Entrada | Saída |
|--------|-----------|---------|-------|
| `solve` | Resolve sistema linear | `sis` | Exibe solução |
| `det` | Calcula determinante | `sis` | Exibe determinante |
| `inv` | Matriz inversa | `sis` | `sis` (matriz inversa) |
| `trans` | Transposta | `sis` | `sis` (matriz transposta) |
| `retP` | Matriz P (LU) | `sis` | `sis` (matriz P) |
| `retL` | Matriz L (LU) | `sis` | `sis` (matriz L) |
| `retU` | Matriz U (LU) | `sis` | `sis` (matriz U) |
| `retD` | Matriz diagonal | `sis` | `sis` (matriz diagonal) |

---

## 📁 Estrutura do Projeto

```
PRO_SIS/
├── 📄 requirements.txt          # Dependências do projeto
├── 📁 classes/                  # Código fonte principal
│   ├── 🐍 pro_sis_interpreter.py   # Interpretador principal
│   ├── 📋 pro_sis_grammar.lark     # Gramática da linguagem
│   ├── 📝 test.psis                # Arquivo de teste
│   ├── 📝 test_final.psis          # Teste final
│   └── 📄 test_final.txt           # Saída da análise léxica
└── 📖 README.md                 # Este arquivo
```

---

## 🏗️ Arquitetura

O interpretador PRO-SIS segue uma arquitetura clássica de compilador em três fases:

### 1. 🔍 **Análise Léxica** (`ProSisLexer`)
- Quebra o código fonte em tokens
- Identifica palavras-chave, operadores, números e identificadores
- Gera arquivo `.txt` com todos os tokens reconhecidos

### 2. 🌳 **Análise Sintática** (`Lark Parser`)
- Usa gramática EBNF definida em `pro_sis_grammar.lark`
- Constrói árvore sintática abstrata (AST)
- Valida a estrutura sintática do programa

### 3. ⚡ **Análise Semântica** (`ProSisInterpreter`)
- Herda de `lark.Transformer`
- Percorre a AST e executa ações semânticas
- Gerencia tabela de símbolos e verificação de tipos
- Executa operações matemáticas usando NumPy/SciPy

### 4. 🎯 **Coordenação** (`ProSisCompiler`)
- Integra todas as fases
- Gerencia fluxo de execução
- Trata erros e exceções

---

## 🧪 Exemplos

### Exemplo 1: Declarações Básicas
```pro-sis
int idade = 25
float altura = 1.75
eq coordenadas = [10, 20, 30]
```

### Exemplo 2: Sistema de Equações 2x2
```pro-sis
sis sistema = {[2, 1, 8], [1, -1, 1]}
solve sistema end
det sistema end
```

### Exemplo 3: Operações com Matrizes
```pro-sis
sis matriz = {[1, 2], [3, 4]}
sis transposta = trans(matriz)
sis inversa = inv(matriz)
float determinante = det(matriz)
```

### Exemplo 4: Decomposição LU
```pro-sis
sis A = {[4, 3, 2], [3, 4, 1], [2, 1, 4]}
sis P = retP(A)
sis L = retL(A)
sis U = retU(A)
```

---

## 🛠️ Detalhes Técnicos

### Dependências
- **lark**: Parser moderno e eficiente
- **numpy**: Operações com arrays e álgebra linear
- **scipy**: Funções científicas avançadas (decomposição LU)

### Tratamento de Erros
- **Erros Léxicos**: Tokens não reconhecidos
- **Erros Sintáticos**: Estrutura inválida
- **Erros Semânticos**: Tipos incompatíveis, variáveis não definidas
- **Erros Matemáticos**: Matrizes singulares, dimensões incompatíveis

### Verificação de Tipos
O interpretador possui um sistema robusto de verificação de tipos:
- Conversão automática `float` → `int` quando possível
- Validação de compatibilidade em atribuições
- Verificação de tipos em chamadas de função


---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autores

**Trabalho acadêmico desenvolvido para a disciplina de Compiladores**  
**Universidade Federal de Itajubá (UNIFEI)**

- **Eduardo Henrique de Sordi Rigamonti**
- **Gabriel Fazion dos Santos** 
- **Lucas Galvão Freitas**
- **Thiago de Oliveira Sousa Júnior**

---

## 📞 Contato

Para dúvidas, sugestões ou colaborações:

- 📧 Email: [ d2023001147@unifei.edu.br, d2023005351@unifei.edu.br, d2022014991@unifei.edu.br, 2023008774@unifei.edu.br]
- 🎓 Instituição: UNIFEI - Universidade Federal de Itajubá
- 📚 Disciplina: Compiladores

---

