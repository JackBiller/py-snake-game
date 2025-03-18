import pygame
from code.const import *

def mostrar_menu(tela, fonte, fonte_grande):
    """
    Mostra o menu principal do jogo.
    
    Args:
        tela: Superfície do Pygame onde o menu será desenhado
        fonte: Fonte para textos normais
        fonte_grande: Fonte para textos grandes
    """
    opcao_selecionada = 0
    opcoes = ['JOGAR', 'DIFICULDADE', 'SAIR']
    
    while True:
        tela.fill(PRETO)
        titulo = fonte_grande.render('JOGO DA COBRINHA', True, VERDE)
        
        # Renderiza as opções com cores diferentes baseado na seleção
        for i, opcao in enumerate(opcoes):
            cor = AMARELO if i == opcao_selecionada else BRANCO
            texto = fonte.render(f'{opcao}', True, cor)
            rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
            tela.blit(texto, rect)
        
        rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/4))
        tela.blit(titulo, rect_titulo)
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

def mostrar_dificuldade(tela, fonte, fonte_grande):
    """
    Mostra o menu de seleção de dificuldade.
    
    Args:
        tela: Superfície do Pygame onde o menu será desenhado
        fonte: Fonte para textos normais
        fonte_grande: Fonte para textos grandes
    """
    opcao_selecionada = 0
    opcoes = ['FÁCIL', 'MÉDIO', 'DIFÍCIL', 'VOLTAR']
    
    while True:
        tela.fill(PRETO)
        titulo = fonte_grande.render('DIFICULDADE', True, VERDE)
        
        # Renderiza as opções com cores diferentes baseado na seleção
        for i, opcao in enumerate(opcoes):
            cor = AMARELO if i == opcao_selecionada else BRANCO
            texto = fonte.render(f'{opcao}', True, cor)
            rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + i * 50))
            tela.blit(texto, rect)
        
        rect_titulo = titulo.get_rect(center=(LARGURA/2, ALTURA/4))
        tela.blit(titulo, rect_titulo)
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

def mostrar_tela_final(tela, fonte, fonte_grande, pontuacao):
    """
    Mostra a tela de fim de jogo com a pontuação.
    
    Args:
        tela: Superfície do Pygame onde a tela será desenhada
        fonte: Fonte para textos normais
        fonte_grande: Fonte para textos grandes
        pontuacao: Pontuação final do jogador
    """
    opcao_selecionada = 0
    opcoes = ['MENU PRINCIPAL', 'JOGAR NOVAMENTE', 'SAIR']
    
    while True:
        tela.fill(PRETO)
        texto_fim = fonte_grande.render('Fim de Jogo!', True, BRANCO)
        texto_pontuacao = fonte.render(f'Pontuação Final: {pontuacao} maçãs', True, BRANCO)
        
        rect_fim = texto_fim.get_rect(center=(LARGURA/2, ALTURA/2 - 80))
        rect_pontuacao = texto_pontuacao.get_rect(center=(LARGURA/2, ALTURA/2 - 20))
        
        tela.blit(texto_fim, rect_fim)
        tela.blit(texto_pontuacao, rect_pontuacao)
        
        # Renderiza as opções com cores diferentes baseado na seleção
        for i, opcao in enumerate(opcoes):
            cor = AMARELO if i == opcao_selecionada else BRANCO
            texto = fonte.render(opcao, True, cor)
            rect = texto.get_rect(center=(LARGURA/2, ALTURA/2 + 80 + i * 50))
            tela.blit(texto, rect)
        
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