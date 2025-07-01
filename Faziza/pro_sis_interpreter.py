import argparse
import numpy as np
from scipy.linalg import lu
from lark import Lark, Transformer, v_args, Token

# Substitua a sua classe ProSisLexer por esta versão simplificada
class ProSisLexer:
    """
    Responsável por executar a análise lexical e imprimir a sequência de tokens
    conforme definidos diretamente na gramática Lark.
    """
    def __init__(self, lark_parser):
        self.parser = lark_parser

    def lex_and_print(self, code):
        """
        Executa o método .lex() do Lark e imprime cada token formatado.
        """
        print("------- Análise Léxica (Tokens Reconhecidos) --------")
        try:
            tokens = list(self.parser.lex(code))
            for token in tokens:
                # Agora imprimimos o tipo do token diretamente, pois ele já está correto!
                print(f"Linha: {token.line}, Coluna: {token.column}, Código: {token.type}, Lexema: {repr(token.value)}")
            print("---------------------------------------------------\n")
        except Exception as e:
            print(f"Ocorreu um erro durante a análise lexical: {e}")


class ProSisInterpreter(Transformer):
    """
    Interpretador completo e funcional.
    Diferencia 'sis' (matriz 2D) de 'eq' (vetor 1D) nos retornos de função.
    """
    # (O código do ProSisInterpreter não muda e permanece exatamente o mesmo)
    def __init__(self):
        self.vars = {}
        print("Interpretador (versão final e funcional) iniciado.")
    def programa(self, *args):
        print("\nPrograma executado com sucesso!")
    @v_args(inline=True)
    def declaracao(self, tipo_token, nome_var_token, valor):
        tipo_declarado = tipo_token.value
        nome_var = nome_var_token.value
        if nome_var in self.vars:
            raise Exception(f"Erro Semântico: A variável '{nome_var}' já foi declarada!")
        valor_final = None
        if isinstance(valor, Token) and valor.type == 'ID':
            nome_var_existente = valor.value
            if nome_var_existente not in self.vars:
                raise Exception(f"Erro Semântico: A variável '{nome_var_existente}' usada na atribuição não foi definida.")
            valor_final = self.vars[nome_var_existente]['valor']
        else:
            valor_final = valor
        tipo_do_valor = None
        if isinstance(valor_final, np.ndarray):
            if valor_final.ndim == 2: tipo_do_valor = 'sis'
            elif valor_final.ndim == 1: tipo_do_valor = 'eq'
        elif isinstance(valor_final, list): tipo_do_valor = 'eq'
        elif isinstance(valor_final, float): tipo_do_valor = 'float'
        elif isinstance(valor_final, int): tipo_do_valor = 'int'
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
        return v[0]
    def sistema(self, equacoes):
        try:
            matriz = np.array(equacoes, dtype=float)
            return matriz
        except ValueError:
            raise Exception("Erro Sintático: Todas as linhas em um sistema devem ter o mesmo número de elementos.")
    def equacao(self, numeros):
        return numeros
    @v_args(inline=True)
    def NUMERO(self, token):
        s = token.value
        val = float(s)
        return int(val) if val.is_integer() else val
    @v_args(inline=True)
    def funcao_chamada(self, func_token, nome_var_token):
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
        func_token = items[0]
        id_tokens = items[1:]
        nome_funcao = func_token.value
        if not id_tokens:
            raise Exception(f"Erro Sintático: O comando '{nome_funcao}' requer pelo menos um argumento.")
        nome_var_principal = id_tokens[0].value
        if nome_var_principal not in self.vars:
            raise Exception(f"Erro Semântico: A variável '{nome_var_principal}' não foi definida.")
        print(f"\n-=-=- Executando '{nome_funcao}' no sistema '{nome_var_principal}' -=-=-")
        valor_da_var = self.vars[nome_var_principal]['valor']
        print(valor_da_var.T if nome_funcao == 'trans' else valor_da_var)

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
        return token.value



class ProSisCompiler:
    def __init__(self, grammar_file):
        try:
            with open(grammar_file, 'r', encoding='utf-8') as f:
                self.pro_sis_parser = Lark(f.read(), start='programa')
            self.interpreter = ProSisInterpreter()
            # ---> LINHA ADICIONADA <---
            # Cria a instância do lexer, passando o parser como argumento
            self.lexer = ProSisLexer(self.pro_sis_parser)
        except FileNotFoundError:
            raise Exception(f"Erro: Arquivo de gramática '{grammar_file}' não encontrado.")
    
    def run(self, code_to_run):
        # A análise sintática (parsing) acontece aqui e já inclui a análise lexical
        tree = self.pro_sis_parser.parse(code_to_run)
        
        # Impressão da árvore, como antes
        print("------- Árvore Sintática Gerada --------")
        print(tree.pretty())
        print("----------------------------------------\n")

        # ---> LINHA ADICIONADA <---
        # Chamamos o método para imprimir a lista de tokens.
        # Ele re-executa a análise lexical para fins de visualização.
        self.lexer.lex_and_print(code_to_run)

        # A interpretação (transformação da árvore) acontece aqui
        result = self.interpreter.transform(tree)
        return result

def main():
    # (O código de main() não precisa de alterações)
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
        compiler.run(codigo_fonte)
    except Exception as e:
        print(f"\nOcorreu um erro durante a compilação: {e}")

if __name__ == "__main__":
    main()
