import random
import sys
import asyncio
from idlelib import debugger

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer
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

        # Determina o estado do jogo
        self.jogo_acabou = False

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
        self.label_size = 2.5 # cm 1.5 para 2.5
        self.pixels_label = int(self.label_size*self.pixels_per_cm)
        # tamanho e posicao da tela
        self.screen_horiz_size = 29.7 # cm
        self.pixels_screen_horiz_size = int(self.screen_horiz_size * self.pixels_per_cm)
        self.screen_vert_size = 26.0 # cm 21 para 26
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
        self.pixels_x_estado_alerta_size = 200
        self.pixels_y_estado_alerta_size = 50

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
        self.top_margin = int(4 * self.pixels_per_cm) # 4cm
        self.right_margin = int(2.5 * self.pixels_per_cm) # 2.5 cm
        self.bottom_margin = int(1.0 * self.pixels_per_cm) # de 2,5 para 1.0 cm

        # imagens png
        self.image_wumpus = 'wumpus.png'

        # Apresentar Tela
        self.setWindowTitle('Wumpus Game')
        self.setWindowIcon(QIcon(self.image_wumpus))
        self.setGeometry(150, 150, self.pixels_screen_horiz_size, self.pixels_screen_vert_size)
        # self.setFixedWidth(self.pixels_screen_horiz_size)
        # self.setFixedHeight(self.pixels_screen_vert_size)

        # Controle de modo: Teste ou Normal
        self.teste = False

        # Cria botão de chaveamento entre os modos Normal e Teste
        self.botao_normal_teste = QPushButton('Normal=>Teste', self)
        self.botao_normal_teste.resize(self.pixels_x_button_size+60, self.pixels_y_button_size)
        self.botao_normal_teste.move(self.pixels_x_up_arrow_coords-50, self.pixels_y_up_arrow_coords + 180)
        self.botao_normal_teste.clicked.connect(self._NormalTeste)

        # Cria botão de chaveamento entre os modos Normal e Teste
        self.jogar_automatico = QPushButton('Jogar automaticamente', self)
        self.jogar_automatico.resize(self.pixels_x_button_size + 60, self.pixels_y_button_size)
        self.jogar_automatico.move(self.pixels_x_up_arrow_coords - 50, self.pixels_y_up_arrow_coords + 280)
        self.jogar_automatico.clicked.connect(self._JogarAutomatico)


        # Inserindo um bloco de elemetos
        self.Interface_Botoes()

        self.grid_layout = QGridLayout(self)

        # Inserindo matriz de labels
        self.Interface_Matriz_Labels()

        # Inserindo Labels de Estado e Alerta
        self.label_conteudo_alerta = self.Interface_Labels_Estado_Alerta()

        self.show()

    # Trata chaveamento do modo normal para modo teste e vice-versa
    def _NormalTeste(self):
        if not self.teste:
          self.botao_normal_teste.setText("Teste => Normal")
          self.teste = True
        else:
          self.botao_normal_teste.setText("Normal => Teste")
          self.teste = False

        self._DeleteGridLabelMatrix()
        self._DeleteGridLabel()
        self.Interface_Matriz_Labels()

    def _ValorCasa(self,casa):
        for valor in casa:
            print("Casa" + str(casa))
            if -1 in valor:
                return -10
            if 2 in valor or 6 in valor:
                return -1000
            if 3 in valor or 4 in valor:
                return -10
            if 7 in valor:
                return 10
            if 5 in valor:
                return 1000
            else:
                return 0

    def _umaJogada(self):
        MO, listaOp = self.agente._Construir_Matriz_Opcoes_Jogadas()

        melhorCasa = [4,-20]

        jogadasInuteis = [1,4,11,14]

        cont = 0

        for linha in MO:
            for elemento in linha:
                # print("elemento " + str(elemento))
                if self._ValorCasa(elemento) > melhorCasa[1] and (not cont in jogadasInuteis):
                    melhorCasa = [cont,self._ValorCasa(elemento)]
                cont += 1

        print("Melhor casa pos " + str(melhorCasa[0]) + " Melhor casa val " + str(melhorCasa[1]))


        self._Jogada(melhorCasa[0])

    def _Jogada(self,melhorCasa):
        print("Melhor jogada " + str(melhorCasa))

        if melhorCasa == 0:
            self.Direita()
            self.Direita()
        elif melhorCasa == 2:
            self.Direita()
            self.PraCima()
        elif melhorCasa == 3:
            self.Direita()
            self.PraBaixo()

        elif melhorCasa == 5:
            self.Esquerda()
            self.Esquerda()
        elif melhorCasa == 6:
            self.Esquerda()
            self.PraCima()
        elif melhorCasa == 7:
            self.Esquerda()
            self.PraBaixo()

        elif melhorCasa == 8:
            self.PraCima()
            self.Direita()
        elif melhorCasa == 9:
            self.PraCima()
            self.Esquerda()
        elif melhorCasa == 10:
            self.PraCima()
            self.PraCima()

        elif melhorCasa == 12:
            self.PraBaixo()
            self.Direita()
        elif melhorCasa == 13:
            self.PraBaixo()
            self.Esquerda()
        elif melhorCasa == 15:
            self.PraBaixo()
            self.PraBaixo()

    def _JogarAutomatico(self):
        if not self.jogo_acabou and not self.coluna_agente == self.n - 1:
            self.jogar_automatico.setEnabled(False)
            self._umaJogada()
            print("Jogada Automática")
            QTimer.singleShot(2000, self._JogarAutomatico)  # Espera 1 segundo antes da próxima jogada automática
        else:
            self.jogar_automatico.setEnabled(True)  # Reativa o botão após o jogo automático terminar

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
        '''
        label_estado = QLabel('<b>Estado</b>', self)
        label_estado.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_estado.move(self.pixels_x_estado_coords, self.pixels_y_estado_coords)
        label_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)


        label_conteudo_estado = QLabel('Vazio', self)
        label_conteudo_estado.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_conteudo_estado.move(self.pixels_x_conteudo_estado_coords, self.pixels_y_conteudo_estado_coords)
        label_conteudo_estado.setStyleSheet("border: 1px solid black;")
        '''

        label_alerta = QLabel('<b>Alerta</b>', self)
        label_alerta.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_alerta.move(self.pixels_x_alerta_coords, self.pixels_y_alerta_coords)
        label_alerta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_conteudo_alerta = QLabel("Inicio de Jogo", self)
        label_conteudo_alerta.resize(self.pixels_x_estado_alerta_size, self.pixels_y_estado_alerta_size)
        label_conteudo_alerta.move(self.pixels_x_conteudo_alerta_coords, self.pixels_y_conteudo_alerta_coords)
        label_conteudo_alerta.setStyleSheet("border: 1px solid black;")

        return label_conteudo_alerta

    def _Elimina_Redundancia_Lista_String(self, input_list):
        # Create an empty set to store unique strings
        unique_strings = set()

        # Create a new list to store the result
        result_list = []

        # Iterate through the input list
        for string in input_list:
            # If the string is not in the set of unique strings, add it to the result list
            if string not in unique_strings and string != "Vazio":
                result_list.append(string)
                unique_strings.add(string)

        return result_list

    def Interface_Matriz_Labels(self):

        self.grid_layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)

        # Create a 10x10 matrix of labels
        for row in range(10):
            for col in range(10):


                # Join the list of strings with line breaks using <br> tag
                if self.teste:
                   formatted_text = "<br>".join(self._Elimina_Redundancia_Lista_String(self.WS[row][col]))  # Note the change in indexing
                else:
                   formatted_text = "<br>".join([" "])

                # Create a QLabel and set the HTML-formatted text
                self.grid_layout.label = QLabel(formatted_text)

                # Set QLabel to display text as HTML
                self.grid_layout.label.setOpenExternalLinks(True)

                # Set the border style
                if row == self.linha_agente  and col == self.coluna_agente:
                    self.grid_layout.label.setStyleSheet("border: 2px solid black;")
                else:
                    self.grid_layout.label.setStyleSheet("border: 1px solid black;")

                self.grid_layout.addWidget(self.grid_layout.label, row, col)

        self._EscreveLabel()

    def _DeleteGridLabel(self):
        # Remove the label from the grid layout
        label_to_delete = self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente)
        if label_to_delete is not None:
            widget = label_to_delete.widget()
            if widget:
                self.grid_layout.removeWidget(widget)
                widget.deleteLater()

    def _DeleteGridLabelMatrix(self):
        # Iterate through rows and columns of the grid layout
        for row in range(self.grid_layout.rowCount()):
            for col in range(self.grid_layout.columnCount()):
                label_to_remove = self.grid_layout.itemAtPosition(row, col)
                if label_to_remove:
                    # Remove and delete the label widget
                    label_widget = label_to_remove.widget()
                    label_widget.deleteLater()

    # Elimina redundancia de Strings na lista de Strings
    # a ser mostrada nos Labels da Matriz Wumpus
    def _EscreveLabel(self):
        self. _DeleteGridLabel()
        # Join the list of strings with line breaks using <br> tag
        formatted_text = "<br>".join(self._Elimina_Redundancia_Lista_String(self.WS[self.linha_agente][self.coluna_agente]))  # Note the change in indexing
        # Create a QLabel and set the HTML-formatted text
        new_label = QLabel(formatted_text)

        # Add the new QLabel to the QGridLayout at the specified position
        self.grid_layout.addWidget(new_label, self.linha_agente, self.coluna_agente)
        self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente).widget().setStyleSheet("border: 2px solid black;")

    def _ApagaLabel(self):
        self._DeleteGridLabel()

        # Create a new QLabel with an empty text
        new_label = QLabel(f" ")


        # Add the new QLabel to the QGridLayout at the specified position
        self.grid_layout.addWidget(new_label, self.linha_agente, self.coluna_agente)
        self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente).widget().setStyleSheet(
            "border: 1px solid black;")
    def Reset(self):
        self.agente.Reset()
        # Obter Posição Inicial do agente
        self.linha_agente, self.coluna_agente = self.agente.GetPosInicialAgente()
        print("Posicao Inicial do Agente:")
        print("linha_agente = %d" % (self.linha_agente))
        print("coluna_agente = %d\n" % (self.coluna_agente))
        # Obter Matriz de Códigos inteiros
        self.WM = self.agente.GetWM()
        print("Nova Matriz Wumpus Códigos Inteiros WM:")
        print(self.WM)
        print("\n")
        self.label_conteudo_alerta.setText("Jogo Iniciou!")

        # Obter Matriz de Labels
        self.WS = self.agente.GetWS()
        print("Nova Matriz Wumpus de Strings WS:")
        print(self.WS)
        self._DeleteGridLabelMatrix()
        self._DeleteGridLabel()
        self.Interface_Matriz_Labels()
        self.jogo_acabou = False

    def PraCima(self):
        print('Pra Cima')
        if self.linha_agente == 0:
            print('Limite')
            self.label_conteudo_alerta.setText("Chegou no Limite")
        elif self.jogo_acabou:
            self._MensagemFimJogo()
        else:
            self.label_conteudo_alerta.setText("Andou Pra Cima")
            self._ApagaLabel()
            self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente).widget().setStyleSheet("border: 1px solid black;")
            self.linha_agente -= 1
            self.WM[self.linha_agente, self.coluna_agente].append(1)
            self.WS[self.linha_agente, self.coluna_agente].append("Agente")
            self._EscreveLabel()
            self.agente.SetPosicaoAgente(self.linha_agente, self.coluna_agente)
            self._VerificarFimJogo()


    def PraBaixo(self):
        print('Pra Baixo')
        if self.linha_agente == self.n-1:
            print('Limite')
            self.label_conteudo_alerta.setText("Chegou no Limite")
        elif self.jogo_acabou:
            self._MensagemFimJogo()
        else:
            self.label_conteudo_alerta.setText("Andou Pra Baixo")
            self._ApagaLabel()
            self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente).widget().setStyleSheet("border: 1px solid black;")
            self.linha_agente += 1
            self.WM[self.linha_agente, self.coluna_agente].append(1)
            self.WS[self.linha_agente, self.coluna_agente].append("Agente")
            self._EscreveLabel()
            self.agente.SetPosicaoAgente(self.linha_agente, self.coluna_agente)
            self._VerificarFimJogo()

    def Direita(self):
        print('Direita')
        if self.coluna_agente == self.n-1:
            print('Limite')
            self.label_conteudo_alerta.setText("Chegou no Limite")
        elif self.jogo_acabou:
            self._MensagemFimJogo()
        else:
            self.label_conteudo_alerta.setText("Andou Pra Direita")
            self._ApagaLabel()
            self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente).widget().setStyleSheet("border: 1px solid black;")
            self.coluna_agente += 1
            self.WM[self.linha_agente, self.coluna_agente].append(1)
            self.WS[self.linha_agente, self.coluna_agente].append("Agente")
            self._EscreveLabel()
            self.agente.SetPosicaoAgente(self.linha_agente, self.coluna_agente)
            self._VerificarFimJogo()

    def Esquerda(self):
        print('Esquerda')
        if self.coluna_agente == 0:
            print('Limite')
            self.label_conteudo_alerta.setText("Chegou no Limite")
        elif self.jogo_acabou:
            self._MensagemFimJogo()
        else:
            self.label_conteudo_alerta.setText("Andou Pra Esquerda")
            self._ApagaLabel()
            self.grid_layout.itemAtPosition(self.linha_agente, self.coluna_agente).widget().setStyleSheet("border: 1px solid black;")
            self.coluna_agente -= 1
            self.WM[self.linha_agente, self.coluna_agente].append(1)
            self.WS[self.linha_agente, self.coluna_agente].append("Agente")
            self._EscreveLabel()
            self.agente.SetPosicaoAgente(self.linha_agente, self.coluna_agente)
            self._VerificarFimJogo()

    def _VerificarFimJogo(self):
        casasDerrota = [2,6]
        casaVitoria = 5
        if any(item in self.WM[self.linha_agente, self.coluna_agente] for item in casasDerrota):
            print("Acabou!")
            self.label_conteudo_alerta.setText("Oh não! Você perdeu :(")
            self.jogo_acabou = True
        if casaVitoria in self.WM[self.linha_agente, self.coluna_agente]:
            print("Acabou!")
            self.label_conteudo_alerta.setText("Parabéns! \nVocê Venceu! :)")
            self.jogo_acabou = True

    def _MensagemFimJogo(self):
        print("O jogo acabou,\n aperte o botão reset para reiniciar")
        self.label_conteudo_alerta.setText("O jogo acabou!\nAperte o botão Reset para reiniciar")

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    app = QtWumpus()
    sys.exit(qt.exec())
