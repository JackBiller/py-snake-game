import pygame

from code.const import *
from code.cobrinha import Cobrinha
from code.comida import Comida
from code.menu import Menu
from code.database import Database

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Inicializa o módulo de áudio

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Jogo da Cobrinha')

        self.fonte = pygame.font.SysFont('Lucida Sans Typewriter', FONTE_NORMAL)
        self.fonte_grande = pygame.font.SysFont('Lucida Sans Typewriter', FONTE_GRANDE)
        self.menu = Menu(self.tela, self.fonte, self.fonte_grande)
        
        # Carrega e redimensiona as imagens para o placar
        self.imagem_maca_placar = pygame.image.load('assets/maca.png')
        self.imagem_maca_placar = pygame.transform.scale(self.imagem_maca_placar, (30, 30))
        
        self.imagem_raio_placar = pygame.image.load('assets/raio.png')
        self.imagem_raio_placar = pygame.transform.scale(self.imagem_raio_placar, (30, 30))
        
        # Carrega e redimensiona a imagem de fundo
        self.imagem_fundo = pygame.image.load('assets/fundo-game.png')
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (LARGURA, ALTURA))
        
        # Carrega o som de comer maçã e ajusta seu volume
        self.som_comer = pygame.mixer.Sound('assets/come.mp3')
        self.som_comer.set_volume(1.0)  # Volume máximo para o som de comer
        
        # Carrega e inicia a música de fundo com volume reduzido
        pygame.mixer.music.load('assets/fundo.mp3')
        pygame.mixer.music.set_volume(0.3)  # 30% do volume máximo para a música de fundo
        pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop infinito
        
        # Inicializa o banco de dados e carrega a última velocidade configurada
        self.db = Database()
        self.velocidade = self.db.obter_velocidade()
        
        self.jogando = True
        self.jogar_novamente = False

    def jogar(self, velocidade=10):
        clock = pygame.time.Clock()
        cobra = Cobrinha()
        comida = Comida(cobra)
        pontuacao = 0
        rodando = True
        
        # Inicializa o cronômetro
        tempo_inicio = pygame.time.get_ticks()
        tempo_pausado = 0
        tempo_total_pausado = 0

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
                        tempo_pausado = pygame.time.get_ticks()
                        escolha = self.menu.mostrar_menu_pausa(cobra, comida, pontuacao, velocidade_texto)
                        if escolha == 'ENCERRAR':
                            tempo_total = (pygame.time.get_ticks() - tempo_inicio - tempo_total_pausado) // 1000
                            self.db.salvar_partida(pontuacao, velocidade_texto, tempo_total)
                            return self.menu.mostrar_tela_final(self.db, pontuacao, velocidade_texto, True)
                        tempo_total_pausado += pygame.time.get_ticks() - tempo_pausado
                        continue 
                    else:
                        cobra.mudar_direcao(evento.key)

            cobra.mover()

            if cobra.posicao[0] == comida.posicao:
                cobra.crescer()
                comida = Comida(cobra)
                pontuacao += 1
                self.som_comer.play()  # Toca o som quando come a maçã
            
            texto_debug = self.fonte.render(f'Cobra: {cobra.posicao[0]} Maçã: {comida.posicao}', True, BRANCO)
            self.tela.blit(texto_debug, (10, ALTURA - 30))

            if cobra.colisao():
                rodando = False

            self.tela.blit(self.imagem_fundo, (0, 0))
            
            # Desenha a linha divisória
            pygame.draw.line(self.tela, CINZA, (0, MARGEM_SUPERIOR), (LARGURA, MARGEM_SUPERIOR), 2)
            
            cobra.desenhar(self.tela)
            comida.desenhar(self.tela)

            # Renderiza a pontuação com o ícone da maçã
            texto_pontuacao = self.fonte.render(f': {pontuacao}', True, BRANCO)
            self.tela.blit(self.imagem_maca_placar, (10, 10))
            self.tela.blit(texto_pontuacao, (45, 10))
            
            # Renderiza a velocidade com o ícone do raio
            texto_velocidade = self.fonte.render(f': {velocidade_texto}', True, BRANCO)
            largura_texto = texto_velocidade.get_width()
            pos_x_raio = LARGURA - largura_texto - 45
            self.tela.blit(self.imagem_raio_placar, (pos_x_raio, 10))
            self.tela.blit(texto_velocidade, (LARGURA - largura_texto - 10, 10))
            
            # Renderiza o cronômetro centralizado
            tempo_atual = (pygame.time.get_ticks() - tempo_inicio - tempo_total_pausado) // 1000
            minutos = tempo_atual // 60
            segundos = tempo_atual % 60
            texto_tempo = self.fonte.render(f'{minutos:02d}:{segundos:02d}', True, BRANCO)
            # Centraliza o texto na tela
            pos_x_tempo = LARGURA // 2 - texto_tempo.get_width() // 2
            self.tela.blit(texto_tempo, (pos_x_tempo, 10))

            pygame.display.update()
            clock.tick(velocidade)

        # Calcula o tempo total de jogo em segundos
        tempo_total = (pygame.time.get_ticks() - tempo_inicio - tempo_total_pausado) // 1000
        # Salva a pontuação ao fim do jogo
        self.db.salvar_partida(pontuacao, velocidade_texto, tempo_total)
        moedas_ganhas = self.db.calcular_moedas(pontuacao, velocidade)
        self.db.adicionar_moedas(moedas_ganhas)
        return self.menu.mostrar_tela_final(self.db, pontuacao, velocidade)
    
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
            
            elif escolha_menu == 'VELOCIDADE':
                escolha_dif = self.menu.mostrar_velocidade()
                if escolha_dif == 'LENTO':
                    self.velocidade = 8
                elif escolha_dif == 'MODERADO':
                    self.velocidade = 10
                elif escolha_dif == 'RÁPIDO':
                    self.velocidade = 12
                elif escolha_dif == 'VOLTAR':
                    continue
                
                # Salva a nova velocidade no banco de dados
                if escolha_dif != 'VOLTAR':
                    self.db.salvar_velocidade(self.velocidade)
            
            elif escolha_menu == 'HISTÓRICO':
                self.menu.mostrar_historico()
                continue
            
            elif escolha_menu == 'SAIR':
                self.jogando = False

        # Fecha a conexão com o banco de dados ao sair
        self.db.fechar()
        pygame.mixer.music.stop()  # Para a música de fundo antes de fechar
        pygame.quit()
