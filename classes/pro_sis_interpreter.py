import argparse
import os
import numpy as np
from scipy.linalg import lu
from lark import Lark, Transformer, v_args, Token, Tree

class ProSisLexer:
    """
    Responsável por executar a análise lexical e imprimir a sequência de tokens
    conforme definidos diretamente na gramática Lark.
    """
    def __init__(self, lark_parser):
        self.parser = lark_parser

    def lex_and_print(self, code, caminho_saida_txt="analise_lexica.txt"):
        """
        Executa a análise lexical, imprime os tokens e salva em um arquivo.txt.
        O caminho de saída pode ser especificado (usado para refletir o nome do arquivo de entrada).
        """
        linhas_saida = []
        header = "------- Análise Léxica (Tokens Reconhecidos) --------"
        footer = "---------------------------------------------------\n"
        
        print(header)
        linhas_saida.append(header)

        try:
            tokens = list(self.parser.lex(code))
            for token in tokens:
                linha = f"Linha: {token.line}, Coluna: {token.column}, Código: {token.type}, Lexema: {repr(token.value)}"
                print(linha)
                linhas_saida.append(linha)
            print(footer)
            linhas_saida.append(footer)
        except Exception as e:
            erro_msg = f"Ocorreu um erro durante a análise lexical: {e}"
            print(erro_msg)
            linhas_saida.append(erro_msg)

        with open(caminho_saida_txt, "w", encoding="utf-8") as f:
            for linha in linhas_saida:
                f.write(linha + "\n")




