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
    def __init__(self, n = 4, percent_pits = 15 , visibilidade = 2):
        # Propriedades
        self.n = n
        self.percent_pits = percent_pits
        self.visibilidade = visibilidade
        self.npits = int(self.n * self.n * self.percent_pits / 100)
        self.nwumpus = 1
        self.nouro = 1
        self.nagente = 1
        # Dicionarios
        self.dict_agent = {'Vazio': 0, 'Agente': 1, 'Wumpus': 2, 'Brisa': 3, 'Cheiro': 4, 'Ouro': 5, 'Buraco': 6,
                      'Brilho': 7}
        self.reverse_dict_agent = {value: key for key, value in self.dict_agent.items()}
        self.dict_move = {0: 'Direita', 1: 'Esquerda', 2: 'PraCima', 3: 'PraBaixo'}
        self.dict_nobjs = {'Agente': self.nagente, 'Buraco': self.npits, 'Wumpus': self.nwumpus, 'Ouro': self.nouro}
        self.dict_efeitos = {'Wumpus': 'Cheiro', 'Buraco': 'Brisa', 'Ouro': 'Brilho'}
        # Matrizes de Listas e posicao inicial do agente
        self.WM, self.WS, self.linha_agente, self.coluna_agente = self._GeraMatrizes_Posicao_Inicial_Agente()
        self.MO = []

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

    def _Gerar_Matriz_Opcoes(self):
        nopcoes = len(self.dict_move)
        matrix = np.zeros((nopcoes, nopcoes), dtype=object)
        for i in range(nopcoes):
            for j in range(nopcoes):
                matrix[i, j] = [[-1]]
        return matrix

    # Preenche células da Matrix com agente, Buraco, Wumpus e Ouro
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

    def SetPosicaoAgente(self, linha_agente, coluna_agente):
        self.linha_agente = linha_agente
        self.coluna_agente = coluna_agente

    # Responde ao botao Reset
    def Reset(self):
        self.WM, self.WS, self.linha_agente, self.coluna_agente = self._GeraMatrizes_Posicao_Inicial_Agente()
        # Alterar Tela

    def ObterPosicaoJogada(self, jogada, linha, coluna):
        # Direita
        if (jogada == 0):
            if (coluna != self.n-1):
                coluna += 1
        # Esquerda
        elif (jogada == 1):
            if (coluna != 0):
                coluna -= 1
        # Pra Cima
        elif (jogada == 2):
            if (linha != 0):
                linha -= 1
        # Pra Baixo
        elif (jogada == 3):
            if (linha != self.n-1):
                linha += 1

        return linha, coluna

    def _FoiPossivelaJogada(self, linha, coluna, linha_jogada, coluna_jogada):
        if ( linha == linha_jogada) and(coluna == coluna_jogada):
            return False
        else:
            return True


    def _Construir_Matriz_Opcoes_Jogadas(self):

        Matriz_Opcoes = self._Gerar_Matriz_Opcoes()
        # print(Matriz_Opcoes)

        linha = self.linha_agente
        coluna = self.coluna_agente
        print('_Construir_Matriz_Opcoes_Jogadas: posicao inicial')
        print(linha)
        print(coluna)

        lista_pos = []

        for key in self.dict_move.keys():

          jogada = key
          linha_jogada, coluna_jogada = self.ObterPosicaoJogada(jogada, linha, coluna)
          lista_pos.append((linha_jogada, coluna_jogada))


          for j in range(len(self.dict_move)):
            if (Matriz_Opcoes[jogada, j][0] == [-1]):
              if (self._FoiPossivelaJogada(linha, coluna, linha_jogada, coluna_jogada)):
                '''
                print('Antes de Atualizar Matriz Opcoes')
                print(linha)
                print(coluna)
                print(linha_jogada)
                print(coluna_jogada)
                '''

                Matriz_Opcoes[jogada, j][0] = self.WM[linha_jogada, coluna_jogada]

        # print('Matriz uma Jogada')
        # print(Matriz_Opcoes)
        Matriz_Opcoes = self._Pos_processar_Matriz_Opcoes(Matriz_Opcoes, lista_pos)
        self.MO = Matriz_Opcoes
        return Matriz_Opcoes, lista_pos


    def _Pos_processar_Matriz_Opcoes(self, Matriz_Opcoes, lista_pos):

        for i in range(len(lista_pos)):
            linha = lista_pos[i][0]
            coluna = lista_pos[i][1]

            for key in self.dict_move.keys():
                linha_jogada, coluna_jogada = self.ObterPosicaoJogada(key, linha, coluna)
                if (self._FoiPossivelaJogada(linha, coluna, linha_jogada, coluna_jogada)):
                  Matriz_Opcoes[key, i].append(self.WM[linha_jogada, coluna_jogada])
                else:
                  Matriz_Opcoes[key, i].append([-1])

        return Matriz_Opcoes

    def find_max_indices(self, input_list):
        if not input_list:
            return None, []

        max_value = max(input_list)
        max_indices = [index for index, value in enumerate(input_list) if value == max_value]

        return max_value, max_indices

    def Jogar(self, jogada):
        # Direita
        if (jogada == 0):
            if self.coluna_agente != self.n-1:
              self.coluna_agente += 1
        # Esquerda
        elif (jogada == 1):
            if self.coluna_agente != 0:
              self.coluna_agente -= 1
        # Pra Cima
        elif (jogada == 2):
            if self.linha_agente != 0:
              self.linha_agente -= 1
        # Prabaixo
        elif (jogada == 3):
            if self.linha_agente != self.n-1:
              self.linha_agente += 1

        self.MO, LP = self._Construir_Matriz_Opcoes_Jogadas()


    def SimularJogo(self):
        seqjogadas = []
        # PlotarMatriz(self.WS)
        njogadas = 20
        for count in range(njogadas):
            self.MO, lista_pos = self._Construir_Matriz_Opcoes_Jogadas()
            #print('Matriz 2 Jogadas')
            #print(self.MO)
            paresestadosjogadas, listajogadas = self.ObterParesJogadas()
            npossiveisjogadas = len(paresestadosjogadas)
            notas = []
            for indice in range(npossiveisjogadas):
                notas.append(self.ObterNota(paresestadosjogadas[indice][0], paresestadosjogadas[indice][1]))
                '''
                if (self.ObterNota(paresestadosjogadas[indice][0], paresestadosjogadas[indice][1]) ==  None):
                    print('indice = %d' %(indice))
                    print(paresestadosjogadas[indice])
                '''

            print(notas)
            print(max(notas))
            max_value, max_indices = self.find_max_indices(notas)
            print(max_value)
            print(max_indices)
            nsorteio = len(max_indices)
            indsorteio = np.random.randint(0, nsorteio)
            print('nsorteio')
            print(nsorteio)
            print('indsorteio')
            print(indsorteio)
            jogada = listajogadas[max_indices[indsorteio]]
            print(jogada)
            seqjogadas.append(self.dict_move[jogada])
            print(seqjogadas)
            self.Jogar(jogada)
            print(self.reverse_dict_agent[paresestadosjogadas[max_indices[indsorteio]][0]])
            print(self.reverse_dict_agent[paresestadosjogadas[max_indices[indsorteio]][0]])
            print(max_value)
            if (max_value == 10) or (max_value == 1):
                print('Encerrar o Jogo')
                print(self.reverse_dict_agent[paresestadosjogadas[max_indices[indsorteio]][0]])
                break
                #pause()
                #self.Reset()

            pause()

    def ObterNota(self, estadoaposjogada1, estadoaposjogada2):
        Nota = 2
        # estado apos jogada 1 = "Ouro"
        if (estadoaposjogada1 == 5):
            Nota = 10
            return Nota
        # estado apos jogada 1 = "Brilho", estado apos jogada 2 = "Ouro"
        elif (estadoaposjogada1 == 7) and (estadoaposjogada2 == 5):
            Nota = 9
            return Nota
        # estado apos jogada 1 = "Vazio", estado apos jogada2 = Brilho
        elif (estadoaposjogada1 == 0) and (estadoaposjogada2 == 7):
            Nota = 8
            return Nota
        # estado apos jogada 1 = "Cheiro", estado apos jogada2 = "Brilho
        elif (estadoaposjogada1 == 4) and (estadoaposjogada2 == 7):
            Nota = 7
            return Nota
        # estado apos jogada 1 = "Brisa", estado apos jogada2 = "Brilho
        elif (estadoaposjogada1 == 3) and (estadoaposjogada2 == 7):
            Nota = 7
            return Nota
        # estado apos jogada 1 = "Vazio", estado apos jogada2 = "Vazio"
        elif (estadoaposjogada1 == 0) and (estadoaposjogada2 == 0):
            Nota = 6
            return Nota
        # estado apos jogada 1 = "Vazio", estado apos jogada2 = "Cheiro"
        elif (estadoaposjogada1 == 0) and (estadoaposjogada2 == 4):
            Nota = 5
            return Nota
        # estado apos jogada 1 = "Vazio", estado apos jogada2 = "Brisa"
        elif (estadoaposjogada1 == 0) and (estadoaposjogada2 == 3):
            Nota = 4
            return Nota
        # estado apos jogada 1 = "Brisa", estado apos jogada2 = "Cheiro"
        elif (estadoaposjogada1 == 3) and (estadoaposjogada2 == 4):
            Nota = 3
            return Nota
        # estado apos jogada 1 = "Cheiro", estado apos jogada2 = "Brisa"
        elif (estadoaposjogada1 == 4) and (estadoaposjogada2 == 3):
            Nota = 3
            return Nota
        # estado apos jogada 1 = "Brisa", estado apos jogada2 = "Buraco"
        elif (estadoaposjogada1 == 3) and (estadoaposjogada2 == 6):
            Nota = 2
            return Nota
        # estado apos jogada 1 = "Cheiro", estado apos jogada2 = "Wumpus"
        elif (estadoaposjogada1 == 3) and (estadoaposjogada2 == 2):
            Nota = 2
            return Nota
        # estado apos jogada 1 = "Buraco"
        elif (estadoaposjogada1 == 6):
            Nota = 1
            return Nota
        # estado apos jogada 1 = "Wumpus"
        elif (estadoaposjogada1 == 2):
            Nota = 1
            return Nota
        # estado apos jogada 1 = "Impossivel"
        elif (estadoaposjogada1 == -1):
            Nota = 0
            return Nota
        elif (estadoaposjogada2 == 1):
            return Nota
        else:
            return Nota

    def _ReduzemImportancia(self, listaestado):
        if -1  in listaestado:
            return [-1]
        if 6 in listaestado:
            return [6]
        if 2 in listaestado:
            return [2]
        if 5 in listaestado:
            return [5]
        if 3 in listaestado:
            return [3]
        if 4 in listaestado:
            return [4]
        if 7 in listaestado:
            return [7]
        if 0 in listaestado:
            return [0]
        if 1 in listaestado:
            return [1]


    def ObterParesJogadas(self):
      paresestadosjogadas = []
      listajogadas = []
      num = len(self.MO[0])
      for linha in range(num):
        for coluna in range(num):

            print(self.MO[linha][coluna][0])
            est1 = self._ReduzemImportancia(self.MO[linha][coluna][0])
            print('est1')
            print(est1)
            print(self.MO[linha][coluna][1])
            est2 =  self._ReduzemImportancia(self.MO[linha][coluna][1])
            print('est2')
            print(est2)
            for estjogada1 in est1:
                for estjogada2 in est2:
                    paresestadosjogadas.append([estjogada1, estjogada2])
                    listajogadas.append(linha)


      print(paresestadosjogadas)
      print(len(paresestadosjogadas))
      print(listajogadas)
      print(len(listajogadas))

      return paresestadosjogadas, listajogadas



if __name__ == '__main__':
    # Gera a semente para os numeros aleatorios
    # GeraeEstabeleceSeed()

    # Tamanho da Matriz
    n = 10

    # Criar agente
    # agente = Agente(n)
    agente = Agente(n) # Default assume n = 4

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
    # PlotarMatriz(WS)

    '''

    # Teste de Reset
    agente.Reset()

    # Obter Matriz de Labels
    WS = agente.GetWS()
    print("Matriz Wumpus de Strings WS:")
    print(WS)

    # Plotar Matriz - só aceita n = 4
    PlotarMatriz(WS)
    '''

    agente.SimularJogo()
