import numpy as np
import matplotlib.pyplot as plt
import time as tm
import copy

def pause():
    wait = input('type any char to continue\n')
    print('stop')

# Gera a semente para os numeros aleatorios
def GeraeEstabeleceSeed():
    timefloat = tm.time()
    # print('timefloat = %f' % (timefloat))
    timeround = round(timefloat)
    # print('timeround = %f' % (timeround))
    timeint = int(timeround)
    # print('timeint = %d' % (timeint))
    timeseed = timeint % 10000
    # print('timeseed = %d' % (timeseed))
    np.random.seed(timeseed)
    return timeseed

# Gerada pelo ChatGPT - Fixa para 4 x 4
def PlotarMatriz(LM):

    n = LM.shape[0]

    try:
      assert n == 4
    except Exception:
      print("PlotarMatriz: Ordem da Matriz deve ser igual a 4 para Plotar")
      exit()


    # Sample matrix of background colors
    background_colors = [
        ['#FF0000', '#00FF00', '#0000FF', '#0000FF'],
        ['#FFFF00', '#00FFFF', '#FF00FF', '#0000FF'],
        ['#C0C0C0', '#800080', '#008000', '#0000FF'],
        ['#C0C0C0', '#800080', '#008000', '#0000FF']
    ]

    # Sample matrix of font colors
    font_colors = [
        ['#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF'],
        ['#000000', '#FFFFFF', '#000000', '#FFFFFF'],
        ['#000000', '#FFFFFF', '#000000', '#FFFFFF'],
        ['#000000', '#FFFFFF', '#000000', '#FFFFFF']
    ]

    n = len(LM)  # Size of the matrix

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Create a heatmap with labeled cells
    cax = ax.matshow(np.zeros((n, n)), cmap='cool', vmin=0, vmax=1)

    # Loop through each cell in the matrix
    for i in range(n):
        for j in range(n):
            labels = LM[i][j]  # Get the list of labels for the cell
            background_color = background_colors[i][j]
            font_color = font_colors[i][j]

            # Add horizontal and vertical lines to separate cells
            ax.axhline(i - 0.5, color='black', linewidth=1)
            ax.axvline(j - 0.5, color='black', linewidth=1)

            # Add text for each label with specified colors and background
            for k, label in enumerate(labels):
                if k < 3:  # Limit to a maximum of 3 labels per cell
                    x_position = j
                    y_position = i + (k - 1.0) * 0.2  # Adjusted position
                    ax.text(x_position, y_position, label, ha='center', va='center', fontsize=12,
                            bbox=dict(boxstyle='round', facecolor=background_color, edgecolor='black'),
                            color=font_color)

    # Show the plot
    plt.show()


