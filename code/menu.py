import pygame
from code.const import *

class Menu:
    def __init__(self, tela, fonte, fonte_grande):
        """
        Inicializa o menu do jogo.
        
        Args:
            tela: Superfície do Pygame onde o menu será desenhado
            fonte: Fonte para textos normais
            fonte_grande: Fonte para textos grandes
        """
        self.tela = tela
        self.fonte = fonte
        self.fonte_grande = fonte_grande
        
        # Carrega as imagens de fundo
        self.imagem_menu = pygame.image.load('assets/fundo-menu.jpeg')
        self.imagem_config = pygame.image.load('assets/fundo-config.png')
        self.imagem_fim = pygame.image.load('assets/fundo-end-game.png')
        
        # Redimensiona as imagens
        self.imagem_menu = pygame.transform.scale(self.imagem_menu, (LARGURA, ALTURA))
        self.imagem_config = pygame.transform.scale(self.imagem_config, (LARGURA, ALTURA))
        self.imagem_fim = pygame.transform.scale(self.imagem_fim, (LARGURA, ALTURA))

    def _desenhar_fundo(self, imagem):
        """Método auxiliar para desenhar o fundo com overlay"""
        self.tela.blit(imagem, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill(PRETO)
        overlay.set_alpha(128)
        self.tela.blit(overlay, (0, 0))

    def mostrar_menu_principal(self):
        """Mostra o menu principal do jogo."""
        opcao_selecionada = 0
        opcoes = ['JOGAR', 'DIFICULDADE', 'SAIR']
        
        while True:
            self._desenhar_fundo(self.imagem_menu)
            
            titulo = self.fonte_grande.render('JOGO DA COBRINHA', True, VERDE)
            
            # Renderiza as opções com cores diferentes baseado na seleção
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(f'{opcao}', True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
                self.tela.blit(texto, rect)
            
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'SAIR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    elif evento.key == pygame.K_RETURN:
                        return opcoes[opcao_selecionada]
                    elif evento.key == pygame.K_ESCAPE:
                        return 'SAIR'

    def mostrar_dificuldade(self):
        """Mostra o menu de seleção de velocidade."""
        opcao_selecionada = 0
        opcoes = ['LENTO', 'MODERADO', 'RÁPIDO', 'VOLTAR']
        
        while True:
            self._desenhar_fundo(self.imagem_config)
            
            titulo = self.fonte_grande.render('VELOCIDADE', True, VERDE)
            
            # Renderiza as opções com cores diferentes baseado na seleção
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(f'{opcao}', True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
                self.tela.blit(texto, rect)
            
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'VOLTAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    elif evento.key == pygame.K_RETURN:
                        return opcoes[opcao_selecionada]
                    elif evento.key == pygame.K_ESCAPE:
                        return 'VOLTAR'

    def mostrar_tela_final(self, pontuacao):
        """
        Mostra a tela de fim de jogo com a pontuação.
        
        Args:
            pontuacao: Pontuação final do jogador
        """
        opcao_selecionada = 0
        opcoes = ['MENU PRINCIPAL', 'JOGAR NOVAMENTE', 'SAIR']
        
        while True:
            self._desenhar_fundo(self.imagem_fim)
            
            texto_fim = self.fonte_grande.render('Fim de Jogo!', True, BRANCO)
            texto_pontuacao = self.fonte.render(f'Pontuação Final: {pontuacao} maçãs', True, BRANCO)
            
            rect_fim = texto_fim.get_rect(center=(LARGURA/2, ALTURA/6.5))
            rect_pontuacao = texto_pontuacao.get_rect(center=(LARGURA/2, ALTURA/6.5 + 50))
            
            self.tela.blit(texto_fim, rect_fim)
            self.tela.blit(texto_pontuacao, rect_pontuacao)
            
            # Renderiza as opções com cores diferentes baseado na seleção
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(opcao, True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + 80 + i * 50))
                self.tela.blit(texto, rect)
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    elif evento.key == pygame.K_RETURN:
                        if opcao_selecionada == 0:  # Menu Principal
                            return "menu"
                        elif opcao_selecionada == 1:  # Jogar Novamente
                            return "jogar"
                        else:  # Sair
                            return False
                    elif evento.key == pygame.K_ESCAPE:
                        return False

    def mostrar_menu_pausa(self, cobra, comida, pontuacao, dificuldade_texto):
        """
        Mostra o menu de pausa durante o jogo.
        
        Args:
            cobra: Instância da cobra para desenhar no fundo
            comida: Instância da comida para desenhar no fundo
            pontuacao: Pontuação atual do jogador
            dificuldade_texto: Texto da dificuldade atual
        """
        opcao_selecionada = 0
        opcoes = ['CONTINUAR', 'ENCERRAR']
        
        # Carrega e redimensiona a imagem da maçã para o placar
        imagem_maca_placar = pygame.image.load('assets/maca.png')
        imagem_maca_placar = pygame.transform.scale(imagem_maca_placar, (30, 30))
        
        while True:
            # Desenha o estado atual do jogo
            self.tela.fill(PRETO)
            
            # Desenha a linha divisória
            pygame.draw.line(self.tela, CINZA, (0, MARGEM_SUPERIOR), (LARGURA, MARGEM_SUPERIOR), 2)
            
            # Desenha a cobra e a comida
            cobra.desenhar(self.tela)
            comida.desenhar(self.tela)
            
            # Renderiza a pontuação com o ícone da maçã
            texto_pontuacao = self.fonte.render(f': {pontuacao}', True, BRANCO)
            self.tela.blit(imagem_maca_placar, (10, 5))
            self.tela.blit(texto_pontuacao, (45, 5))
            
            # Renderiza o texto de dificuldade
            texto_dificuldade = self.fonte.render(f'Dificuldade: {dificuldade_texto}', True, BRANCO)
            self.tela.blit(texto_dificuldade, (LARGURA - texto_dificuldade.get_width() - 10, 5))
            
            # Adiciona um overlay semi-transparente para escurecer o jogo
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.fill(PRETO)
            overlay.set_alpha(128)
            self.tela.blit(overlay, (0, 0))
            
            # Desenha o menu de pausa
            titulo = self.fonte_grande.render('JOGO PAUSADO', True, VERDE)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/3))
            self.tela.blit(titulo, rect_titulo)
            
            # Renderiza as opções com cores diferentes baseado na seleção
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(f'{opcao}', True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
                self.tela.blit(texto, rect)
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'ENCERRAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    elif evento.key == pygame.K_RETURN:
                        return opcoes[opcao_selecionada]
                    elif evento.key == pygame.K_ESCAPE:
                        return 'CONTINUAR' 