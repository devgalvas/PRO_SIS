
# 🧠 Interpretador da Linguagem PRO-SIS

## 📖 Sobre o Projeto

O **PRO-SIS** é um interpretador para uma linguagem de programação de domínio específico, projetada para simplificar a **manipulação e representação de sistemas de equações lineares**.

Este projeto foi desenvolvido como aplicação prática dos conceitos da disciplina de **Compiladores**, com o objetivo de oferecer uma ferramenta intuitiva para modelar e resolver problemas matemáticos complexos de forma direta e eficiente.

Este repositório contém o **código-fonte completo do analisador léxico, sintático e do interpretador semântico** da linguagem.

---

## ✨ Funcionalidades

- ✅ **Sintaxe Declarativa**: Limpa e focada na descrição de variáveis e sistemas de equações.
- 🔢 **Tipos de Dados Dedicados**: Suporte a `inteiro`, `real` e `termo` para melhor organização.
- 🌳 **Análise de Código Robusta**: Usa **Lark** para gerar a Árvore Sintática Abstrata (AST).
- 🧩 **Estrutura Extensível**: Baseada no padrão `Transformer`, facilitando expansões futuras.
- 💻 **Interface de Linha de Comando**: Execute arquivos `.psis` diretamente pelo terminal.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**: Linguagem principal do projeto.
- **Lark**: Biblioteca moderna de parsing usada para análise léxica e sintática.

---

## 🚀 Começando

### 📋 Pré-requisitos

- Python 3.8 ou superior.  
Verifique com:
```bash
python3 --version
```

### 📦 Instalação

Clone o repositório e acesse a pasta:

```bash
git clone <URL_DO_REPOSITORIO>
cd pro-sis-interpreter
```

Instale a dependência:

```bash
pip install lark
```

---

## 💻 Como Usar

Crie um arquivo `.psis`, por exemplo `exemplo.psis`:

```psis
programa meu_primeiro_sistema {
    declare inteiro a, real b, termo x, termo y;

    sistema {
        2 * x + 3 * y = 10,
        x - 5 * y = 2
    }
}
```

Execute o interpretador:

```bash
python3 pro_sis_interpreter.py exemplo.psis
```

### ✅ Saída Esperada

```
Iniciando a compilação do arquivo 'exemplo.psis'...
------- Árvore Sintática Gerada (Final) --------
programa
  meu_primeiro_sistema
  declaracao_lista
    declaracao
      inteiro
      a
    declaracao
      real
      b
    declaracao
      termo
      x
    declaracao
      termo
      y
  sistema
    equacao
      ...
----------------------------------------
 ---- Variáveis Declaradas ---- 
 Nome: a, Tipo: inteiro
 Nome: b, Tipo: real
 Nome: x, Tipo: termo
 Nome: y, Tipo: termo
----------------------------------------

Programa: meu_primeiro_sistema
-=-=-=- Executando o sistema de equações -=-=-=-

 Programa analisado com sucesso!
```

---

## 📂 Estrutura do Projeto

```
.
├── pro_sis_interpreter.py      # Interpretador e compilador principal
├── pro_sis_gramatica.lark      # Definição da gramática da linguagem PRO-SIS
├── exemplo.psis                # Exemplo de código PRO-SIS
└── README.md                   # Este arquivo
```

---

## 🏛️ Arquitetura e Funcionamento

O processo de interpretação acontece em 3 etapas principais:

1. **Gramática** (`pro_sis_gramatica.lark`)  
   Regras da linguagem no formato EBNF, interpretadas pela Lark.

2. **Parsing** (`ProSisCompiler`)  
   Inicializa o parser, valida a sintaxe e gera a AST.

3. **Interpretação** (`ProSisInterpreter`)  
   A AST é percorrida por uma classe `Transformer`, com métodos dedicados para cada regra gramatical.

---

## 🗺️ Próximos Passos (Roadmap)

- [ ] 💡 Implementar operações matemáticas (`termo`, `expr`, `fator`)
- [ ] 🔧 Resolver sistemas de equações com **NumPy**
- [ ] 🧠 Implementar funções como `solve`, `det`, `inv`, `trans`
- [ ] 🐛 Melhorar tratamento de erros com linha e coluna
- [ ] ➕ Adicionar suporte aos tipos `eq` e `sis`

---

## ⚖️ Licença

Este projeto está licenciado sob os termos da [MIT License](./LICENSE).

---

## 👥 Autores

Este projeto foi desenvolvido por:

- **Eduardo Henrique de Sordi Rigamonti**  
- **Gabriel Fazion dos Santos**  
- **Lucas Galvão Freitas**  
- **Thiago de Oliveira Sousa Júnior**

Trabalho apresentado para a disciplina de **Compiladores** na **Universidade Federal de Itajubá (UNIFEI)**.

---

> 🌟 *Se este projeto te ajudou, não esqueça de deixar uma estrela no repositório!* ⭐
