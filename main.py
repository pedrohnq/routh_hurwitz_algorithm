"""
# Atividade da disciplina Modelagem e Análise de Sistemas Dinâmicos (DCA0110)

# Componentes:
 - Pedro Henrique Leite dos Santos
 - Edson Augusto Dias Gomes
 - Luiz Gustavo Bezerra Rodrigues
 - Joanderson Luan da Silva Linhares

"""

import pandas as pd


class RouthHurwitzAlgorithm:
    """
    Algoritmo responsável por montar a Matriz de Routh-Hurwitz e fornecer algumas informações 
    sobre o sistema

    ### Atributos:
        - degree [int]: Salva o grau do polinômio
        - coefficients [dict]: Salva os coeficiêntes do polinômi
        - signal_changes [int]: Salva o número de mudanças de sinal na primeira coluna da matriz
        - matrix [DataFrame]: Matriz de Routh-Hurwitz montada
    """

    def __init__(self) -> None:
        self.degree = 0
        self.coefficients = {}
        self.signal_changes = 0
        self.matrix = pd.DataFrame()

    def collect_data(self) -> None:
        """
        Faz a validação e coleta inicial do polinômio
        """
        self.degree = int(input('Digite o grau do polinômio: '))

        if self.degree < 3:
            raise ValueError('O polinômio deve ter grau 3 ou acima')
        
        for i in range(self.degree, -1, -1):
            self.coefficients[f's{i}'] = float(input(f'Digite o valor do coeficiente de s{i}: '))

    def generate_matrix(self) -> None:
        """
        Gera a Matriz com base no polinômio fornecido
        """
        num_columns = (self.degree//2) + 1
        line_index = [f's{i}' for i in range(self.degree, -1, -1)]
        col_index = [f'col{i}' for i in range(1, num_columns + 1)]
        self.matrix = pd.DataFrame(0, index=line_index, columns=col_index)

        idx_line_1 = range(self.degree, -1, -2)
        idx_line_2 = range(self.degree-1, -1, -2)

        for idx in idx_line_1:
            self.matrix.loc[f's{self.degree}', f'col{idx_line_1.index(idx)+1}'] = self.coefficients.get(f's{idx}', 0)
        for idx in idx_line_2:
            self.matrix.loc[f's{self.degree-1}', f'col{idx_line_2.index(idx)+1}'] = self.coefficients.get(f's{idx}', 0)

        current_degree = self.degree-2

        while current_degree >= 0:
            prev_line = self.matrix.loc[f's{current_degree+1}']
            two_prev_line = self.matrix.loc[f's{current_degree+2}']
            for i in range(1, len(two_prev_line)):
                x = (
                    (prev_line.loc['col1'] * two_prev_line.loc[f'col{i+1}']) 
                    - (two_prev_line['col1'] * prev_line[f'col{i+1}'])
                )
                y = prev_line.loc['col1']
                value = x/y if y != 0 else 0
                self.matrix.loc[f's{current_degree}', f'col{i}'] = value

            current_degree -= 1
    
    def count_signal_changes(self) -> None:
        """
        Conta a quantidade de alternância de sinal na primeira coluna da Matriz
        """
        first_column = self.matrix['col1'].tolist()
        for i in range(1, len(first_column)):
            if first_column[i] * first_column[i-1] < 0:
                self.signal_changes += 1

    def show_data(self) -> None:
        """
        Método que serve apenas para renderizar na tela a Matriz e algumas informações úteis
        """
        print('\n')
        print('A Matriz de Routh-Hurwitz obtida foi:')
        print(self.matrix)

        print('\n')
        print('O sistema é estável?', 'Sim' if self.signal_changes == 0 else 'Não')

        print('\n')
        print('Quantidade de polos no semi-plano direito:', self.signal_changes)
        print('Quantidade de polos no semi-plano esquerdo:', self.degree - self.signal_changes)
    
    def execute(self) -> None:
        """
        Executa o algoritmo chamanando todos os métodos
        """
        self.collect_data()
        self.generate_matrix()
        self.count_signal_changes()
        self.show_data()



if __name__ == '__main__':
    RouthHurwitzAlgorithm().execute()