class ProSisInterpreter(Transformer):
    """
    Interpretador completo e funcional.
    Diferencia 'sis' (matriz 2D) de 'eq' (vetor 1D) nos retornos de função.
    """
    
    def __init__(self):
        """
        Inicializa o interpretador PRO-SIS.
        
        Attributes:
            vars (dict): Dicionário que armazena as variáveis declaradas no programa,
                        com seus tipos e valores.
        """
        self.vars = {}
        print("Interpretador (versão final e funcional) iniciado.")
        
    def programa(self, *args):
        """
        Método chamado ao final da execução do programa.
        Indica que o programa foi executado com sucesso.
        
        Args:
            *args: Argumentos variados vindos da árvore sintática.
        """
        print("\nPrograma executado com sucesso!")
        
    @v_args(inline=True)
    def declaracao(self, tipo_token, nome_var_token, operador_token, valor):
        """
        Processa a declaração e inicialização de uma variável.
        
        Realiza a verificação dos tipos e de compatibilidade entre o tipo declarado
        e o valor atribuído. Suporta tipos: int, float, eq (equação/vetor) e sis (sistema/matriz).
        
        Args:
            tipo_token: Token contendo o tipo da variável (int, float, eq, sis)
            nome_var_token: Token contendo o nome da variável
            operador_token: Token do operador de atribuição (=)
            valor: Valor a ser atribuído (pode ser Token, lista, np.ndarray, etc.)
            
        Raises:
            Exception: Se houver incompatibilidade de tipos ou se a variável não foi definida
        """
        tipo_declarado = tipo_token.children[0].value
        nome_var = nome_var_token.value

        if isinstance(valor, Token):
            if valor.type == 'TK_NUMERO':
                valor = float(valor.value)
                valor = int(valor) if valor.is_integer() else valor
            elif valor.type == 'ID':
                nome_var_existente = valor.value
                if nome_var_existente not in self.vars:
                    raise Exception(f"Erro Semântico: A variável '{nome_var_existente}' usada na atribuição não foi definida.")
                valor = self.vars[nome_var_existente]['valor']

        valor_final = valor

        tipo_do_valor = None
        if isinstance(valor_final, np.ndarray):
            if valor_final.ndim == 2:
                tipo_do_valor = 'sis'
            elif valor_final.ndim == 1:
                tipo_do_valor = 'eq'
        elif isinstance(valor_final, list):
            tipo_do_valor = 'eq'
        elif isinstance(valor_final, float):
            tipo_do_valor = 'float'
        elif isinstance(valor_final, int):
            tipo_do_valor = 'int'

        if tipo_do_valor is None:
            raise Exception(f"Erro Interno: Tipo de valor desconhecido para '{valor_final}' (tipo real: {type(valor_final)}).")

        if tipo_declarado == 'int' and tipo_do_valor == 'float':
            if not valor_final.is_integer():
                raise Exception(f"Erro Semântico: Impossível atribuir o float com casas decimais '{valor_final}' a uma variável do tipo 'int'.")
            valor_final = int(valor_final)
            tipo_do_valor = 'int'

        if tipo_declarado != tipo_do_valor:
            raise Exception(f"Erro Semântico: Impossível atribuir um valor do tipo '{tipo_do_valor}' a uma variável do tipo '{tipo_declarado}'.")

        self.vars[nome_var] = {'tipo': tipo_declarado, 'valor': valor_final}
        print(f"-> Variável '{nome_var}' (tipo: {tipo_declarado}) declarada e inicializada.")

    def valor(self, v):
        """
        Extrai o primeiro elemento de uma lista de valores.
        
        Args:
            v (list): Lista contendo valores
            
        Returns:
            O primeiro elemento da lista de valores
        """
        return v[0]
    
    def sistema(self, equacoes):
        """
        Processa uma lista de equações e cria uma matriz, usando numpy, que representa um sistema.
        
        Filtra apenas os elementos que são listas (equações válidas) e converte
        para uma matriz NumPy bidimensional.
        
        Args:
            equacoes (list): Lista contendo equações (listas de números)
            
        Returns:
            np.ndarray: Matriz representando o sistema de equações
            
        Raises:
            Exception: Se as equações não tiverem o mesmo número de elementos
        """
        
        #print(f"[DEBUG] Equações recebidas no sistema: {equacoes}")

        equacoes_filtradas = [n for n in equacoes if isinstance(n, list)]
        
        #print(f"[DEBUG] Equações filtradas no sistema: {equacoes_filtradas}")
        

        try:
            matriz = np.array(equacoes_filtradas, dtype=float)
            return matriz
        except ValueError as e:
            #print(f"[DEBUG] Erro de conversão: {e}")
            raise Exception("Erro Sintático: Todas as linhas em um sistema devem ter o mesmo número de elementos.")

    
    def equacao(self, numeros):
        """
        Processa uma lista de tokens numéricos e os converte para uma lista de números.
        
        Filtra tokens do tipo TK_NUMERO e os converte para int ou float conforme apropriado.
        
        Args:
            numeros (list): Lista de tokens contendo números
            
        Returns:
            list: Lista de números convertidos (int ou float)
        """
        numeros_convertidos = []
        for n in numeros:
            if isinstance(n, Token) and n.type == 'TK_NUMERO':
                valor = float(n.value)
                valor = int(valor) if valor.is_integer() else valor
                #print(f"[DEBUG] Convertendo token '{n.value}' para valor: {valor}")
                
                numeros_convertidos.append(valor)
        return numeros_convertidos


    @v_args(inline=True)
    def NUMERO(self, token):
        """
        Converte um token numérico para int ou float.
        
        Args:
            token: Token contendo um valor numérico
            
        Returns:
            int or float: Valor convertido (int se for inteiro, float caso contrário)
        """
        s = token.value
        val = float(s)
        return int(val) if val.is_integer() else val
    
    @v_args(inline=True)
    def funcao_chamada(self, func_token, nome_var_token):
        """
        Executa uma chamada de função matemática sobre uma matriz/sistema.
        
        Suporta funções: inv (inversa), trans (transposta), retP/retL/retU (decomposição LU),
        retD (diagonal), det (determinante), solve (resolução do sistema).
        
        Args:
            func_token: Token contendo o nome da função
            nome_var_token: Token contendo o nome da variável (deve ser tipo 'sis')
            
        Returns:
            np.ndarray or float: Resultado da operação matemática
            
        Raises:
            Exception: Se a variável não for do tipo 'sis', matriz não for quadrada
                      (quando necessário), ou ocorrer erro de álgebra linear
        """
        nome_funcao = func_token.value
        nome_var = nome_var_token.value
        print(f"-> Resolvendo chamada de função: {nome_funcao}({nome_var})")
        if nome_var not in self.vars or self.vars[nome_var]['tipo'] != 'sis':
            raise Exception(f"Erro: A função '{nome_funcao}' requer uma variável do tipo 'sis', mas '{nome_var}' não é.")
        matriz_aumentada = self.vars[nome_var]['valor']
        A = matriz_aumentada[:, :-1]
        b = matriz_aumentada[:, -1]
        if A.shape[0] != A.shape[1] and nome_funcao not in ['trans', 'solve']:
             raise Exception(f"Erro: A matriz de coeficientes (A) não é quadrada para a função '{nome_funcao}'.")
        try:
            if nome_funcao == 'inv': return np.linalg.inv(A)
            if nome_funcao == 'trans': return A.T
            if nome_funcao in ['retP', 'retL', 'retU']:
                P, L, U = lu(A)
                if nome_funcao == 'retP': return P
                if nome_funcao == 'retL': return L
                if nome_funcao == 'retU': return U
            if nome_funcao == 'retD': return np.diag(np.diag(A))
            if nome_funcao == 'det': return np.linalg.det(A)
            if nome_funcao == 'solve': return np.linalg.solve(A, b)
            raise Exception(f"Erro Semântico: A função '{nome_funcao}' não pode ser usada em uma atribuição pois não retorna um valor.")
        except np.linalg.LinAlgError:
            raise Exception(f"Erro de Álgebra Linear: A operação '{nome_funcao}' não pôde ser concluída (matriz singular?).")

    def comando(self, items):
        """
        Processa e executa um comando de função sobre uma variável.
        
        Extrai o token da função e o nome da variável dos itens fornecidos,
        valida se a variável existe e executa a função correspondente,
        exibindo o resultado.
        
        Args:
            items (list): Lista contendo tokens e árvores sintáticas do comando
            
        Raises:
            Exception: Se o comando estiver mal formado ou a variável não existir
        """

        # print("\n[DEBUG] Itens recebidos em 'comando':")
        # for idx, item in enumerate(items):
        #     print(f"  Item {idx}: {item} (tipo: {type(item)})")

        func_token = None
        id_token = None

        for item in items:
            if isinstance(item, Tree) and item.data == 'funcao_comando':
                
                func_token = item.children[0]
            elif isinstance(item, Token) and item.type == 'ID':
                id_token = item
            

        if not func_token or not id_token:
            raise Exception("Erro Sintático: Comando mal formado. Esperado: funcao_comando ID end_comando")

        nome_funcao = func_token.value
        nome_var_principal = id_token.value

        if nome_var_principal not in self.vars:
            raise Exception(f"Erro Semântico: A variável '{nome_var_principal}' não foi definida.")

        print(f"\n-=-=- Executando '{nome_funcao}' no sistema '{nome_var_principal}' -=-=-")
        
        # Verificar se é um sistema válido
        if self.vars[nome_var_principal]['tipo'] != 'sis':
            raise Exception(f"Erro: A função '{nome_funcao}' requer uma variável do tipo 'sis'.")
        
        matriz_aumentada = self.vars[nome_var_principal]['valor']
        
        try:
            if nome_funcao == 'solve':
                # Para solve, assumir que é matriz aumentada [A|b]
                if matriz_aumentada.shape[1] < 2:
                    raise Exception("Erro: Matriz deve ter pelo menos 2 colunas para resolução de sistema.")
                A = matriz_aumentada[:, :-1]  # Todas as colunas exceto a última
                b = matriz_aumentada[:, -1]   # Última coluna (termos independentes)
                if A.shape[0] != A.shape[1]:
                    raise Exception("Erro: Para resolver o sistema, a matriz de coeficientes deve ser quadrada.")
                solucao = np.linalg.solve(A, b)
                print("Solução do sistema:")
                print(solucao)
                
            elif nome_funcao == 'det':
                # Para determinante, usar toda a matriz se for quadrada, ou só os coeficientes se for aumentada
                if matriz_aumentada.shape[0] == matriz_aumentada.shape[1]:
                    # Matriz já é quadrada
                    A = matriz_aumentada
                else:
                    # Matriz aumentada - usar só os coeficientes
                    A = matriz_aumentada[:, :-1]
                    if A.shape[0] != A.shape[1]:
                        raise Exception("Erro: Para calcular determinante, a matriz de coeficientes deve ser quadrada.")
                determinante = np.linalg.det(A)
                print(f"Determinante: {determinante}")
                
            elif nome_funcao == 'inv':
                # Para inversa, usar toda a matriz se for quadrada, ou só os coeficientes se for aumentada
                if matriz_aumentada.shape[0] == matriz_aumentada.shape[1]:
                    A = matriz_aumentada
                else:
                    A = matriz_aumentada[:, :-1]
                    if A.shape[0] != A.shape[1]:
                        raise Exception("Erro: Para calcular a inversa, a matriz de coeficientes deve ser quadrada.")
                inversa = np.linalg.inv(A)
                print("Matriz inversa:")
                print(inversa)
                
            elif nome_funcao == 'trans':
                # Para transposta, usar toda a matriz
                transposta = matriz_aumentada.T
                print("Matriz transposta:")
                print(transposta)
                
            elif nome_funcao == 'retP':
                if matriz_aumentada.shape[0] == matriz_aumentada.shape[1]:
                    A = matriz_aumentada
                else:
                    A = matriz_aumentada[:, :-1]
                    if A.shape[0] != A.shape[1]:
                        raise Exception("Erro: Para decomposição LU, a matriz de coeficientes deve ser quadrada.")
                P, L, U = lu(A)
                print("Matriz P (permutação):")
                print(P)
                
            elif nome_funcao == 'retL':
                if matriz_aumentada.shape[0] == matriz_aumentada.shape[1]:
                    A = matriz_aumentada
                else:
                    A = matriz_aumentada[:, :-1]
                    if A.shape[0] != A.shape[1]:
                        raise Exception("Erro: Para decomposição LU, a matriz de coeficientes deve ser quadrada.")
                P, L, U = lu(A)
                print("Matriz L (triangular inferior):")
                print(L)
                
            elif nome_funcao == 'retU':
                if matriz_aumentada.shape[0] == matriz_aumentada.shape[1]:
                    A = matriz_aumentada
                else:
                    A = matriz_aumentada[:, :-1]
                    if A.shape[0] != A.shape[1]:
                        raise Exception("Erro: Para decomposição LU, a matriz de coeficientes deve ser quadrada.")
                P, L, U = lu(A)
                print("Matriz U (triangular superior):")
                print(U)
                
            elif nome_funcao == 'retD':
                if matriz_aumentada.shape[0] == matriz_aumentada.shape[1]:
                    A = matriz_aumentada
                else:
                    A = matriz_aumentada[:, :-1]
                    if A.shape[0] != A.shape[1]:
                        raise Exception("Erro: Para extrair diagonal, a matriz de coeficientes deve ser quadrada.")
                diagonal = np.diag(np.diag(A))
                print("Matriz diagonal:")
                print(diagonal)
                
            else:
                raise Exception(f"Erro: Função '{nome_funcao}' não reconhecida.")
                
        except np.linalg.LinAlgError as e:
            raise Exception(f"Erro de Álgebra Linear: {e} (matriz pode ser singular)")
        


    def TK_OPE_ATB(self, token):
        return token.value

    def TK_DELIM_MULT(self, token):
        return token.value
    
    def TK_DELIM_INIT_SISTEMA(self, token):
        return token.value

    def TK_DELIM_END_SISTEMA(self, token):
        return token.value
        
    def TK_DELIM_INIT_EQ(self, token):
        return token.value

    def TK_DELIM_END_EQ(self, token):
        return token.value
        
    def end_comando(self, token):
        return token
    