class Agente:
    def __init__(self, n = 4, percent_pits = 15 ):
        # Propriedades
        self.n = n
        self.percent_pits = percent_pits
        self.npits = int(self.n * self.n * self.percent_pits / 100)
        self.nwumpus = 1
        self.nouro = 1
        self.nagente = 1
        # Dicionarios
        self.dict_agent = {'Vazio': 0, 'Agente': 1, 'Wumpus': 2, 'Brisa': 3, 'Cheiro': 4, 'Ouro': 5, 'Buraco': 6,
                      'Brilho': 7}
        self.reverse_dict_agent = {value: key for key, value in self.dict_agent.items()}
        self.dict_move = {0: 'Direita', 1: 'Esquerda', 2: 'PraCima', 3: 'Pra Baixo'}
        self.dict_nobjs = {'Agente': self.nagente, 'Buraco': self.npits, 'Wumpus': self.nwumpus, 'Ouro': self.nouro}
        self.dict_efeitos = {'Wumpus': 'Cheiro', 'Buraco': 'Brisa', 'Ouro': 'Brilho'}
        # Matrizes de Listas e posicao inicial do agente
        self.WM, self.WS, self.linha_agente, self.coluna_agente = self._GeraMatrizes_Posicao_Inicial_Agente()

    def __str__(self):
        stragente = 'Jogo Wumpus para :\n' +\
            "\tOrdem da Matriz n = "+ str(self.n)+"\n"+\
            "\tNumero de Buracos npits = "+str(self.npits)+"\n"+\
            "\tNumero de Agentes nagente = "+str(self.nagente)+"\n"+\
            "\tNumero de Wumpus  nwumpus ="+str(self.nwumpus)+"\n"\
            "\tNumero de tesouros nouro ="+str(self.nouro)+"\n"
        return stragente

    # Gera Matrizes Wumpus e posição inicial do agente na Construção
    def _GeraMatrizes_Posicao_Inicial_Agente(self):
        # Gerar  Matriz Wumpus de listas vazias
        WM, linha_agente, Linha_coluna = self._Preencher_WM_Random()
        WM = self._Gerar_efeitos(WM)
        WS = self._GetLabelsMatrix(WM)

        return WM, WS, linha_agente, Linha_coluna

    # Gera Matriz Wumpus Vazia
    def _Gerar_Matriz_Wumpus(self):
        matrix = np.zeros((self.n, self.n), dtype=object)
        for i in range(self.n):
            for j in range(self.n):
                matrix[i, j] = [0]
        return matrix

    # Preenche células da Matrix com agente, Wumpus e Ouro
    def _Preencher_WM_Random(self):
        WM = self._Gerar_Matriz_Wumpus()
        limite_objetos = 20
        linha_agente = None
        coluna_agente = None
        assert (np.sum([self.dict_nobjs[key] for key in self.dict_nobjs.keys()]) < limite_objetos)
        for key in self.dict_nobjs.keys():
            for num in range(self.dict_nobjs[key]):
                Preenchido = False
                while (not Preenchido):
                    linha = np.random.randint(0, self.n)
                    coluna = np.random.randint(0, self.n)
                    if WM[linha, coluna][0] == 0:
                        WM[linha, coluna][0] = self.dict_agent[key]
                        # Se agente guarda posicao inicial
                        if (self.dict_agent[key] == 1):
                            linha_agente = linha
                            coluna_agente = coluna
                        Preenchido = True


        return WM, linha_agente, coluna_agente

    def _Gerar_efeitos(self, WM):
        n = WM.shape[0]

        # Percorrer o dicinário de efeitos
        for key in self.dict_efeitos.keys():
            # Percorrer a Matriz Wumpus de listas
            for linha in range(n):
                for coluna in range(n):
                    if any(self.dict_agent[key] == value for value in WM[linha][coluna]):
                        WM = self._Adicionar_efeito(WM, self.dict_agent[self.dict_efeitos[key]], linha, coluna)
        return WM

    def _Adicionar_efeito_a_direita(self, WM, efeito, linha, coluna):
        WM[linha][coluna + 1].append(efeito)
        return WM

    def _Adicionar_efeito_a_esquerda(self, WM, efeito, linha, coluna):
        WM[linha][coluna - 1].append(efeito)
        return WM

    def _Adicionar_efeito_acima(self, WM, efeito, linha, coluna):
        WM[linha - 1][coluna].append(efeito)
        return WM

    def _Adicionar_efeito_abaixo(self, WM, efeito, linha, coluna):
        WM[linha + 1][coluna].append(efeito)
        return WM

    def _Adicionar_efeito(self, WM, efeito, linha, coluna):
        n = WM.shape[0]
        if linha == 0:
            self._Adicionar_efeito_abaixo(WM, efeito, linha, coluna)
        elif linha == n - 1:
            WM = self._Adicionar_efeito_acima(WM, efeito, linha, coluna)
        else:
            WM = self._Adicionar_efeito_abaixo(WM, efeito, linha, coluna)
            WM = self._Adicionar_efeito_acima(WM, efeito, linha, coluna)
        if coluna == 0:
            WM = self._Adicionar_efeito_a_direita(WM, efeito, linha, coluna)
        elif coluna == n - 1:
            WM = self._Adicionar_efeito_a_esquerda(WM, efeito, linha, coluna)
        else:
            WM = self._Adicionar_efeito_a_direita(WM, efeito, linha, coluna)
            WM = self._Adicionar_efeito_a_esquerda(WM, efeito, linha, coluna)
        return WM

    # Transforma matriz em Matriz de Labels
    def _GetLabelsMatrix(self, LI):

        n = LI.shape[0]

        deep_copy_matrix = copy.deepcopy(LI)

        # Iterate through each row in the matrix of integer codes (LI)
        for row in range(n):
            for col in range(n):
                count = 0
                for code in LI[row][col]:
                    if (isinstance(LI[row, col][count], int)):
                        label = self.reverse_dict_agent[code]
                        deep_copy_matrix[row, col][count] = label
                    count = count + 1

        return deep_copy_matrix

    def GetPosInicialAgente(self):
        return self.linha_agente, self.coluna_agente

    def GetWM(self):
        return self.WM
    def GetWS(self):
        return self.WS

    # Responde ao botao Reset
    def Reset(self):
        self.WM, self.WS, self.linha_agente, self.coluna_agente = self._GeraMatrizes_Posicao_Inicial_Agente()
        # Alterar Tela

    # Responde ao botao Direita
    def Direita(self):
        print('Movimento a direita')
        # Alterar tela

    # Responde ao botao Esquerda
    def Esquerda(self):
        print('Movimento a esquerda')
        # Alterar tela

    # Responde ao botao PraCima
    def PraCima(self):
        print('Movimento para cima')
        # Alterar tela

    # Responde ao botao PraCima
    def PraCima(self):
        print('Movimento para baixo')
        # Alterar Tela

    def _CaiuBuraco(self):
        print('Caiu no Buraco')
        # Alterar Tela

    def _CaiuWumpus(self):
        print('Caiu no Wumpus')
        # Alterar tela

    def _AchouTesouro(self):
        print('Achou Tesouro')
        # Alterar tela

    def SimularJogo(self, njogadas):
        for i in range(njogadas):
            # Sortear a direção para qual ir
            # usando np.random.randint(0, self.4) e  self.dict_move
            # Imprimir o número da jogada
            print('Jogador escolhe (direta ou esquerda, ou pra cima ou pra baixo) i = %d'%(i))
            # Imprimir o sentido da jogada (direita, esquerda, pra baixo, pra cima)
            # Imprimir a Matriz WS (Matriz  de Strings)
            # Imprimir o resultado da ação
            # print('Sentindo Briza')
            # print('Sentindo Cheiro')
            # print('Detectou Brilho')
            # print('Caiu no Buraco')
            # print('Detonado pelo Wumpus')
            # print('Ganhou o Tesouro)
            # pausar usando a funcao pause()
            # Avaliar visualmente a coerencia do resultado da ação
            # Digitar qualquer caracter para prosseguir jogando



if __name__ == '__main__':
    # Gera a semente para os numeros aleatorios
    GeraeEstabeleceSeed()

    # Tamanho da Matriz
    n = 10

    # Criar agente
    # agente = Agente(n)
    agente = Agente() # Default assume n = 4

    # Imprimir Dados do Jogo Wumpus
    print(agente)

    # Obter Posição Inicial do agente
    linha_agente, coluna_agente = agente.GetPosInicialAgente()
    print("Posicao Inicial do Agente:")
    print("linha_agente = %d" %(linha_agente))
    print("coluna_agente = %d\n" % (coluna_agente))

    # Obter Matriz de Códigos inteiros
    WM = agente.GetWM()
    print("Matriz Wumpus Códigos Inteiros WM:")
    print(WM)
    print("\n")

    # Obter Matriz de Labels
    WS = agente.GetWS()
    print("Matriz Wumpus de Strings WS:")
    print(WS)

    # Plotar Matriz - só aceita n = 4
    PlotarMatriz(WS)