import random
import pygame

from code.const import *

class Comida:
    def __init__(self, cobra):
        imagem_maca = pygame.image.load('assets/maca.png')
        imagem_maca = pygame.transform.scale(imagem_maca, (TAMANHO_BLOCO, TAMANHO_BLOCO))
        self.posicao = self.gerar_posicao(cobra)
        self.imagem = imagem_maca

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
            x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
            y = random.randrange(MARGEM_SUPERIOR, ALTURA, TAMANHO_BLOCO)
            posicao = (x, y)
            # Verifica se a posição não está ocupada pela cobra
            if posicao not in cobra.posicao:
                return posicao 