class ProSisCompiler:
    """
    Compilador principal para a linguagem PRO-SIS.
    
    Integra o analisador léxico, sintático e o interpretador semântico.
    Responsável por coordenar todo o processo de compilação desde a análise
    lexical até a execução do código.
    
    Attributes:
        pro_sis_parser (Lark): Parser Lark para análise sintática
        interpreter (ProSisInterpreter): Interpretador semântico
        lexer (ProSisLexer): Analisador léxico
    """
    def __init__(self, grammar_file):
        """
        Inicializa o compilador carregando a gramática do .lark e criando os componentes.
        
        Args:
            grammar_file (str): Caminho para o arquivo de gramática .lark
            
        Raises:
            Exception: Se o arquivo de gramática não for encontrado
        """
        try:
            with open(grammar_file, 'r', encoding='utf-8') as f:
                self.pro_sis_parser = Lark(f.read(), start='programa')
            
            self.interpreter = ProSisInterpreter()
            self.lexer = ProSisLexer(self.pro_sis_parser)

        except FileNotFoundError:
            raise Exception(f"Erro: Arquivo de gramática '{grammar_file}' não encontrado.")
    
    def run(self, code_to_run, code_to_run_path):
        """
        Executa todo o processo de compilação do código PRO-SIS.
        
        Realiza a análise sintática, gera e exibe a árvore sintática,
        executa a análise léxica salvando os tokens em arquivo,
        e por fim executa o interpretador semântico.
        
        Args:
            code_to_run (str): Código fonte PRO-SIS a ser compilado
            code_to_run_path (str): Caminho do arquivo de entrada (para nomear arquivos de saída)
            
        Returns:
            O resultado da interpretação semântica
            
        Raises:
            Exception: Se houver erros durante qualquer fase da compilação
        """

        tree = self.pro_sis_parser.parse(code_to_run)

        print("------- Árvore Sintática Gerada --------")
        print(tree.pretty())
        print("----------------------------------------\n")

        nome_base = os.path.splitext(os.path.basename(code_to_run_path))[0]
        saida_txt = f"{nome_base}.txt"
        self.lexer.lex_and_print(code_to_run, caminho_saida_txt=saida_txt)

        result = self.interpreter.transform(tree)
        return result

def main():
    """
    Função principal do programa.
    
    Configura o parser de argumentos da linha de comando, carrega o arquivo
    de entrada e inicia o processo de compilação.
    
    Trata erros de arquivo não encontrado e erros gerais de compilação.
    """
    cli_parser = argparse.ArgumentParser(description="Interpretador para a linguagem PRO-SIS")
    cli_parser.add_argument("arquivo_entrada", help="Caminho para o arquivo .psis a ser executado.")
    args = cli_parser.parse_args()
    try:
        with open(args.arquivo_entrada, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada '{args.arquivo_entrada}' não encontrado.")
        return
    try:
        print(f"Iniciando a compilação do arquivo '{args.arquivo_entrada}'...")
        compiler = ProSisCompiler("pro_sis_grammar.lark")
        compiler.run(codigo_fonte, args.arquivo_entrada)
    except Exception as e:
        print(f"\nOcorreu um erro durante a compilação: {e}")

if __name__ == "__main__":
    main()
