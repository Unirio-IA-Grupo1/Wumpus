# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kREke8ldOyp2ai6MhSxGoG-Lh7u87RYe
"""

import random

# Tamanho do tabuleiro
board_size = 10

# Posição inicial do agente
agent_position = (0, 0)

# Posição do ouro
gold_position = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))

# Posição do Wumpus
wumpus_position = (random.randint(0, board_size - 1), random.randint(0, board_size - 1))

# Posições dos buracos
num_holes = 5
hole_positions = [(random.randint(0, board_size - 1), random.randint(0, board_size - 1)) for _ in range(num_holes)]

# Função para verificar se uma posição é válida no tabuleiro
def is_valid_position(position):
    x, y = position
    return 0 <= x < board_size and 0 <= y < board_size

# Função para realizar uma busca em profundidade no tabuleiro
def depth_first_search(start_position, target_position, visited):
    stack = [(start_position, [])]

    while stack:
        current_position, path = stack.pop()
        visited.add(current_position)

        if current_position == target_position:
            return path

        neighbors = [(current_position[0] - 1, current_position[1]),
                     (current_position[0] + 1, current_position[1]),
                     (current_position[0], current_position[1] - 1),
                     (current_position[0], current_position[1] + 1)]

        for neighbor in neighbors:
            if is_valid_position(neighbor) and neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

# Função para imprimir o tabuleiro
def print_board():
    for row in range(board_size):
        for col in range(board_size):
            if (row, col) == agent_position:
                print("A ", end='')
            elif (row, col) == gold_position:
                print("O ", end='')
            elif (row, col) == wumpus_position:
                print("W ", end='')
            elif (row, col) in hole_positions:
                print("H ", end='')
            else:
                print(". ", end='')
        print()

# Loop principal do jogo
visited = set()
while True:
    # Imprimir o tabuleiro
    print_board()

    # Verificar se o agente ganhou
    if agent_position == gold_position:
        print("Parabéns! O agente encontrou o ouro!")
        break

    # Verificar se o agente perdeu
    if agent_position == wumpus_position:
        print("O agente foi pego pelo Wumpus! Game over.")
        break

    if agent_position in hole_positions:
        print("O agente caiu em um buraco! Game over.")
        break

    # Fazer o agente escolher o próximo movimento usando busca em profundidade
    path_to_gold = depth_first_search(agent_position, gold_position, visited)

    if path_to_gold:
        next_move = path_to_gold[0]
    else:
        # Se não houver caminho para o ouro, escolher uma ação aleatória
        possible_moves = [(agent_position[0] - 1, agent_position[1]),
                          (agent_position[0] + 1, agent_position[1]),
                          (agent_position[0], agent_position[1] - 1),
                          (agent_position[0], agent_position[1] + 1)]
        possible_moves = [move for move in possible_moves if is_valid_position(move)]
        next_move = random.choice(possible_moves)

    # Atualizar a posição do agente
    agent_position = next_move

    # Mostrar o movimento do agente
    print(f"O agente se moveu para a posição {agent_position}")