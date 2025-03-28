import pygame
from code.const import *
from datetime import datetime

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

        # Carrega o som de navegação
        self.som_navegacao = pygame.mixer.Sound('assets/option.mp3')
        self.som_navegacao.set_volume(0.5)  # 50% do volume máximo para o som de navegação
        
        # Carrega o som de select
        self.som_select = pygame.mixer.Sound('assets/select.mp3')
        self.som_select.set_volume(0.7)  # 70% do volume máximo para o som de seleção
        
        # Carrega o som de select
        self.som_coin = pygame.mixer.Sound('assets/coin.mp3')
        self.som_coin.set_volume(0.7)  # 70% do volume máximo para o som de seleção

    def _desenhar_fundo(self, imagem):
        """Método auxiliar para desenhar o fundo com overlay"""
        self.tela.blit(imagem, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill(PRETO)
        overlay.set_alpha(128)
        self.tela.blit(overlay, (0, 0))

    def _desenhar_creditos(self):
        """Método auxiliar para desenhar os créditos do aluno."""
        # Renderiza o RU
        texto_ru = self.fonte.render('RU: 3955575', True, BRANCO)
        rect_ru = texto_ru.get_rect(bottomright=(LARGURA - 20, ALTURA - 30))
        self.tela.blit(texto_ru, rect_ru)
        
        # Renderiza o nome
        texto_nome = self.fonte.render('Jack Biller', True, BRANCO)
        rect_nome = texto_nome.get_rect(bottomright=(LARGURA - 20, ALTURA - 10))
        self.tela.blit(texto_nome, rect_nome)

    def _desenhar_moedas(self):
        """Método auxiliar para desenhar as moedas do jogador."""
        # Carrega e redimensiona a imagem da moeda
        imagem_moeda = pygame.image.load('assets/moeda.png')
        imagem_moeda = pygame.transform.scale(imagem_moeda, (30, 30))
        
        # Obtém o total de moedas do banco de dados
        from code.database import Database
        db = Database()
        moedas = db.obter_moedas()
        db.fechar()
        
        # Renderiza a moeda e o número
        self.tela.blit(imagem_moeda, (LARGURA - 100, 10))
        texto_moedas = self.fonte.render(f': {moedas}', True, BRANCO)
        self.tela.blit(texto_moedas, (LARGURA - 65, 10))

    def mostrar_menu_principal(self):
        """Mostra o menu principal do jogo."""
        opcao_selecionada = 0
        opcoes = ['JOGAR', 'VELOCIDADE', 'CONTROLES', 'HISTÓRICO', 'SHOP', 'SAIR']
        
        while True:
            self._desenhar_fundo(self.imagem_menu)
            
            titulo = self.fonte_grande.render('JOGO DA COBRINHA', True, VERDE)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)
            
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(opcao, True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
                self.tela.blit(texto, rect)
            
            # Adiciona os créditos e moedas
            self._desenhar_creditos()
            self._desenhar_moedas()
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'SAIR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_RETURN:
                        return opcoes[opcao_selecionada]
                    elif evento.key == pygame.K_ESCAPE:
                        return 'SAIR'

    def mostrar_velocidade(self):
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
            
            # Adiciona os créditos e moedas
            self._desenhar_creditos()
            self._desenhar_moedas()
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'VOLTAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_RETURN:
                        return opcoes[opcao_selecionada]
                    elif evento.key == pygame.K_ESCAPE:
                        return 'VOLTAR'

    def mostrar_tela_final(self, db, pontuacao, velocidade, pausado=False):
        """Mostra a tela final do jogo com a pontuação e opções."""
        opcao_selecionada = 0
        opcoes = ['MENU PRINCIPAL', 'JOGAR NOVAMENTE', 'SAIR']

        # Carrega as imagens
        imagem_maca = pygame.image.load('assets/maca.png')
        imagem_maca = pygame.transform.scale(imagem_maca, (30, 30))
        
        imagem_moeda = pygame.image.load('assets/moeda.png')
        imagem_moeda = pygame.transform.scale(imagem_moeda, (30, 30))
        
        # Obtém a velocidade atual do banco de dados
        from code.database import Database
        db = Database()
        velocidade = db.obter_velocidade()
        moedas_ganhas = db.calcular_moedas(pontuacao, velocidade)
        db.fechar()
        
        # Define o texto da velocidade
        if velocidade == 'LENTO':
            velocidade_texto = 'LENTO'
        elif velocidade == 'MODERADO':
            velocidade_texto = 'MODERADO'
        else:
            velocidade_texto = 'RÁPIDO'
        
        while True:
            self._desenhar_fundo(self.imagem_fim)
            
            titulo = self.fonte_grande.render('FIM DE JOGO', True, BRANCO)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)

            if not pausado:            
                # Renderiza a pontuação com o ícone da maçã
                texto_pontuacao = self.fonte.render(f': {pontuacao}', True, BRANCO)
                pos_x_maca = LARGURA/2 - 100
                self.tela.blit(imagem_maca, (pos_x_maca, ALTURA/8 + 50))
                self.tela.blit(texto_pontuacao, (pos_x_maca + 35, ALTURA/8 + 50))
                
                # Renderiza a seta de conversão
                texto_seta = self.fonte.render('->', True, BRANCO)
                self.tela.blit(texto_seta, (LARGURA/2 - 5, ALTURA/8 + 50))
                
                # Renderiza as moedas ganhas com o ícone da moeda
                texto_moedas = self.fonte.render(f': {moedas_ganhas}', True, BRANCO)
                pos_x_moeda = LARGURA/2 + 40
                self.tela.blit(imagem_moeda, (pos_x_moeda, ALTURA/8 + 50))
                self.tela.blit(texto_moedas, (pos_x_moeda + 35, ALTURA/8 + 50))
            else:
                texto_pontuacao = self.fonte.render(f': {pontuacao}', True, BRANCO)
                pos_x_maca = LARGURA/2 - 35
                self.tela.blit(imagem_maca, (pos_x_maca, ALTURA/8 + 50))
                self.tela.blit(texto_pontuacao, (pos_x_maca + 35, ALTURA/8 + 50))
            
            # Renderiza as opções
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(opcao, True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + 80 + i * 50))
                self.tela.blit(texto, rect)
            
            # Adiciona os créditos
            self._desenhar_creditos()
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_RETURN:
                        if opcao_selecionada == 0:  # Menu Principal
                            return "menu"
                        elif opcao_selecionada == 1:  # Jogar Novamente
                            return "jogar"
                        else:  # Sair
                            return False
                    elif evento.key == pygame.K_ESCAPE:
                        return False

    def mostrar_menu_pausa(self, cobra, comida, pontuacao, velocidade_texto):
        """
        Mostra o menu de pausa com o estado atual do jogo.
        
        Args:
            cobra: Objeto da cobra para desenhar seu estado atual
            comida: Objeto da comida para desenhar sua posição
            pontuacao: Pontuação atual do jogo
            velocidade_texto: Texto indicando a velocidade atual
            
        Returns:
            str: Opção selecionada ('CONTINUAR' ou 'ENCERRAR')
        """
        opcao_selecionada = 0
        opcoes = ['CONTINUAR', 'ENCERRAR']
        
        # Carrega e redimensiona a imagem de fundo
        imagem_fundo = pygame.image.load('assets/fundo-game.png')
        imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
        
        while True:
            # Desenha o fundo
            self.tela.blit(imagem_fundo, (0, 0))
            
            # Desenha a linha divisória
            pygame.draw.line(self.tela, CINZA, (0, MARGEM_SUPERIOR), (LARGURA, MARGEM_SUPERIOR), 2)
            
            # Desenha o estado atual do jogo
            cobra.desenhar(self.tela)
            comida.desenhar(self.tela)
            
            # Cria uma superfície semi-transparente para escurecer o jogo
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)  # 128 é 50% de opacidade
            self.tela.blit(overlay, (0, 0))
            
            # Renderiza o título
            titulo = self.fonte_grande.render('JOGO PAUSADO', True, VERDE)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/4))
            self.tela.blit(titulo, rect_titulo)
            
            # Renderiza as opções
            for i, opcao in enumerate(opcoes):
                cor = AMARELO if i == opcao_selecionada else BRANCO
                texto = self.fonte.render(opcao, True, cor)
                rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
                self.tela.blit(texto, rect)
            
            # Renderiza a pontuação com o ícone da maçã
            texto_pontuacao = self.fonte.render(f': {pontuacao}', True, BRANCO)
            imagem_maca = pygame.image.load('assets/maca.png')
            imagem_maca = pygame.transform.scale(imagem_maca, (30, 30))
            self.tela.blit(imagem_maca, (LARGURA/2 - 100, ALTURA/3))
            self.tela.blit(texto_pontuacao, (LARGURA/2 - 65, ALTURA/3))
            
            # Renderiza a velocidade com o ícone do raio
            texto_velocidade = self.fonte.render(f': {velocidade_texto}', True, BRANCO)
            imagem_raio = pygame.image.load('assets/raio.png')
            imagem_raio = pygame.transform.scale(imagem_raio, (30, 30))
            self.tela.blit(imagem_raio, (LARGURA/2 + 20, ALTURA/3))
            self.tela.blit(texto_velocidade, (LARGURA/2 + 55, ALTURA/3))
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'ENCERRAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                        self.som_navegacao.play()  # Toca o som ao navegar
                    elif evento.key == pygame.K_RETURN:
                        return opcoes[opcao_selecionada]
                    elif evento.key == pygame.K_ESCAPE:
                        return 'CONTINUAR'

    def mostrar_historico(self):
        """Mostra o histórico das 9 melhores pontuações."""
        opcao_selecionada = 0
        opcoes = ['VOLTAR']
        
        # Carrega a imagem de fundo específica para o histórico
        imagem_fundo = pygame.image.load('assets/fundo-historico.png')
        imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
        
        while True:
            self._desenhar_fundo(imagem_fundo)
            
            titulo = self.fonte_grande.render('MELHORES PONTUAÇÕES', True, VERDE)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)
            
            # Obtém as pontuações do banco de dados
            from code.database import Database
            db = Database()
            pontuacoes = db.obter_melhores_pontuacoes(limite=9)  # Limita a 9 resultados
            db.fechar()
            
            # Renderiza as pontuações
            for i, (pontuacao, velocidade, data_hora_str, tempo_jogo) in enumerate(pontuacoes):
                try:
                    # Tenta converter a string de data/hora em objeto datetime
                    # Primeiro tenta com o formato que inclui milissegundos
                    try:
                        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        # Se falhar, tenta sem milissegundos
                        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")
                    
                    data_formatada = data_hora.strftime("%d/%m/%Y %H:%M")
                    minutos = tempo_jogo // 60
                    segundos = tempo_jogo % 60
                    texto = f"{pontuacao} maçãs - {velocidade} - {minutos:02d}:{segundos:02d} - {data_formatada}"
                    texto_surface = self.fonte.render(texto, True, BRANCO)
                    rect = texto_surface.get_rect(center=(LARGURA/2, ALTURA/4 + i * 40))
                    self.tela.blit(texto_surface, rect)
                except Exception as e:
                    print(f"Erro ao processar data/hora: {e}")
                    continue
            
            # Renderiza a opção de voltar
            texto = self.fonte.render('VOLTAR', True, AMARELO)
            rect = texto.get_rect(center=(LARGURA/2, ALTURA - 100))
            self.tela.blit(texto, rect)
            
            # Adiciona os créditos e moedas
            self._desenhar_creditos()
            self._desenhar_moedas()
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'VOLTAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                        return 'VOLTAR'

    def mostrar_controles(self):
        """Mostra a tela de controles do jogo."""
        opcao_selecionada = 0
        opcoes = ['VOLTAR']
        
        # Carrega a imagem de fundo específica para os controles
        imagem_fundo = pygame.image.load('assets/fundo-config.png')
        imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
        
        while True:
            self._desenhar_fundo(imagem_fundo)
            
            titulo = self.fonte_grande.render('CONTROLES', True, VERDE)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)
            
            # Renderiza as instruções de controle
            instrucoes = [
                "Use as SETAS do teclado para mover a cobra:",
                "^ - Move para cima",
                "v - Move para baixo",
                "< - Move para a esquerda", 
                "> - Move para a direita",
                "",
                "Outros controles:",
                "ESC - Pausa o jogo",
                "ENTER - Seleciona opções nos menus"
            ]
            
            for i, texto in enumerate(instrucoes):
                cor = BRANCO
                texto_surface = self.fonte.render(texto, True, cor)
                rect = texto_surface.get_rect(center=(LARGURA/2, ALTURA/4 + i * 40))
                self.tela.blit(texto_surface, rect)
            
            # Renderiza a opção de voltar
            texto = self.fonte.render('VOLTAR', True, AMARELO)
            rect = texto.get_rect(center=(LARGURA/2, ALTURA - 100))
            self.tela.blit(texto, rect)
            
            # Adiciona os créditos e moedas
            self._desenhar_creditos()
            self._desenhar_moedas()
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'VOLTAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                        return 'VOLTAR'

    def mostrar_shop(self):
        """Mostra a tela de shop para comprar skins."""
        opcao_selecionada = 0
        
        # Carrega a imagem de fundo específica para o shop
        imagem_fundo = pygame.image.load('assets/fundo-shop.png')
        imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
        
        # Carrega a imagem da moeda
        imagem_moeda = pygame.image.load('assets/moeda.png')
        imagem_moeda = pygame.transform.scale(imagem_moeda, (30, 30))
        
        # Obtém as skins do banco de dados
        from code.database import Database
        db = Database()
        skins = db.obter_skins()
        moedas = db.obter_moedas()
        db.fechar()
        
        # Cria uma instância da cobrinha para atualizar a skin
        from code.cobrinha import Cobrinha
        cobra = Cobrinha()
        
        while True:
            self._desenhar_fundo(imagem_fundo)
            
            titulo = self.fonte_grande.render('SHOP DE SKINS', True, VERDE)
            rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/8))
            self.tela.blit(titulo, rect_titulo)
            
            # Desenha os cards das skins
            for i, skin in enumerate(skins):
                # Calcula a posição do card
                x = LARGURA/2 - 310 if i % 2 == 0 else LARGURA/2 + 10
                y = ALTURA/5 if i < 2 else ALTURA/3 + 100
                
                # Desenha o card
                # Cria uma superfície semi-transparente para o fundo do card
                card_fundo = pygame.Surface((300, 150))
                card_fundo.fill(PRETO)
                card_fundo.set_alpha(50)  # 50 é aproximadamente 20% de opacidade
                self.tela.blit(card_fundo, (x, y))
                pygame.draw.rect(self.tela, CINZA, (x, y, 300, 150), 2)
                
                # Carrega e desenha a imagem da cobrinha
                sprite_sheet = pygame.image.load(f'assets/{skin[2]}')
                sprites_cobra = []
                for j in range(7):
                    sprite = sprite_sheet.subsurface((0, j * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
                    sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
                    sprites_cobra.append(sprite)

                # Posição inicial ajustada para a área jogável
                posicao1 = (x + 20 + (TAMANHO_BLOCO * 3), y + 0 + (MARGEM_SUPERIOR /2))
                posicao2 = (x + 20 + (TAMANHO_BLOCO * 2), y + 0 + (MARGEM_SUPERIOR /2))
                posicao3 = (x + 20 + (TAMANHO_BLOCO * 1), y + 0 + (MARGEM_SUPERIOR /2))
                posicao4 = (x + 20 + (TAMANHO_BLOCO * 1), y + (TAMANHO_BLOCO * 1) + (MARGEM_SUPERIOR /2))
                posicao5 = (x + 20 + (TAMANHO_BLOCO * 1), y + (TAMANHO_BLOCO * 2) + (MARGEM_SUPERIOR /2))
                posicao6 = (x + 20 + (TAMANHO_BLOCO * 2), y + (TAMANHO_BLOCO * 2) + (MARGEM_SUPERIOR /2))
                posicao7 = (x + 20 + (TAMANHO_BLOCO * 3), y + (TAMANHO_BLOCO * 2) + (MARGEM_SUPERIOR /2))
                posicao8 = (x + 20 + (TAMANHO_BLOCO * 3), y + (TAMANHO_BLOCO * 3) + (MARGEM_SUPERIOR /2))
                posicao9 = (x + 20 + (TAMANHO_BLOCO * 3), y + (TAMANHO_BLOCO * 4) + (MARGEM_SUPERIOR /2))
                posicao10 = (x + 20 + (TAMANHO_BLOCO * 2), y + (TAMANHO_BLOCO * 4) + (MARGEM_SUPERIOR /2))
                posicao11 = (x + 20 + (TAMANHO_BLOCO * 1), y + (TAMANHO_BLOCO * 4) + (MARGEM_SUPERIOR /2))
                self.posicao = [posicao1, posicao2, posicao3, posicao4, posicao5, posicao6, posicao7, posicao8, posicao9, posicao10, posicao11]
                self.direcao = [TAMANHO_BLOCO, 0]
                self.comprimento = 3
                self.sprites = sprites_cobra
                self.rotacoes = {
                    (0, -TAMANHO_BLOCO): 0,  # Cima
                    (0, TAMANHO_BLOCO): 180,  # Baixo
                    (-TAMANHO_BLOCO, 0): 90,  # Esquerda
                    (TAMANHO_BLOCO, 0): 270   # Direita
                }
                for j, posicao in enumerate(self.posicao):
                    sprite = self.obter_sprite_parte(j)
                    self.tela.blit(sprite, posicao)
                
                # Desenha o nome da skin
                texto_nome = self.fonte.render(skin[1], True, BRANCO)
                self.tela.blit(texto_nome, (x + 140, y + 30))
                
                # Verifica se está selecionada
                if skin[5]:  # selecionada
                    texto_status = pygame.font.SysFont('Lucida Sans Typewriter', 24).render('SELECIONADA', True, VERDE)
                elif skin[4]:  # desbloqueada
                    texto_status = pygame.font.SysFont('Lucida Sans Typewriter', 24).render('DESBLOQUEADA', True, AZUL)
                else:  # bloqueada
                    texto_status = pygame.font.SysFont('Lucida Sans Typewriter', 24).render(f'{skin[3]} moedas', True, AMARELO)
                    self.tela.blit(imagem_moeda, (x + 140, y + 90))
                
                if skin[5] or skin[4]:
                    self.tela.blit(texto_status, (x + 140, y + 90))
                else:
                    self.tela.blit(texto_status, (x + 180, y + 90))
                
                # Destaca o card selecionado
                if i == opcao_selecionada:
                    pygame.draw.rect(self.tela, AMARELO, (x, y, 300, 150), 3)
            
            # Renderiza a opção de voltar
            texto = self.fonte.render('VOLTAR', True, AMARELO if opcao_selecionada == len(skins) else BRANCO)
            rect = texto.get_rect(center=(LARGURA/2, ALTURA - 100))
            self.tela.blit(texto, rect)
            
            # Adiciona os créditos e moedas
            self._desenhar_creditos()
            self._desenhar_moedas()
            
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'VOLTAR'
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % (len(skins) + 1)
                        self.som_navegacao.play()
                    elif evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % (len(skins) + 1)
                        self.som_navegacao.play()
                    elif evento.key == pygame.K_RETURN:
                        if opcao_selecionada == len(skins):  # Opção voltar
                            return 'VOLTAR'
                        
                        # Obtém informações da skin selecionada
                        skin = skins[opcao_selecionada]
                        db = Database()
                        
                        # Verifica se está desbloqueada
                        if db.verificar_skin_desbloqueada(skin[0]):
                            # Verifica se está selecionada
                            if db.verificar_skin_selecionada(skin[0]):
                                # Já está selecionada
                                continue
                            else:
                                # Seleciona a skin
                                db.selecionar_skin(skin[0])
                                # Atualiza a skin da cobrinha
                                cobra.atualizar_skin()
                                self.som_select.play()
                                return 'VOLTAR'
                        else:
                            # Verifica se tem moedas suficientes
                            preco = db.obter_preco_skin(skin[0])
                            if moedas >= preco:
                                # Pergunta se deseja comprar
                                if self._confirmar_compra(preco):
                                    # Compra a skin
                                    db.adicionar_moedas(-preco)
                                    db.desbloquear_skin(skin[0])
                                    db.selecionar_skin(skin[0])
                                    cobra.atualizar_skin()
                                    self.som_coin.play()
                                    return 'VOLTAR'
                            else:
                                # Moedas insuficientes
                                self._mostrar_mensagem('Moedas insuficientes!')
                        
                        db.fechar()
                    elif evento.key == pygame.K_ESCAPE:
                        return 'VOLTAR'

    def _confirmar_compra(self, preco):
        """Mostra uma mensagem de confirmação de compra."""
        mensagem = f'Deseja comprar por {preco} moedas?'
        texto = self.fonte.render(mensagem, True, BRANCO)
        rect = texto.get_rect(center=(LARGURA/2, ALTURA/2))
        
        # Desenha um fundo semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill(PRETO)
        overlay.set_alpha(128)
        self.tela.blit(overlay, (0, 0))
        
        # Desenha a mensagem
        self.tela.blit(texto, rect)
        
        # Adiciona as instruções de confirmação
        texto_instrucoes = self.fonte.render('ENTER - Comprar | ESC - Sair', True, BRANCO)
        rect_instrucoes = texto_instrucoes.get_rect(center=(LARGURA/2, ALTURA/2 + 40))
        self.tela.blit(texto_instrucoes, rect_instrucoes)
        
        pygame.display.update()
        
        # Aguarda a resposta do usuário
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return True
                    elif evento.key == pygame.K_ESCAPE:
                        return False
            pygame.time.wait(100)

    def _mostrar_mensagem(self, mensagem):
        """Mostra uma mensagem na tela."""
        texto = self.fonte.render(mensagem, True, BRANCO)
        rect = texto.get_rect(center=(LARGURA/2, ALTURA/2))

        texto_instrucoes = self.fonte.render('ESC - Sair', True, BRANCO)
        rect_instrucoes = texto_instrucoes.get_rect(center=(LARGURA/2, ALTURA/2 + 40))
        
        # Desenha um fundo semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill(PRETO)
        overlay.set_alpha(128)
        self.tela.blit(overlay, (0, 0))
        
        # Desenha a mensagem
        self.tela.blit(texto, rect)
        self.tela.blit(texto_instrucoes, rect_instrucoes)
        pygame.display.update()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False
            pygame.time.wait(100)

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
