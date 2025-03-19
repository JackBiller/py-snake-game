import pygame

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128)

# Configurações da tela
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 20
MARGEM_SUPERIOR = 40  # Espaço para pontuação e dificuldade
ALTURA_JOGAVEL = ALTURA - MARGEM_SUPERIOR  # Altura disponível para o jogo

# Índices dos sprites
RABO_LATERAL = 0
CABECA_BAIXO = 1
CORPO_CURVA_LADO_BAIXO = 2
CORPO_HORIZONTAL = 3
CABECA_ESQUERDA = 4
RABO_VERTICAL = 5
CORPO_VERTICAL = 6
SPRITE_SIZE = 42 

# Configurações da fonte
FONTE_NORMAL = 36
FONTE_GRANDE = 72 