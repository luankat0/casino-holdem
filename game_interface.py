import pygame
from game_logic import Carta, Naipe

# Configurações
WIDTH, HEIGHT = 1400, 900
FPS = 60
CARD_WIDTH, CARD_HEIGHT = 70, 100

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
BLUE = (70, 130, 180)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class GameInterface:
    def __init__(self, game_logic):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Casino Hold'em - Análise Estatística")
        self.clock = pygame.time.Clock()
        self.game = game_logic
        
        # Fontes
        self.font_titulo = pygame.font.Font(None, 50)
        self.font_grande = pygame.font.Font(None, 36)
        self.font_medio = pygame.font.Font(None, 32)
        self.font_texto = pygame.font.Font(None, 28)
        self.font_pequeno = pygame.font.Font(None, 26)
        self.font_mini = pygame.font.Font(None, 22)
    
    def desenhar_carta(self, carta, x, y, virada=False):
        if virada:
            pygame.draw.rect(self.screen, BLUE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
            pygame.draw.rect(self.screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=5)
            text = self.font_grande.render("?", True, WHITE)
            self.screen.blit(text, (x + CARD_WIDTH//2 - 10, y + CARD_HEIGHT//2 - 15))
        else:
            pygame.draw.rect(self.screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
            pygame.draw.rect(self.screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=5)
            
            cor = RED if carta.naipe in [Naipe.COPAS, Naipe.OUROS] else BLACK
            
            text_valor = self.font_medio.render(carta.valor, True, cor)
            text_naipe = self.font_medio.render(carta.naipe.value, True, cor)
            
            self.screen.blit(text_valor, (x + 5, y + 5))
            self.screen.blit(text_naipe, (x + CARD_WIDTH//2 - 10, y + CARD_HEIGHT//2 - 15))
    
    def desenhar_tela(self):
        self.screen.fill(DARK_GREEN)
        
        # Título
        titulo = self.font_titulo.render("CASINO HOLD'EM", True, GOLD)
        self.screen.blit(titulo, (WIDTH//2 - 200, 20))
        
        # Fichas e Ante
        fichas_text = self.font_grande.render(f"Fichas: ${self.game.fichas}", True, WHITE)
        self.screen.blit(fichas_text, (50, 80))
        
        ante_text = self.font_grande.render(f"Ante: ${self.game.aposta_ante}", True, WHITE)
        self.screen.blit(ante_text, (50, 120))
        
        # Mão do Dealer
        dealer_label = self.font_texto.render("DEALER", True, WHITE)
        self.screen.blit(dealer_label, (WIDTH//2 - 40, 150))
        
        if self.game.fase == "FIM":
            for i, carta in enumerate(self.game.mao_dealer):
                self.desenhar_carta(carta, WIDTH//2 - 80 + i * 90, 180)
        elif self.game.fase != "INICIO":
            for i in range(2):
                self.desenhar_carta(None, WIDTH//2 - 80 + i * 90, 180, virada=True)
        
        # Cartas Comunitárias
        if len(self.game.cartas_comunitarias) > 0:
            comunitarias_label = self.font_texto.render("MESA", True, WHITE)
            self.screen.blit(comunitarias_label, (WIDTH//2 - 30, 330))
            
            for i, carta in enumerate(self.game.cartas_comunitarias):
                self.desenhar_carta(carta, WIDTH//2 - 190 + i * 90, 360)
        
        # Mão do Jogador
        jogador_label = self.font_texto.render("VOCÊ", True, GOLD)
        self.screen.blit(jogador_label, (WIDTH//2 - 30, 520))
        
        if len(self.game.mao_jogador) > 0:
            for i, carta in enumerate(self.game.mao_jogador):
                self.desenhar_carta(carta, WIDTH//2 - 80 + i * 90, 550)
        
        # Mensagem
        msg = self.font_texto.render(self.game.mensagem, True, WHITE)
        msg_rect = msg.get_rect(center=(WIDTH//2, 680))
        self.screen.blit(msg, msg_rect)
        
        # Botões
        self.desenhar_botoes()
        
        # Painel de Análise Estatística
        self.desenhar_painel_stats()
        
        # Histórico
        self.desenhar_historico()
        
        pygame.display.flip()
    
    def desenhar_botoes(self):
        if self.game.fase == "INICIO" or self.game.fase == "FIM":
            btn_nova = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            pygame.draw.rect(self.screen, GREEN, btn_nova, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_nova, 3, border_radius=10)
            text = self.font_medio.render("NOVA RODADA", True, WHITE)
            self.screen.blit(text, (btn_nova.x + 20, btn_nova.y + 12))
        
        elif self.game.fase == "PRE_FLOP":
            btn_call = pygame.Rect(WIDTH//2 - 220, 730, 150, 50)
            btn_fold = pygame.Rect(WIDTH//2 + 70, 730, 150, 50)
            
            pygame.draw.rect(self.screen, GREEN, btn_call, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_call, 3, border_radius=10)
            text_call = self.font_medio.render("CALL", True, WHITE)
            self.screen.blit(text_call, (btn_call.x + 40, btn_call.y + 12))
            
            pygame.draw.rect(self.screen, RED, btn_fold, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_fold, 3, border_radius=10)
            text_fold = self.font_medio.render("FOLD", True, WHITE)
            self.screen.blit(text_fold, (btn_fold.x + 40, btn_fold.y + 12))
        
        elif self.game.fase in ["FLOP", "TURN", "RIVER"]:
            btn_next = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            pygame.draw.rect(self.screen, GREEN, btn_next, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_next, 3, border_radius=10)
            text_next = self.font_medio.render("CONTINUAR", True, WHITE)
            self.screen.blit(text_next, (btn_next.x + 30, btn_next.y + 12))
    
    def desenhar_painel_stats(self):
        if not self.game.stats or self.game.fase not in ["PRE_FLOP", "FLOP", "TURN", "RIVER"]:
            return
        
        # Painel
        painel_x, painel_y = WIDTH - 380, 80
        painel_w, painel_h = 360, 400
        
        pygame.draw.rect(self.screen, (20, 60, 20), (painel_x, painel_y, painel_w, painel_h), border_radius=15)
        pygame.draw.rect(self.screen, GOLD, (painel_x, painel_y, painel_w, painel_h), 3, border_radius=15)
        
        # Título
        titulo = self.font_medio.render("ANÁLISE ESTATÍSTICA", True, GOLD)
        self.screen.blit(titulo, (painel_x + 30, painel_y + 15))
        
        y_offset = painel_y + 60
        
        # Mão Atual
        mao_text = self.font_pequeno.render(f"Mão: {self.game.stats['tipo_mao']}", True, WHITE)
        self.screen.blit(mao_text, (painel_x + 20, y_offset))
        y_offset += 40
        
        # Barras de Probabilidade
        vitoria = self.game.stats['vitoria']
        empate = self.game.stats['empate']
        derrota = self.game.stats['derrota']
        
        # Barra Vitória
        pygame.draw.rect(self.screen, LIGHT_GRAY, (painel_x + 20, y_offset, 320, 30), border_radius=5)
        if vitoria > 0:
            largura_vitoria = int(320 * vitoria / 100)
            pygame.draw.rect(self.screen, GREEN, (painel_x + 20, y_offset, largura_vitoria, 30), border_radius=5)
        text_v = self.font_mini.render(f"Vitória: {vitoria}%", True, WHITE)
        self.screen.blit(text_v, (painel_x + 30, y_offset + 5))
        y_offset += 40
        
        # Barra Empate
        pygame.draw.rect(self.screen, LIGHT_GRAY, (painel_x + 20, y_offset, 320, 30), border_radius=5)
        if empate > 0:
            largura_empate = int(320 * empate / 100)
            pygame.draw.rect(self.screen, GOLD, (painel_x + 20, y_offset, largura_empate, 30), border_radius=5)
        text_e = self.font_mini.render(f"Empate: {empate}%", True, WHITE)
        self.screen.blit(text_e, (painel_x + 30, y_offset + 5))
        y_offset += 40
        
        # Barra Derrota
        pygame.draw.rect(self.screen, LIGHT_GRAY, (painel_x + 20, y_offset, 320, 30), border_radius=5)
        if derrota > 0:
            largura_derrota = int(320 * derrota / 100)
            pygame.draw.rect(self.screen, RED, (painel_x + 20, y_offset, largura_derrota, 30), border_radius=5)
        text_d = self.font_mini.render(f"Derrota: {derrota}%", True, WHITE)
        self.screen.blit(text_d, (painel_x + 30, y_offset + 5))
        y_offset += 50
        
        # Outs
        outs_text = self.font_pequeno.render(f"Outs: {self.game.stats['outs']} cartas", True, WHITE)
        self.screen.blit(outs_text, (painel_x + 20, y_offset))
        y_offset += 35
        
        # Categoria de Força
        if vitoria >= 70:
            categoria = "MUITO FORTE"
            cor_cat = GREEN
        elif vitoria >= 50:
            categoria = "FORTE"
            cor_cat = (100, 200, 100)
        elif vitoria >= 35:
            categoria = "MÉDIA"
            cor_cat = GOLD
        else:
            categoria = "FRACA"
            cor_cat = RED
        
        cat_text = self.font_pequeno.render(f"Força: {categoria}", True, cor_cat)
        self.screen.blit(cat_text, (painel_x + 20, y_offset))
        y_offset += 40
        
        # Fase do Jogo
        fase_text = self.font_mini.render(f"Fase: {self.game.fase}", True, LIGHT_GRAY)
        self.screen.blit(fase_text, (painel_x + 20, y_offset))
    
    def desenhar_historico(self):
        if not self.game.historico:
            return
        
        hist_x, hist_y = 50, 180
        hist_w, hist_h = 280, 320
        
        pygame.draw.rect(self.screen, (20, 60, 20), (hist_x, hist_y, hist_w, hist_h), border_radius=10)
        pygame.draw.rect(self.screen, GOLD, (hist_x, hist_y, hist_w, hist_h), 2, border_radius=10)
        
        titulo = self.font_texto.render("HISTÓRICO", True, GOLD)
        self.screen.blit(titulo, (hist_x + 80, hist_y + 10))
        
        y_offset = hist_y + 45
        
        for entrada in self.game.historico[:5]:
            resultado = entrada['resultado']
            ganho = entrada['ganho']
            
            cor = GREEN if ganho > 0 else (WHITE if ganho == 0 else RED)
            
            text_res = self.font_mini.render(resultado[:20], True, cor)
            self.screen.blit(text_res, (hist_x + 10, y_offset))
            
            ganho_str = f"+${ganho}" if ganho > 0 else f"${ganho}"
            text_ganho = self.font_mini.render(ganho_str, True, cor)
            self.screen.blit(text_ganho, (hist_x + hist_w - 70, y_offset))
            
            y_offset += 30
        
        # Estatísticas Gerais
        y_offset += 20
        pygame.draw.line(self.screen, GOLD, (hist_x + 10, y_offset), (hist_x + hist_w - 10, y_offset), 2)
        y_offset += 15
        
        taxa_vitoria = self.game.get_taxa_vitoria()
        
        text_jogos = self.font_mini.render(f"Jogos: {self.game.total_jogos}", True, WHITE)
        self.screen.blit(text_jogos, (hist_x + 10, y_offset))
        y_offset += 25
        
        text_taxa = self.font_mini.render(f"Taxa: {taxa_vitoria:.1f}%", True, GREEN if taxa_vitoria >= 50 else RED)
        self.screen.blit(text_taxa, (hist_x + 10, y_offset))
    
    def processar_click(self, pos):
        if self.game.fase == "INICIO" or self.game.fase == "FIM":
            btn_nova = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            if btn_nova.collidepoint(pos):
                self.game.iniciar_rodada()
        
        elif self.game.fase == "PRE_FLOP":
            btn_call = pygame.Rect(WIDTH//2 - 220, 730, 150, 50)
            btn_fold = pygame.Rect(WIDTH//2 + 70, 730, 150, 50)
            
            if btn_call.collidepoint(pos):
                self.game.call()
            elif btn_fold.collidepoint(pos):
                self.game.fold()
        
        elif self.game.fase in ["FLOP", "TURN", "RIVER"]:
            btn_next = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            if btn_next.collidepoint(pos):
                self.game.call()
    
    def get_clock(self):
        return self.clock
    
    def get_fps(self):
        return FPS