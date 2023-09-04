import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import Agente as ag




class QtWumpus(QWidget):
    def __init__(self):
        super().__init__()

        # Gera a semente para os numeros aleatorios
        ag.GeraeEstabeleceSeed()

        # Tamanho da Matriz
        self.n = 10

        # Criar agente
        # agente = Agente(n)
        self.agente = ag.Agente(self.n)  # Default assume n = 4

        # Imprimir Dados do Jogo Wumpus
        print(self.agente)

        # Obter Posição Inicial do agente
        self.linha_agente, self.coluna_agente = self.agente.GetPosInicialAgente()
        print("Posicao Inicial do Agente:")
        print("linha_agente = %d" % (self.linha_agente))
        print("coluna_agente = %d\n" % (self.coluna_agente))

        # Obter Matriz de Códigos inteiros
        self.WM = self.agente.GetWM()
        print("Matriz Wumpus Códigos Inteiros WM:")
        print(self.WM)
        print("\n")

        # Obter Matriz de Labels
        self.WS = self.agente.GetWS()
        print("Matriz Wumpus de Strings WS:")
        print(self.WS)


        # tamanhos de buttons e labels
        self.pixels_per_cm = 36.85613777652585
        # tamanho dos labels da Matriz Wumpus
        self.label_size = 1.5 # cm
        self.pixels_label = int(self.label_size*self.pixels_per_cm)
        # tamanho e posicao da tela
        self.screen_horiz_size = 29.7 # cm
        self.pixels_screen_horiz_size = int(self.screen_horiz_size * self.pixels_per_cm)
        self.screen_vert_size = 21.0 # cm
        self.pixels_screen_vert_size = int(self.screen_vert_size * self.pixels_per_cm)
        # tamanho dos botoes
        self.x_button_size = 2.0  # cm
        self.pixels_x_button_size = int(self.x_button_size * self.pixels_per_cm)
        self.y_button_size = 1.0  # cm
        self.pixels_y_button_size = int(self.y_button_size * self.pixels_per_cm)
        # posicao do botao pra cima
        self.x_up_arrow_coords = 3.0 # cm
        self.pixels_x_up_arrow_coords = int(self.x_up_arrow_coords * self.pixels_per_cm)
        self.y_up_arrow_coords = 8.5  # cm
        self.pixels_y_up_arrow_coords = int(self.y_up_arrow_coords * self.pixels_per_cm)

        # posicao do botao reset
        self.pixels_x_reset_coords = self.pixels_x_up_arrow_coords
        self.pixels_y_reset_coords = self.pixels_y_up_arrow_coords + self.pixels_y_button_size

        # posicao do botao pra baixo
        self.pixels_x_prabaixo_coords = self.pixels_x_up_arrow_coords
        self.pixels_y_prabaixo_coords = self.pixels_y_reset_coords + self.pixels_y_button_size

        # posicao do botao esquerda
        self.pixels_x_esquerda_coords = self.pixels_x_up_arrow_coords - self.pixels_x_button_size
        self.pixels_y_esquerda_coords = self.pixels_y_reset_coords

        # posicao do botao direita
        self.pixels_x_direita_coords = self.pixels_x_up_arrow_coords + self.pixels_x_button_size
        self.pixels_y_direita_coords = self.pixels_y_reset_coords

        # posicao do labels de estado
        self.x_estado_coords = 13.0  # cm
        self.pixels_x_estado_coords = int(self.x_estado_coords * self.pixels_per_cm)
        self.y_estado_coords = 1.0 # cm
        self.pixels_y_estado_coords = int(self.y_estado_coords * self.pixels_per_cm)

        # tamanho labels de estado e alerta
        self.pixels_x_estado_alerta_size = self.pixels_x_button_size
        self.pixels_y_estado_alerta_size = self.pixels_y_button_size

        # posicao do labels de conteudo do estado
        self.x_conteudo_estado_coords =  self.x_estado_coords  # cm
        self.pixels_x_conteudo_estado_coords = int(self.x_conteudo_estado_coords * self.pixels_per_cm)
        self.y_conteudo_estado_coords = self.y_estado_coords + self.y_button_size
        self.pixels_y_conteudo_estado_coords = int(self.y_conteudo_estado_coords * self.pixels_per_cm)

        # posicao do labels de alerta
        self.x_alerta_coords = 17.0  # cm
        self.pixels_x_alerta_coords = int(self.x_alerta_coords * self.pixels_per_cm)
        self.y_alerta_coords = 1.0  # cm
        self.pixels_y_alerta_coords = int(self.y_alerta_coords * self.pixels_per_cm)

        # posicao do labels de conteudo do alerta
        self.x_conteudo_alerta_coords = self.x_alerta_coords  # cm
        self.pixels_x_conteudo_alerta_coords = int(self.x_conteudo_alerta_coords * self.pixels_per_cm)
        self.y_conteudo_alerta_coords = self.y_alerta_coords + self.y_button_size
        self.pixels_y_conteudo_alerta_coords = int(self.y_conteudo_alerta_coords * self.pixels_per_cm)



        # margens da matriz de Labels Wumpus
        self.left_margin = int(9 * self.pixels_per_cm) # 7 cm
        self.top_margin = int(4 * self.pixels_per_cm) # 4 cm
        self.right_margin = int(2.5 * self.pixels_per_cm) # 2.5 cm
        self.bottom_margin = int(2.5 * self.pixels_per_cm) # 2.5

        # imagens png
        self.image_wumpus = 'wumpus.png'

        # Apresentar Tela
        self.setWindowTitle('Wumpus Game')
        self.setWindowIcon(QIcon(self.image_wumpus))
        self.setGeometry(150, 150, self.pixels_screen_horiz_size, self.pixels_screen_vert_size)
        self.setFixedWidth(self.pixels_screen_horiz_size)
        self.setFixedHeight(self.pixels_screen_vert_size)

        # Inserindo um bloco de elemetos
        self.Interface_Botoes()

        self.grid_layout = QGridLayout(self)

        # Inserindo matriz de labels
        self.Interface_Matriz_Labels()

        # Inserindo Labels de Estado e Alerta
        self.Interface_Labels_Estado_Alerta()


        self.show()



    def Interface_Botoes(self):
        botao_pracima = QPushButton('PraCima', self)
        botao_pracima.resize(self.pixels_x_button_size, self.pixels_y_button_size)
        botao_pracima.move(self.pixels_x_up_arrow_coords, self.pixels_y_up_arrow_coords)
        botao_pracima.clicked.connect(self.PraCima)

        botao_reset = QPushButton('Reset', self)
        botao_reset.resize(self.pixels_x_button_size, self.pixels_y_button_size)
        botao_reset.move(self.pixels_x_reset_coords, self.pixels_y_reset_coords)
        botao_reset.clicked.connect(self.Reset)

        botao_prabaixo = QPushButton('Pra Baixo', self)
        botao_prabaixo.resize(self.pixels_x_button_size, self.pixels_y_button_size)
        botao_prabaixo.move(self.pixels_x_prabaixo_coords, self.pixels_y_prabaixo_coords)
        botao_prabaixo.clicked.connect(self.PraBaixo)

        botao_esquerda = QPushButton('Esquerda', self)
        botao_esquerda.resize(self.pixels_x_button_size, self.pixels_y_button_size)
        botao_esquerda.move(self.pixels_x_esquerda_coords, self.pixels_y_esquerda_coords)
        botao_esquerda.clicked.connect(self.Esquerda)

        botao_direita = QPushButton('Direita', self)
        botao_direita.resize(self.pixels_x_button_size, self.pixels_y_button_size)
        botao_direita.move(self.pixels_x_direita_coords, self.pixels_y_direita_coords)
        botao_direita.clicked.connect(self.Direita)

    def Interface_Labels_Estado_Alerta(self):

        label_estado = QLabel('<b>Estado</b>', self)
        label_estado.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_estado.move(self.pixels_x_estado_coords, self.pixels_y_estado_coords)
        label_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)


        label_conteudo_estado = QLabel('Vazio', self)
        label_conteudo_estado.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_conteudo_estado.move(self.pixels_x_conteudo_estado_coords, self.pixels_y_conteudo_estado_coords)
        label_conteudo_estado.setStyleSheet("border: 1px solid black;")

        label_alerta = QLabel('<b>Alerta</b>', self)
        label_alerta.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_alerta.move(self.pixels_x_alerta_coords, self.pixels_y_alerta_coords)
        label_alerta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_conteudo_alerta = QLabel('Limite', self)
        label_conteudo_alerta.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_conteudo_alerta.move(self.pixels_x_conteudo_alerta_coords, self.pixels_y_conteudo_alerta_coords)
        label_conteudo_alerta.setStyleSheet("border: 1px solid black;")


    def Interface_Matriz_Labels(self):
        # grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)

        # Create a 10x10 matrix of labels
        for row in range(10):
            for col in range(10):
                # label = QLabel(f"Label {row + 1}-{col + 1}")
                self.grid_layout.label = QLabel(f" ")

                # Set the border style

                if row == self.linha_agente  and col == self.coluna_agente:
                    self.grid_layout.label.setStyleSheet("border: 2px solid black;")
                else:
                    self.grid_layout.label.setStyleSheet("border: 1px solid black;")

                self.grid_layout.addWidget(self.grid_layout.label, row, col)

    def _DeleteGridLabel(self):
        # Remove the label from the grid layout
        label_to_delete = self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente)
        if label_to_delete is not None:
            widget = label_to_delete.widget()
            if widget:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

    def Reset(self):
        print('Reset')

    def PraCima(self):
        print('Pra Cima')
        if self.linha_agente == 0:
          print('Limite')
        else:
          self.linha_agente -= 1
          if (self.WM[self.linha_agente, self.coluna_agente] == list([-1])):
              print('Limite')
              self.linha_agente += 1
          else:
              self.linha_agente += 1
              self._DeleteGridLabel()
              self.WM[self.linha_agente, self.coluna_agente] = list([-1])
              self.linha_agente -= 1
              self._DeleteGridLabel()
              self.grid_layout.label = QLabel(f" ")
              self.grid_layout.label.setStyleSheet("border: 2px solid black;")
              self.grid_layout.addWidget(self.grid_layout.label, self.linha_agente, self.coluna_agente)


    def PraBaixo(self):
        print('Pra Baixo')
        if self.linha_agente == self.n-1:
          print('Limite')
        else:
          self.linha_agente += 1
          if (self.WM[self.linha_agente, self.coluna_agente] == list([-1])):
              print('Limite')
              self.linha_agente -= 1
          else:
              self.linha_agente -= 1
              self._DeleteGridLabel()
              self.WM[self.linha_agente, self.coluna_agente] = list([-1])
              self.linha_agente += 1
              self._DeleteGridLabel()
              self.grid_layout.label = QLabel(f" ")
              self.grid_layout.label.setStyleSheet("border: 2px solid black;")
              self.grid_layout.addWidget(self.grid_layout.label, self.linha_agente, self.coluna_agente)

    def Direita(self):
        print('Direita')
        if self.coluna_agente == self.n-1:
            print('Limite')
        else:
            self.coluna_agente += 1
            if (self.WM[self.linha_agente, self.coluna_agente] == list([-1])):
                print('Limite')
                self.coluna_agente -= 1
            else:
                self.coluna_agente -= 1
                self._DeleteGridLabel()
                self.WM[self.linha_agente, self.coluna_agente] = list([-1])
                self.coluna_agente += 1
                self._DeleteGridLabel()
                self.grid_layout.label = QLabel(f" ")
                self.grid_layout.label.setStyleSheet("border: 2px solid black;")
                self.grid_layout.addWidget(self.grid_layout.label, self.linha_agente, self.coluna_agente)


    def Esquerda(self):
        print('Esquerda')
        if self.coluna_agente == 0:
            print('Limite')
        else:
            self.coluna_agente -= 1
            if (self.WM[self.linha_agente, self.coluna_agente] == list([-1])):
                print('Limite')
                self.coluna_agente += 1
            else:
                self.coluna_agente += 1
                self._DeleteGridLabel()
                self.WM[self.linha_agente, self.coluna_agente] = list([-1])
                self.coluna_agente -= 1
                self._DeleteGridLabel()
                self.grid_layout.label = QLabel(f" ")
                self.grid_layout.label.setStyleSheet("border: 2px solid black;")
                self.grid_layout.addWidget(self.grid_layout.label, self.linha_agente, self.coluna_agente)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = QtWumpus()
    sys.exit(qt.exec())

