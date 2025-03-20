import random
import pygame

from code.const import *

class Comida:
    def __init__(self, cobra):
        # Carrega e redimensiona a imagem da maçã para o tamanho do bloco
        imagem_maca = pygame.image.load('assets/maca.png')
        self.imagem = pygame.transform.scale(imagem_maca, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.posicao = self.gerar_posicao(cobra)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.posicao)

    def gerar_posicao(self, cobra):
        """
        Gera uma nova posição aleatória para a comida que não está ocupada pela cobra.
        
        Args:
            cobra: Instância da classe Cobrinha para verificar posições ocupadas
            
        Returns:
            tuple: Posição (x, y) da nova comida
        """
        while True:
            # Garante que a posição esteja alinhada com a grade
            colunas = (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO
            linhas = (ALTURA - MARGEM_SUPERIOR - TAMANHO_BLOCO) // TAMANHO_BLOCO
            
            x = random.randint(0, colunas) * TAMANHO_BLOCO
            y = random.randint(0, linhas) * TAMANHO_BLOCO + MARGEM_SUPERIOR
            
            posicao = (x, y)
            # Verifica se a posição não está ocupada pela cobra
            if posicao not in cobra.posicao:
                return posicao 