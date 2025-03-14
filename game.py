import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definição das cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Configurações da tela
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 20

# Criação da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Cobrinha')

# Carrega as imagens
imagem_maca = pygame.image.load('maca.png')
imagem_maca = pygame.transform.scale(imagem_maca, (TAMANHO_BLOCO, TAMANHO_BLOCO))

# Carrega e prepara os sprites da cobrinha
sprite_sheet = pygame.image.load('cobrinha.png')
sprites_cobra = []

# Obtém as dimensões da sprite sheet
sprite_sheet_height = sprite_sheet.get_height()
sprite_size = 42  # Tamanho de cada sprite

# Verifica quantos sprites cabem na altura da imagem
num_sprites = sprite_sheet_height // sprite_size

for i in range(7):  # Precisamos exatamente de 7 sprites
    sprite = sprite_sheet.subsurface((0, i * sprite_size, sprite_size, sprite_size))
    sprite = pygame.transform.scale(sprite, (TAMANHO_BLOCO, TAMANHO_BLOCO))
    sprites_cobra.append(sprite)


# Índices dos sprites
RABO_LATERAL = 0
CABECA_BAIXO = 1
CORPO_CURVA_LADO_BAIXO = 2
CORPO_HORIZONTAL = 3
CABECA_ESQUERDA = 4
RABO_VERTICAL = 5
CORPO_VERTICAL = 6

# Configuração da fonte
fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 72)

def mostrar_menu():
    tela.fill(PRETO)
    titulo = fonte_grande.render('JOGO DA COBRINHA', True, VERDE)
    jogar = fonte.render('1 - JOGAR', True, BRANCO)
    dificuldade = fonte.render('2 - DIFICULDADE', True, BRANCO)
    sair = fonte.render('3 - SAIR', True, BRANCO)
    
    rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/4))
    rect_jogar = jogar.get_rect(center=(LARGURA/2, ALTURA/2))
    rect_dificuldade = dificuldade.get_rect(center=(LARGURA/2, ALTURA/2 + 50))
    rect_sair = sair.get_rect(center=(LARGURA/2, ALTURA/2 + 100))
    
    tela.blit(titulo, rect_titulo)
    tela.blit(jogar, rect_jogar)
    tela.blit(dificuldade, rect_dificuldade)
    tela.blit(sair, rect_sair)
    pygame.display.update()

def mostrar_dificuldade():
    tela.fill(PRETO)
    titulo = fonte_grande.render('DIFICULDADE', True, VERDE)
    facil = fonte.render('1 - FÁCIL', True, BRANCO)
    medio = fonte.render('2 - MÉDIO', True, BRANCO)
    dificil = fonte.render('3 - DIFÍCIL', True, BRANCO)
    voltar = fonte.render('4 - VOLTAR', True, BRANCO)
    
    rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/4))
    rect_facil = facil.get_rect(center=(LARGURA/2, ALTURA/2))
    rect_medio = medio.get_rect(center=(LARGURA/2, ALTURA/2 + 50))
    rect_dificil = dificil.get_rect(center=(LARGURA/2, ALTURA/2 + 100))
    rect_voltar = voltar.get_rect(center=(LARGURA/2, ALTURA/2 + 150))
    
    tela.blit(titulo, rect_titulo)
    tela.blit(facil, rect_facil)
    tela.blit(medio, rect_medio)
    tela.blit(dificil, rect_dificil)
    tela.blit(voltar, rect_voltar)
    pygame.display.update()

