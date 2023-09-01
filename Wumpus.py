import numpy as np
import matplotlib.pyplot as plt
import time as tm

# Gera a semente para os numeros aleatorios
def GeraeEstabeleceSeed():
  timefloat = tm.time()
  print ('timefloat = %f' %(timefloat))
  timeround = round(timefloat)
  print ('timeround = %f' %(timeround))
  timeint = int(timeround)
  print ('timeint = %d' %(timeint))
  timeseed = timeint%10000
  print ('timeseed = %d' %(timeseed))
  np.random.seed(timeseed)
  return timeseed


# Gerada pelo ChatGPT - Fixa para 4 x 4
def PlotarMatriz(LM):

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


# Gera Matriz Wumpus Vazia
def Gerar_Matriz_Wumpus(n):
    matrix = np.zeros((n, n), dtype=object)
    for i in range(n):
        for j in range(n):
            matrix[i, j] = [0]
    return matrix

# Preenche células da Matrix com agente, Wumpus e Ouro
def Preencher_WM_Random(WM, dict_nobjs, dict_agent):
    limite_objetos = 20
    n = WM.shape[0]
    assert (np.sum([dict_nobjs[key] for key in dict_nobjs.keys()] ) < limite_objetos)
    for key in dict_nobjs.keys():
        count = 0
        for num in range(dict_nobjs[key]):
            Preenchido = False
            while (not Preenchido):
                linha = np.random.randint(0, n)
                coluna = np.random.randint(0, n)
                if WM[linha, coluna][0] == 0:
                    WM[linha, coluna][0] = dict_agent[key]
                    Preenchido = True
                    count = count + 1

    return WM

def Gerar_efeitos(WM, dict_efeitos, dict_agent):
    n = WM.shape[0]
    # print(n)
    # Percorrer o dicinário de efeitos
    for key in dict_efeitos.keys():
        #print(key)
      # Percorrer a Matriz Wumpus de listas
        for linha in range(n):
            for coluna in range(n):
                if any(dict_agent[key] == value for value in WM[linha][coluna]):
                    WM = Adicionar_efeito(WM, dict_efeitos[key], linha, coluna)
    return WM


def Adicionar_efeito_a_direita(WM, efeito, linha, coluna):
    #print('Adicionar_efeito_a_direita: WM')
    #print(WM)
    WM[linha][coluna+1].append(efeito)
    return WM

def Adicionar_efeito_a_esquerda(WM, efeito, linha, coluna):
    # print('Adicionar_efeito_a_esquerda: WM')
    #print(WM)
    WM[linha][coluna-1].append(efeito)
    return WM

def Adicionar_efeito_acima(WM, efeito, linha, coluna):
    # print('Adicionar_efeito_acima: WM')
    # print(WM)
    WM[linha-1][coluna].append(efeito)
    return WM

def Adicionar_efeito_abaixo(WM, efeito, linha, coluna):
    # print('Adicionar_efeito_abaixo: WM')
    # print(WM)
    WM[linha+1][coluna].append(efeito)
    return WM

def Adicionar_efeito(WM, efeito, linha, coluna):
    # print('Adicionar Efeito: WM')
    # print(WM)
    n = WM.shape[0]
    # print(efeito)
    if linha == 0:
        Adicionar_efeito_abaixo(WM, efeito, linha, coluna)
    elif linha == n-1:
        WM = Adicionar_efeito_acima(WM, efeito, linha, coluna)
    else:
        WM = Adicionar_efeito_abaixo(WM, efeito, linha, coluna)
        WM = Adicionar_efeito_acima(WM, efeito, linha, coluna)
    if  coluna == 0:
        WM = Adicionar_efeito_a_direita(WM, efeito, linha, coluna)
    elif coluna == n-1:
        WM = Adicionar_efeito_a_esquerda(WM, efeito, linha, coluna)
    else:
        WM = Adicionar_efeito_a_direita(WM, efeito, linha, coluna)
        WM = Adicionar_efeito_a_esquerda(WM, efeito, linha, coluna)
    return WM

# Transforma matriz em Matriz de Labels
def GetLabelsMatrix(LI, dict_codes):

    n = LI.shape[0]

    # Iterate through each row in the matrix of integer codes (LI)
    for row in range(n):
        for col in range(n):
            count = 0
            for code in LI[row][col]:
              if (isinstance(LI[row, col][count], int)):
                label = dict_codes[code]
                LI[row, col][count] = label
              count = count + 1

    return LI

if __name__ == '__main__':
    dict_agent = {'Vazio': 0, 'Agente': 1, 'Wumpus': 2, 'Brisa': 3, 'Cheiro': 4, 'Ouro': 5, 'Buraco': 6, 'Brilho': 7}
    reverse_dict_agent = {value: key for key, value in dict_agent.items()}
    dict_move  = {'Direita': 0, 'Esquerda': 1, 'PraCima': 2, 'Pra Baixo': 3}
    # n = 10
    n = 4
    percent_pits = 15
    npits = int(n*n*percent_pits/100)
    # print(npits)
    nwumpus = 1
    nouro = 1
    nagente = 1
    dict_nobjs = {'Agente': nagente, 'Buraco': npits, 'Wumpus': nwumpus, 'Ouro' : nouro}
    dict_efeitos = {'Wumpus': 'Cheiro', 'Buraco' : 'Brisa',  'Ouro' : 'Brilho' }

    # Gerar  Matriz Wumpus de listas vazias
    WM = Gerar_Matriz_Wumpus(n)
    #print('WM')
    #print(WM)

    # Preencher Agente, Buraco, Wumpus e Ouro
    WM = Preencher_WM_Random(WM, dict_nobjs, dict_agent)
    # print('WM Random')
    # print(WM)

    # Proximos passos - preencher brisa, cheiro e brilho
    WM = Gerar_efeitos(WM, dict_efeitos, dict_agent)
    # print('WM')
    # print(WM)

    # Transformar em Matriz de Labels Strings
    WS = GetLabelsMatrix(WM, reverse_dict_agent)
    print('WS')
    print(WS)

    PlotarMatriz(WS)







