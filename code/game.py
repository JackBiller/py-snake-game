import pygame

from code.const import *
from code.cobrinha import Cobrinha
from code.comida import Comida
from code.menu import Menu

class Game:
    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Jogo da Cobrinha')

        self.fonte = pygame.font.SysFont('Lucida Sans Typewriter', FONTE_NORMAL)
        self.fonte_grande = pygame.font.SysFont('Lucida Sans Typewriter', FONTE_GRANDE)
        self.menu = Menu(self.tela, self.fonte, self.fonte_grande)
        
        # Carrega e redimensiona a imagem da maçã para o placar
        self.imagem_maca_placar = pygame.image.load('assets/maca.png')
        self.imagem_maca_placar = pygame.transform.scale(self.imagem_maca_placar, (30, 30))
        
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
            velocidade_texto = "LENTO"
        elif velocidade == 10:
            velocidade_texto = "MODERADO"
        else:
            velocidade_texto = "RÁPIDO"

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        # Mostra o menu de pausa com o estado atual do jogo
                        escolha = self.menu.mostrar_menu_pausa(cobra, comida, pontuacao, velocidade_texto)
                        if escolha == 'ENCERRAR':
                            return self.menu.mostrar_tela_final(pontuacao)
                        continue  # Pula o resto do loop se estiver pausado
                    else:
                        cobra.mudar_direcao(evento.key)

            cobra.mover()

            if cobra.posicao[0] == comida.posicao:
                cobra.crescer()
                comida = Comida(cobra)
                pontuacao += 1

            if cobra.colisao():
                rodando = False

            self.tela.fill(PRETO)
            
            # Desenha a linha divisória
            pygame.draw.line(self.tela, CINZA, (0, MARGEM_SUPERIOR), (LARGURA, MARGEM_SUPERIOR), 2)
            
            cobra.desenhar(self.tela)
            comida.desenhar(self.tela)

            # Renderiza a pontuação com o ícone da maçã
            texto_pontuacao = self.fonte.render(f': {pontuacao}', True, BRANCO)
            self.tela.blit(self.imagem_maca_placar, (10, 5))  # Desenha a maçã
            self.tela.blit(texto_pontuacao, (45, 5))  # Desenha a pontuação após a maçã
            
            # Renderiza o texto de velocidade
            texto_velocidade = self.fonte.render(f'Velocidade: {velocidade_texto}', True, BRANCO)
            self.tela.blit(texto_velocidade, (LARGURA - texto_velocidade.get_width() - 10, 5))

            pygame.display.update()
            clock.tick(velocidade)

        return self.menu.mostrar_tela_final(pontuacao)
    
    def run(self):
        while self.jogando:
            if not self.jogar_novamente:
                escolha_menu = self.menu.mostrar_menu_principal()
            
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
                escolha_dif = self.menu.mostrar_dificuldade()
                if escolha_dif == 'LENTO':
                    self.velocidade = 8
                elif escolha_dif == 'MODERADO':
                    self.velocidade = 10
                elif escolha_dif == 'RÁPIDO':
                    self.velocidade = 12
                elif escolha_dif == 'VOLTAR':
                    continue
            
            elif escolha_menu == 'SAIR':
                self.jogando = False

        pygame.quit()