# Classe da Cobrinha
class Cobra:
    def __init__(self):
        self.posicao = [(LARGURA//2, ALTURA//2)]
        self.direcao = [TAMANHO_BLOCO, 0]
        self.comprimento = 3
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
                return sprites_cobra[CABECA_BAIXO]
            elif self.direcao == [-TAMANHO_BLOCO, 0]:  # Esquerda
                return sprites_cobra[CABECA_ESQUERDA]
            elif self.direcao == [TAMANHO_BLOCO, 0]:  # Direita
                return pygame.transform.flip(sprites_cobra[CABECA_ESQUERDA], True, False)
            else:  # Cima
                return pygame.transform.rotate(sprites_cobra[CABECA_BAIXO], 180)
        
        elif indice == len(self.posicao) - 1:  # Rabo
            dx = self.posicao[-1][0] - self.posicao[-2][0]
            dy = self.posicao[-1][1] - self.posicao[-2][1]
            
            if dx != 0:  # Movimento horizontal
                sprite_rabo = sprites_cobra[RABO_LATERAL]
                # Se o rabo estiver indo da direita para esquerda, gira 180°
                if dx > 0:
                    sprite_rabo = pygame.transform.rotate(sprite_rabo, 180)
                return sprite_rabo
            else:  # Movimento vertical
                sprite_rabo = sprites_cobra[RABO_VERTICAL]
                # Se o rabo estiver indo de baixo para cima, gira 180°
                if dy > 0:
                    sprite_rabo = pygame.transform.rotate(sprite_rabo, 180)
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
                    return sprites_cobra[CORPO_HORIZONTAL]
                else:
                    return sprites_cobra[CORPO_VERTICAL]
            else:
                # Curva
                sprite_curva = sprites_cobra[CORPO_CURVA_LADO_BAIXO]
                
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

# Classe da Comida
class Comida:
    def __init__(self, cobra):
        self.posicao = self.gerar_posicao(cobra)

    def gerar_posicao(self, cobra):
        while True:
            x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
            y = random.randrange(0, ALTURA, TAMANHO_BLOCO)
            posicao = (x, y)
            # Verifica se a posição não está ocupada pela cobra
            if posicao not in cobra.posicao:
                return posicao

def mostrar_tela_final(pontuacao):
    tela.fill(PRETO)
    texto_fim = fonte_grande.render('Fim de Jogo!', True, BRANCO)
    texto_pontuacao = fonte.render(f'Pontuação Final: {pontuacao} maçãs', True, BRANCO)
    texto_menu = fonte.render('ESPAÇO - Menu Principal', True, BRANCO)
    texto_sair = fonte.render('ESC - Sair', True, BRANCO)
    
    rect_fim = texto_fim.get_rect(center=(LARGURA/2, ALTURA/2 - 80))
    rect_pontuacao = texto_pontuacao.get_rect(center=(LARGURA/2, ALTURA/2 - 20))
    rect_menu = texto_menu.get_rect(center=(LARGURA/2, ALTURA/2 + 80))
    rect_sair = texto_sair.get_rect(center=(LARGURA/2, ALTURA/2 + 120))
    
    tela.blit(texto_fim, rect_fim)
    tela.blit(texto_pontuacao, rect_pontuacao)
    tela.blit(texto_menu, rect_menu)
    tela.blit(texto_sair, rect_sair)
    pygame.display.update()

def jogar(velocidade=10):
    clock = pygame.time.Clock()
    cobra = Cobra()
    comida = Comida(cobra)
    pontuacao = 0
    rodando = True

    # Define o texto da dificuldade baseado na velocidade
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
                if evento.key == pygame.K_UP and cobra.direcao != [0, TAMANHO_BLOCO]:
                    cobra.direcao = [0, -TAMANHO_BLOCO]
                elif evento.key == pygame.K_DOWN and cobra.direcao != [0, -TAMANHO_BLOCO]:
                    cobra.direcao = [0, TAMANHO_BLOCO]
                elif evento.key == pygame.K_LEFT and cobra.direcao != [TAMANHO_BLOCO, 0]:
                    cobra.direcao = [-TAMANHO_BLOCO, 0]
                elif evento.key == pygame.K_RIGHT and cobra.direcao != [-TAMANHO_BLOCO, 0]:
                    cobra.direcao = [TAMANHO_BLOCO, 0]

        cobra.mover()

        if cobra.posicao[0] == comida.posicao:
            cobra.crescer()
            comida = Comida(cobra)
            pontuacao += 1

        if cobra.colisao():
            rodando = False

        tela.fill(PRETO)
        
        # Desenha a maçã usando a imagem
        tela.blit(imagem_maca, comida.posicao)
        
        # Desenha a cobra usando os sprites
        for i, posicao in enumerate(cobra.posicao):
            sprite = cobra.obter_sprite_parte(i)
            tela.blit(sprite, posicao)

        texto_pontuacao = fonte.render(f'Maçãs: {pontuacao}', True, BRANCO)
        texto_dificuldade = fonte.render(f'Dificuldade: {dificuldade_texto}', True, BRANCO)
        tela.blit(texto_pontuacao, (10, 10))
        tela.blit(texto_dificuldade, (LARGURA - texto_dificuldade.get_width() - 10, 10))

        pygame.display.update()
        clock.tick(velocidade)

    mostrar_tela_final(pontuacao)
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "jogar"
                elif evento.key == pygame.K_m:
                    return "menu"
                elif evento.key == pygame.K_ESCAPE:
                    return False
    return True

# Função principal do jogo
def main():
    jogando = True
    velocidade = 10
    
    while jogando:
        mostrar_menu()
        escolha_menu = None
        
        while escolha_menu is None:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        escolha_menu = "jogar"
                    elif evento.key == pygame.K_2:
                        escolha_menu = "dificuldade"
                    elif evento.key == pygame.K_3:
                        jogando = False
                        escolha_menu = "sair"
        
        if escolha_menu == "dificuldade":
            mostrar_dificuldade()
            escolha_dif = None
            
            while escolha_dif is None:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        return
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_1:
                            velocidade = 8
                            escolha_dif = "voltar"
                        elif evento.key == pygame.K_2:
                            velocidade = 10
                            escolha_dif = "voltar"
                        elif evento.key == pygame.K_3:
                            velocidade = 15
                            escolha_dif = "voltar"
                        elif evento.key == pygame.K_4:
                            escolha_dif = "voltar"
        
        elif escolha_menu == "jogar":
            resultado = jogar(velocidade)
            if resultado == False:
                jogando = False
            elif resultado == "jogar":
                continue
            elif resultado == "menu":
                continue

    pygame.quit()

if __name__ == "__main__":
    main()
