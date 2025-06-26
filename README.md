Interpretador da Linguagem PRO-SIS
📖 Sobre o Projeto
O PRO-SIS é um interpretador para uma linguagem de programação de domínio específico, projetada para simplificar a manipulação e representação de sistemas de equações lineares. Este projeto foi desenvolvido como aplicação prática dos conceitos da disciplina de Compiladores, com o objetivo de oferecer uma ferramenta intuitiva para modelar e resolver problemas matemáticos complexos de forma mais direta e eficiente.

Este repositório contém o código-fonte completo do analisador léxico, sintático e do interpretador semântico da linguagem.

✨ Funcionalidades
Sintaxe Declarativa: Uma sintaxe limpa e focada na descrição de variáveis e sistemas de equações.

Tipos de Dados Dedicados: Suporte para tipos como inteiro, real e termo, facilitando a organização das equações.

Análise de Código Robusta: Utiliza a biblioteca Lark para uma análise sintática poderosa e de fácil manutenção, gerando uma Árvore Sintática Abstrata (AST) para a interpretação.

Estrutura Extensível: O interpretador foi construído com base no padrão Transformer, permitindo a fácil adição de novas funcionalidades e operações matemáticas.

Interface de Linha de Comando: Permite executar ficheiros de código .psis diretamente do terminal.

🛠️ Tecnologias Utilizadas
Python 3: Linguagem principal do projeto.

Lark: Uma biblioteca moderna de parsing para Python, usada para implementar o analisador léxico e sintático.

🚀 Começando
Siga estas instruções para obter uma cópia do projeto e executá-la na sua máquina local.

Pré-requisitos
Python 3.8 ou superior. Pode verificar a sua versão com python3 --version.

Instalação
Clone o repositório para a sua máquina (substitua pela URL do seu repositório):

git clone 
cd pro-sis-interpreter

Instale a única dependência do projeto, a biblioteca Lark:

pip install lark

💻 Como Usar
O interpretador é executado através da linha de comando, passando como argumento o caminho para um ficheiro de código-fonte escrito em PRO-SIS (sugerimos a extensão .psis).

Crie um ficheiro com o seu código, por exemplo, exemplo.psis:

programa meu_primeiro_sistema {
    declare inteiro a, real b, termo x, termo y;

    sistema {
        2 * x + 3 * y = 10,
        x - 5 * y = 2
    }
}

Execute o interpretador a partir da raiz do projeto:

python3 pro_sis_interpreter.py exemplo.psis

Saída Esperada
Verá a seguinte saída no terminal, mostrando a análise do código:

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
      termo
        expr
          fator 2.0
          *
          fator x
        +
        expr
          fator 3.0
          *
          fator y
      termo
        expr
          fator 10.0
    equacao
      termo
        expr
          fator x
        -
        expr
          fator 5.0
          *
          fator y
      termo
        expr
          fator 2.0
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

📂 Estrutura do Projeto
.
├── pro_sis_interpreter.py   # O script principal com o interpretador e o compilador
├── pro_sis_gramatica.lark     # A definição da gramática da linguagem PRO-SIS
├── exemplo.psis               # Um ficheiro de exemplo com código PRO-SIS
└── README.md                  # Este ficheiro

🏛️ Arquitetura e Funcionamento
O processo de interpretação ocorre em três etapas principais:

Gramática (pro_sis_gramatica.lark): A estrutura da linguagem (regras, palavras-chave, tokens) é definida num ficheiro de gramática no formato EBNF, que é lido pelo Lark.

Parsing (Analisador): A classe ProSisCompiler inicializa o parser do Lark com a gramática. Ao receber um código-fonte, o parser valida a sintaxe e, se for válida, gera uma Árvore Sintática Abstrata (AST). Essa árvore representa a estrutura hierárquica do código.

Interpretação (ProSisInterpreter): A classe ProSisInterpreter, que herda de lark.Transformer, percorre a AST de baixo para cima. Para cada regra da gramática (ex: declaracao, fator), um método correspondente é chamado para executar a lógica semântica, como declarar variáveis, verificar tipos e (futuramente) realizar cálculos.

🗺️ Próximos Passos (Roadmap)
Este projeto implementa com sucesso a análise do código, mas a interpretação ainda é um esqueleto. Os próximos passos lógicos são:

[ ] Implementar Operações Matemáticas: Avaliar as expressões aritméticas nos métodos termo, expr e fator.

[ ] Resolver Sistemas de Equações: Utilizar uma biblioteca como NumPy no método que processa o sistema para efetivamente montar e resolver o sistema linear.

[ ] Implementar Funções da Linguagem: Adicionar a lógica para as funções definidas na especificação original, como solve, det, inv e trans.

[ ] Melhorar Tratamento de Erros: Adicionar informações de linha e coluna nas mensagens de erro semântico para facilitar a depuração.

[ ] Adicionar Tipos eq e sis: Implementar a declaração e manipulação dos tipos eq (equação) e sis (sistema), conforme a especificação.

⚖️ Licença
Este projeto está sob a licença MIT. Veja o ficheiro LICENSE para mais detalhes.

👥 Autores
Este projeto é uma implementação baseada no trabalho académico de:

Eduardo Henrique de Sordi Rigamonti

Gabriel Fazion dos Santos

Lucas Galvão Freitas

Thiago de Oliveira Sousa Júnior

Trabalho apresentado para a disciplina de Compiladores na Universidade Federal de Itajubá (UNIFEI).
