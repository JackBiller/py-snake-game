import pygame

from code.const import *
from code.cobrinha import Cobrinha
from code.comida import Comida
from code.menu import mostrar_tela_final, mostrar_menu, mostrar_dificuldade

class Game:
    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Jogo da Cobrinha')

        self.fonte = pygame.font.SysFont('Lucida Sans Typewriter', FONTE_NORMAL)
        self.fonte_grande = pygame.font.SysFont('Lucida Sans Typewriter', FONTE_GRANDE)
        self.jogando = True
        self.velocidade = 10
        self.jogar_novamente = False

    def jogar(self, velocidade=10):
        clock = pygame.time.Clock()
        cobra = Cobrinha()
        comida = Comida(cobra)
        pontuacao = 0
        rodando = True

        if velocidade == 8:
            dificuldade_texto = "FÁCIL"
        elif velocidade == 10:
            dificuldade_texto = "MÉDIO"
        else:
            dificuldade_texto = "DIFÍCIL"

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                elif evento.type == pygame.KEYDOWN:
                    cobra.mudar_direcao(evento.key)

            cobra.mover()

            if cobra.posicao[0] == comida.posicao:
                cobra.crescer()
                comida = Comida(cobra)
                pontuacao += 1

            if cobra.colisao():
                rodando = False

            self.tela.fill(PRETO)
            cobra.desenhar(self.tela)
            comida.desenhar(self.tela)

            texto_pontuacao = self.fonte.render(f'Maçãs: {pontuacao}', True, BRANCO)
            texto_dificuldade = self.fonte.render(f'Dificuldade: {dificuldade_texto}', True, BRANCO)
            self.tela.blit(texto_pontuacao, (10, 10))
            self.tela.blit(texto_dificuldade, (LARGURA - texto_dificuldade.get_width() - 10, 10))

            pygame.display.update()
            clock.tick(velocidade)

        return mostrar_tela_final(self.tela, self.fonte, self.fonte_grande, pontuacao)
    
    def run(self):
        while self.jogando:
            if not self.jogar_novamente:
                escolha_menu = mostrar_menu(self.tela, self.fonte, self.fonte_grande)
            
            if escolha_menu == 'JOGAR' or self.jogar_novamente:
                self.jogar_novamente = False
                resultado = self.jogar(self.velocidade)
                if resultado == False:
                    self.jogando = False
                elif resultado == "menu":
                    continue
                elif resultado == "jogar":
                    self.jogar_novamente = True
                    continue
            
            elif escolha_menu == 'DIFICULDADE':
                escolha_dif = mostrar_dificuldade(self.tela, self.fonte, self.fonte_grande)
                if escolha_dif == 'FÁCIL':
                    self.velocidade = 8
                elif escolha_dif == 'MÉDIO':
                    self.velocidade = 10
                elif escolha_dif == 'DIFÍCIL':
                    self.velocidade = 12
                elif escolha_dif == 'VOLTAR':
                    continue
            
            elif escolha_menu == 'SAIR':
                self.jogando = False

        pygame.quit()
