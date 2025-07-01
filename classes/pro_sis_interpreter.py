import argparse
import numpy as np
from lark import Lark, Transformer, v_args

class ProSisInterpreter(Transformer):
    """
    Versão final e robusta. Utiliza Tokens nomeados para os tipos e funções,
    garantindo um processamento estável e à prova de erros.
    """
    def __init__(self):
        self.vars = {}
        print("Interpretador (versão final e à prova de falhas) iniciado.")

    def programa(self, *args):
        print("\nPrograma executado com sucesso!")

    # ----------------- Processamento de Declarações -----------------

    @v_args(inline=True)
    def declaracao(self, tipo_token, nome_var_token, valor):
        tipo = tipo_token.value
        nome_var = nome_var_token.value

        if nome_var in self.vars:
            raise Exception(f"Erro Semântico: A variável '{nome_var}' já foi declarada!")

        if tipo == 'sis' and not isinstance(valor, np.ndarray):
             raise Exception(f"Erro: Tentando atribuir um valor não-sistema a uma variável 'sis'.")
        if tipo in ['int', 'float'] and not isinstance(valor, (int, float)):
             raise Exception(f"Erro: Tentando atribuir um valor não-numérico a uma variável '{tipo}'.")

        self.vars[nome_var] = {'tipo': tipo, 'valor': valor}
        print(f"-> Variável '{nome_var}' (tipo: {tipo}) declarada e inicializada.")

    # ----------------- Processamento de Estruturas de Dados -----------------

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
    def expressao_numerica(self, numero_token):
        return float(numero_token.value)
    
    # ----------------- Processamento de Comandos -----------------

    @v_args(inline=True)
    def comando(self, func_token, nome_var_token):
        # A regra 'func' foi substituída pelo Token 'FUNC'. Recebemos o token diretamente.
        nome_funcao = func_token.value
        nome_var = nome_var_token.value

        if nome_var not in self.vars or self.vars[nome_var]['tipo'] != 'sis':
            raise Exception(f"Erro: O comando '{nome_funcao}' requer uma variável do tipo 'sis', mas '{nome_var}' não é.")
        
        matriz_aumentada = self.vars[nome_var]['valor']
        A = matriz_aumentada[:, :-1]
        b = matriz_aumentada[:, -1]

        if A.shape[0] != A.shape[1]:
            raise Exception("Erro: A matriz de coeficientes (A) não é quadrada.")

        print(f"\n-=-=- Executando '{nome_funcao}' no sistema '{nome_var}' -=-=-")
        try:
            if nome_funcao == 'solve':
                solucao = np.linalg.solve(A, b)
                print("Solução do sistema:", solucao)
            elif nome_funcao == 'det':
                print("Determinante:", np.linalg.det(A))
            elif nome_funcao == 'inv':
                print("Matriz Inversa:\n", np.linalg.inv(A))
            elif nome_funcao == 'trans':
                print("Matriz Transposta:\n", A.T)
            else:
                print(f"Função '{nome_funcao}' reconhecida, mas não implementada.")
        except np.linalg.LinAlgError:
            print(f"Erro de Álgebra Linear: A operação '{nome_funcao}' não pôde ser concluída (matriz singular).")


# ----------------- Compilador e Execução (sem alterações) -----------------
class ProSisCompiler:
    def __init__(self, grammar_file):
        try:
            with open(grammar_file, 'r', encoding='utf-8') as f:
                self.pro_sis_parser = Lark(f.read(), start='programa')
            self.interpreter = ProSisInterpreter()
        except FileNotFoundError:
            raise Exception(f"Erro: Arquivo de gramática '{grammar_file}' não encontrado.")
    
    def run(self, code_to_run):
        tree = self.pro_sis_parser.parse(code_to_run)
        print("------- Árvore Sintática Gerada --------")
        print(tree.pretty())
        print("----------------------------------------\n")
        result = self.interpreter.transform(tree)
        return result

def main():
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