import pygame
from code.const import *

class Cobrinha:
    def __init__(self):
        sprite_sheet = pygame.image.load('assets/cobrinha.png')
        sprites_cobra = []
        for i in range(7):
            sprite = sprite_sheet.subsurface((0, i * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
            sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
            sprites_cobra.append(sprite)

        self.posicao = [(LARGURA//2, ALTURA//2)]
        self.direcao = [TAMANHO_BLOCO, 0]
        self.comprimento = 3
        self.sprites = sprites_cobra
        self.rotacoes = {
            (0, -TAMANHO_BLOCO): 0,  # Cima
            (0, TAMANHO_BLOCO): 180,  # Baixo
            (-TAMANHO_BLOCO, 0): 90,  # Esquerda
            (TAMANHO_BLOCO, 0): 270   # Direita
        }

    def mover(self):
        nova_x = self.posicao[0][0] + self.direcao[0]
        nova_y = self.posicao[0][1] + self.direcao[1]
        
        # Atravessa as bordas
        if nova_x >= LARGURA:
            nova_x = 0
        elif nova_x < 0:
            nova_x = LARGURA - TAMANHO_BLOCO
            
        if nova_y >= ALTURA:
            nova_y = 0
        elif nova_y < 0:
            nova_y = ALTURA - TAMANHO_BLOCO
            
        nova_posicao = (nova_x, nova_y)
        self.posicao.insert(0, nova_posicao)
        if len(self.posicao) > self.comprimento:
            self.posicao.pop()

    def crescer(self):
        self.comprimento += 1

    def colisao(self):
        # Apenas colisão com o próprio corpo
        if self.posicao[0] in self.posicao[1:]:
            return True
        return False

    def obter_sprite_parte(self, indice):
        if indice == 0:  # Cabeça
            if self.direcao == [0, TAMANHO_BLOCO]:  # Baixo
                return self.sprites[CABECA_BAIXO]
            elif self.direcao == [-TAMANHO_BLOCO, 0]:  # Esquerda
                return self.sprites[CABECA_ESQUERDA]
            elif self.direcao == [TAMANHO_BLOCO, 0]:  # Direita
                return pygame.transform.flip(self.sprites[CABECA_ESQUERDA], True, False)
            else:  # Cima
                sprite_cabeça = pygame.transform.rotate(self.sprites[CABECA_BAIXO], 180)
                sprite_cabeça = pygame.transform.flip(sprite_cabeça, True, False)
                return sprite_cabeça
        
        elif indice == len(self.posicao) - 1:  # Rabo
            dx = self.posicao[-1][0] - self.posicao[-2][0]
            dy = self.posicao[-1][1] - self.posicao[-2][1]
            
            if dx != 0:  # Movimento horizontal
                sprite_rabo = self.sprites[RABO_LATERAL]
                # Se o rabo estiver indo da direita para esquerda, gira 180°
                if dx > 0:
                    sprite_rabo = pygame.transform.rotate(sprite_rabo, 180)
                return sprite_rabo
            else:  # Movimento vertical
                sprite_rabo = self.sprites[RABO_VERTICAL]
                # Se o rabo estiver indo de baixo para cima, gira 180°
                if dy > 0:
                    sprite_rabo = pygame.transform.rotate(sprite_rabo, 180)
                    sprite_rabo = pygame.transform.flip(sprite_rabo, True, False)
                return sprite_rabo
        
        else:  # Corpo
            prev = self.posicao[indice-1]
            curr = self.posicao[indice]
            next = self.posicao[indice+1]
            
            dx1 = curr[0] - prev[0]
            dy1 = curr[1] - prev[1]
            dx2 = next[0] - curr[0]
            dy2 = next[1] - curr[1]
            
            if (dx1 != 0 and dx2 != 0) or (dy1 != 0 and dy2 != 0):
                # Movimento em linha reta
                if dx1 != 0:
                    return self.sprites[CORPO_HORIZONTAL]
                else:
                    return self.sprites[CORPO_VERTICAL]
            else:
                # Curva
                sprite_curva = self.sprites[CORPO_CURVA_LADO_BAIXO]
                # Da esquerda para baixo (padrão)
                if (dx1 > 0 and dy2 > 0) or (dy1 < 0 and dx2 < 0):
                    return sprite_curva
                # Da direita para baixo
                elif (dx1 < 0 and dy2 > 0) or (dy1 < 0 and dx2 > 0):
                    return pygame.transform.flip(sprite_curva, True, False)
                # Da esquerda para cima
                elif (dx1 > 0 and dy2 < 0) or (dy1 > 0 and dx2 < 0):
                    return pygame.transform.flip(sprite_curva, False, True)
                # Da direita para cima
                else:
                    return pygame.transform.flip(sprite_curva, True, True)

    def mudar_direcao(self, tecla):
        if tecla == pygame.K_UP and self.direcao != [0, TAMANHO_BLOCO]:
            self.direcao = [0, -TAMANHO_BLOCO]
        elif tecla == pygame.K_DOWN and self.direcao != [0, -TAMANHO_BLOCO]:
            self.direcao = [0, TAMANHO_BLOCO]
        elif tecla == pygame.K_LEFT and self.direcao != [TAMANHO_BLOCO, 0]:
            self.direcao = [-TAMANHO_BLOCO, 0]
        elif tecla == pygame.K_RIGHT and self.direcao != [-TAMANHO_BLOCO, 0]:
            self.direcao = [TAMANHO_BLOCO, 0] 

    def desenhar(self, tela):
        for i, posicao in enumerate(self.posicao):
            sprite = self.obter_sprite_parte(i)
            tela.blit(sprite, posicao)
