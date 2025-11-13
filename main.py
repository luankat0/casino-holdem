import pygame
import random
from enum import Enum
from collections import Counter
import itertools

pygame.init()

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

class Naipe(Enum):
    PAUS = "♣"
    OUROS = "♦"
    COPAS = "♥"
    ESPADAS = "♠"

class TipoMao(Enum):
    CARTA_ALTA = (0, "Carta Alta")
    PAR = (1, "Par")
    DOIS_PARES = (2, "Dois Pares")
    TRINCA = (3, "Trinca")
    SEQUENCIA = (4, "Sequência")
    FLUSH = (5, "Flush")
    FULL_HOUSE = (6, "Full House")
    QUADRA = (7, "Quadra")
    STRAIGHT_FLUSH = (8, "Straight Flush")
    ROYAL_FLUSH = (9, "Royal Flush")
    
    def __lt__(self, other):
        return self.value[0] < other.value[0]

class Carta:
    VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
        self.valor_numerico = self.VALORES.index(valor) + 2
    
    def __repr__(self):
        return f"{self.valor}{self.naipe.value}"
    
    def desenhar(self, screen, x, y, virada=False):
        if virada:
            pygame.draw.rect(screen, BLUE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
            pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=5)
            font = pygame.font.Font(None, 40)
            text = font.render("?", True, WHITE)
            screen.blit(text, (x + CARD_WIDTH//2 - 10, y + CARD_HEIGHT//2 - 15))
        else:
            pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=5)
            pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=5)
            
            cor = RED if self.naipe in [Naipe.COPAS, Naipe.OUROS] else BLACK
            font = pygame.font.Font(None, 30)
            text_valor = font.render(self.valor, True, cor)
            text_naipe = font.render(self.naipe.value, True, cor)
            
            screen.blit(text_valor, (x + 5, y + 5))
            screen.blit(text_naipe, (x + CARD_WIDTH//2 - 10, y + CARD_HEIGHT//2 - 15))

class Baralho:
    def __init__(self):
        self.cartas = [Carta(valor, naipe) for naipe in Naipe for valor in Carta.VALORES]
        self.embaralhar()
    
    def embaralhar(self):
        random.shuffle(self.cartas)
    
    def dar_carta(self):
        return self.cartas.pop() if self.cartas else None

class AvaliadorMao:
    @staticmethod
    def avaliar_mao(cartas):
        if len(cartas) < 5:
            return (TipoMao.CARTA_ALTA, [c.valor_numerico for c in sorted(cartas, key=lambda x: x.valor_numerico, reverse=True)])
        
        melhor_mao = None
        melhor_tipo = TipoMao.CARTA_ALTA
        
        for combinacao in itertools.combinations(cartas, 5):
            tipo, valores = AvaliadorMao._avaliar_5_cartas(list(combinacao))
            if tipo > melhor_tipo or (tipo == melhor_tipo and valores > (melhor_mao[1] if melhor_mao else [])):
                melhor_tipo = tipo
                melhor_mao = (tipo, valores)
        
        return melhor_mao
    
    @staticmethod
    def _avaliar_5_cartas(cartas):
        valores = sorted([c.valor_numerico for c in cartas], reverse=True)
        naipes = [c.naipe for c in cartas]
        contagem_valores = Counter(valores)
        contagem_naipes = Counter(naipes)
        
        is_flush = len(contagem_naipes) == 1
        is_straight = AvaliadorMao._is_sequencia(valores)
        
        if is_straight and is_flush:
            if valores[0] == 14:
                return (TipoMao.ROYAL_FLUSH, valores)
            return (TipoMao.STRAIGHT_FLUSH, valores)
        
        contagens = sorted(contagem_valores.values(), reverse=True)
        
        if contagens[0] == 4:
            return (TipoMao.QUADRA, valores)
        if contagens[0] == 3 and contagens[1] == 2:
            return (TipoMao.FULL_HOUSE, valores)
        if is_flush:
            return (TipoMao.FLUSH, valores)
        if is_straight:
            return (TipoMao.SEQUENCIA, valores)
        if contagens[0] == 3:
            return (TipoMao.TRINCA, valores)
        if contagens[0] == 2 and contagens[1] == 2:
            return (TipoMao.DOIS_PARES, valores)
        if contagens[0] == 2:
            return (TipoMao.PAR, valores)
        
        return (TipoMao.CARTA_ALTA, valores)
    
    @staticmethod
    def _is_sequencia(valores):
        if valores == [14, 5, 4, 3, 2]:
            return True
        for i in range(len(valores) - 1):
            if valores[i] - valores[i+1] != 1:
                return False
        return True

class CalculadorProbabilidades:
    @staticmethod
    def calcular_equity(mao_jogador, cartas_comunitarias, num_simulacoes=1000):
        cartas_conhecidas = mao_jogador + cartas_comunitarias
        baralho_restante = [Carta(v, n) for n in Naipe for v in Carta.VALORES 
                           if not any(c.valor == v and c.naipe == n for c in cartas_conhecidas)]
        
        vitorias = empates = derrotas = 0
        cartas_faltantes = 5 - len(cartas_comunitarias)
        
        for _ in range(num_simulacoes):
            random.shuffle(baralho_restante)
            
            cartas_simuladas = cartas_comunitarias + baralho_restante[:cartas_faltantes]
            mao_dealer = baralho_restante[cartas_faltantes:cartas_faltantes+2]
            
            mao_jogador_completa = mao_jogador + cartas_simuladas
            mao_dealer_completa = mao_dealer + cartas_simuladas
            
            tipo_jogador, valores_jogador = AvaliadorMao.avaliar_mao(mao_jogador_completa)
            tipo_dealer, valores_dealer = AvaliadorMao.avaliar_mao(mao_dealer_completa)
            
            if tipo_jogador > tipo_dealer or (tipo_jogador == tipo_dealer and valores_jogador > valores_dealer):
                vitorias += 1
            elif tipo_jogador == tipo_dealer and valores_jogador == valores_dealer:
                empates += 1
            else:
                derrotas += 1
        
        return {
            'vitoria': round(vitorias / num_simulacoes * 100, 1),
            'empate': round(empates / num_simulacoes * 100, 1),
            'derrota': round(derrotas / num_simulacoes * 100, 1)
        }
    
    @staticmethod
    def calcular_outs(mao_jogador, cartas_comunitarias):
        if len(cartas_comunitarias) >= 5:
            return 0
        
        cartas_conhecidas = mao_jogador + cartas_comunitarias
        tipo_atual, _ = AvaliadorMao.avaliar_mao(cartas_conhecidas) if len(cartas_conhecidas) >= 5 else (TipoMao.CARTA_ALTA, [])
        
        baralho_restante = [Carta(v, n) for n in Naipe for v in Carta.VALORES 
                           if not any(c.valor == v and c.naipe == n for c in cartas_conhecidas)]
        
        outs = 0
        for carta in baralho_restante:
            novas_cartas = cartas_conhecidas + [carta]
            if len(novas_cartas) >= 5:
                novo_tipo, _ = AvaliadorMao.avaliar_mao(novas_cartas)
                if novo_tipo > tipo_atual:
                    outs += 1
        
        return outs

class Jogo:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Casino Hold'em - Análise Estatística")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.fichas = 1000
        self.aposta_ante = 10
        self.baralho = None
        self.mao_jogador = []
        self.mao_dealer = []
        self.cartas_comunitarias = []
        self.fase = "INICIO"
        self.mensagem = "Bem-vindo ao Casino Hold'em!"
        
        self.historico = []
        self.total_jogos = 0
        self.total_vitorias = 0
        
        self.stats = None
        
    def iniciar_rodada(self):
        if self.fichas < self.aposta_ante * 2:
            self.mensagem = "Fichas insuficientes!"
            return
        
        self.baralho = Baralho()
        self.mao_jogador = [self.baralho.dar_carta() for _ in range(2)]
        self.mao_dealer = [self.baralho.dar_carta() for _ in range(2)]
        self.cartas_comunitarias = []
        self.fichas -= self.aposta_ante
        self.fase = "PRE_FLOP"
        self.mensagem = "Suas cartas foram distribuídas. CALL (2x ante) ou FOLD?"
        self.atualizar_stats()
    
    def call(self):
        if self.fase == "PRE_FLOP":
            if self.fichas < self.aposta_ante * 2:
                self.mensagem = "Fichas insuficientes para CALL!"
                return
            self.fichas -= self.aposta_ante * 2
            self.fase = "FLOP"
            self.cartas_comunitarias = [self.baralho.dar_carta() for _ in range(3)]
            self.mensagem = "FLOP revelado. Aguardando TURN..."
            self.atualizar_stats()
        elif self.fase == "FLOP":
            self.fase = "TURN"
            self.cartas_comunitarias.append(self.baralho.dar_carta())
            self.mensagem = "TURN revelado. Aguardando RIVER..."
            self.atualizar_stats()
        elif self.fase == "TURN":
            self.fase = "RIVER"
            self.cartas_comunitarias.append(self.baralho.dar_carta())
            self.mensagem = "RIVER revelado. Aguardando SHOWDOWN..."
            self.atualizar_stats()
        elif self.fase == "RIVER":
            self.showdown()
    
    def fold(self):
        if self.fase == "PRE_FLOP":
            self.mensagem = f"Você desistiu. Perdeu {self.aposta_ante} fichas."
            self.adicionar_historico("FOLD", -self.aposta_ante)
            self.fase = "FIM"
    
    def showdown(self):
        mao_jogador_completa = self.mao_jogador + self.cartas_comunitarias
        mao_dealer_completa = self.mao_dealer + self.cartas_comunitarias
        
        tipo_jogador, valores_jogador = AvaliadorMao.avaliar_mao(mao_jogador_completa)
        tipo_dealer, valores_dealer = AvaliadorMao.avaliar_mao(mao_dealer_completa)
        
        total_apostado = self.aposta_ante * 3
        
        # Verificar se dealer qualifica (par de 4s ou melhor)
        dealer_qualifica = tipo_dealer >= TipoMao.PAR and (tipo_dealer > TipoMao.PAR or valores_dealer[0] >= 4)
        
        if not dealer_qualifica:
            ganho = self.aposta_ante * 2
            self.fichas += total_apostado + ganho
            self.mensagem = f"Dealer não qualificou! Você ganhou {ganho} fichas. {tipo_jogador.value[1]}"
            self.adicionar_historico("VITÓRIA (Dealer não qualificou)", ganho)
        elif tipo_jogador > tipo_dealer or (tipo_jogador == tipo_dealer and valores_jogador > valores_dealer):
            ganho = self.aposta_ante * 2
            self.fichas += total_apostado + ganho
            self.mensagem = f"Você venceu! Ganhou {ganho} fichas. {tipo_jogador.value[1]} vs {tipo_dealer.value[1]}"
            self.adicionar_historico("VITÓRIA", ganho)
        elif tipo_jogador == tipo_dealer and valores_jogador == valores_dealer:
            self.fichas += total_apostado
            self.mensagem = f"Empate! Apostas devolvidas. {tipo_jogador.value[1]}"
            self.adicionar_historico("EMPATE", 0)
        else:
            self.mensagem = f"Dealer venceu. Perdeu {total_apostado} fichas. {tipo_dealer.value[1]} vs {tipo_jogador.value[1]}"
            self.adicionar_historico("DERROTA", -total_apostado)
        
        self.fase = "FIM"
    
    def adicionar_historico(self, resultado, ganho):
        self.historico.insert(0, {"resultado": resultado, "ganho": ganho})
        if len(self.historico) > 5:
            self.historico.pop()
        
        self.total_jogos += 1
        if ganho > 0:
            self.total_vitorias += 1
    
    def atualizar_stats(self):
        if len(self.mao_jogador) > 0 and self.fase in ["PRE_FLOP", "FLOP", "TURN", "RIVER"]:
            self.stats = CalculadorProbabilidades.calcular_equity(
                self.mao_jogador, self.cartas_comunitarias, num_simulacoes=500
            )
            tipo_atual, _ = AvaliadorMao.avaliar_mao(self.mao_jogador + self.cartas_comunitarias)
            self.stats['tipo_mao'] = tipo_atual.value[1]
            self.stats['outs'] = CalculadorProbabilidades.calcular_outs(self.mao_jogador, self.cartas_comunitarias)
    
    def desenhar(self):
        self.screen.fill(DARK_GREEN)
        
        # Título
        font_titulo = pygame.font.Font(None, 50)
        titulo = font_titulo.render("CASINO HOLD'EM", True, GOLD)
        self.screen.blit(titulo, (WIDTH//2 - 200, 20))
        
        # Fichas
        font = pygame.font.Font(None, 36)
        fichas_text = font.render(f"Fichas: ${self.fichas}", True, WHITE)
        self.screen.blit(fichas_text, (50, 80))
        
        # Ante
        ante_text = font.render(f"Ante: ${self.aposta_ante}", True, WHITE)
        self.screen.blit(ante_text, (50, 120))
        
        # Mão do Dealer
        font_label = pygame.font.Font(None, 28)
        dealer_label = font_label.render("DEALER", True, WHITE)
        self.screen.blit(dealer_label, (WIDTH//2 - 40, 150))
        
        if self.fase == "FIM":
            for i, carta in enumerate(self.mao_dealer):
                carta.desenhar(self.screen, WIDTH//2 - 80 + i * 90, 180)
        elif self.fase != "INICIO":
            for i in range(2):
                Carta('A', Naipe.ESPADAS).desenhar(self.screen, WIDTH//2 - 80 + i * 90, 180, virada=True)
        
        # Cartas Comunitárias
        if len(self.cartas_comunitarias) > 0:
            comunitarias_label = font_label.render("MESA", True, WHITE)
            self.screen.blit(comunitarias_label, (WIDTH//2 - 30, 330))
            
            for i, carta in enumerate(self.cartas_comunitarias):
                carta.desenhar(self.screen, WIDTH//2 - 190 + i * 90, 360)
        
        # Mão do Jogador
        jogador_label = font_label.render("VOCÊ", True, GOLD)
        self.screen.blit(jogador_label, (WIDTH//2 - 30, 520))
        
        if len(self.mao_jogador) > 0:
            for i, carta in enumerate(self.mao_jogador):
                carta.desenhar(self.screen, WIDTH//2 - 80 + i * 90, 550)
        
        # Mensagem
        font_msg = pygame.font.Font(None, 28)
        msg = font_msg.render(self.mensagem, True, WHITE)
        self.screen.blit(msg, (WIDTH//2 - len(self.mensagem) * 6, 680))
        
        # Botões
        self.desenhar_botoes()
        
        # Painel de Análise Estatística
        self.desenhar_painel_stats()
        
        # Histórico
        self.desenhar_historico()
        
        pygame.display.flip()
    
    def desenhar_botoes(self):
        font = pygame.font.Font(None, 32)
        
        if self.fase == "INICIO" or self.fase == "FIM":
            btn_nova = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            pygame.draw.rect(self.screen, GREEN, btn_nova, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_nova, 3, border_radius=10)
            text = font.render("NOVA RODADA", True, WHITE)
            self.screen.blit(text, (btn_nova.x + 20, btn_nova.y + 12))
        
        elif self.fase == "PRE_FLOP":
            btn_call = pygame.Rect(WIDTH//2 - 220, 730, 150, 50)
            btn_fold = pygame.Rect(WIDTH//2 + 70, 730, 150, 50)
            
            pygame.draw.rect(self.screen, GREEN, btn_call, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_call, 3, border_radius=10)
            text_call = font.render("CALL", True, WHITE)
            self.screen.blit(text_call, (btn_call.x + 40, btn_call.y + 12))
            
            pygame.draw.rect(self.screen, RED, btn_fold, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_fold, 3, border_radius=10)
            text_fold = font.render("FOLD", True, WHITE)
            self.screen.blit(text_fold, (btn_fold.x + 40, btn_fold.y + 12))
        
        elif self.fase in ["FLOP", "TURN", "RIVER"]:
            btn_next = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            pygame.draw.rect(self.screen, GREEN, btn_next, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, btn_next, 3, border_radius=10)
            text_next = font.render("CONTINUAR", True, WHITE)
            self.screen.blit(text_next, (btn_next.x + 30, btn_next.y + 12))
    
    def desenhar_painel_stats(self):
        if not self.stats or self.fase not in ["PRE_FLOP", "FLOP", "TURN", "RIVER"]:
            return
        
        # Painel
        painel_x, painel_y = WIDTH - 380, 80
        painel_w, painel_h = 360, 400
        
        pygame.draw.rect(self.screen, (20, 60, 20), (painel_x, painel_y, painel_w, painel_h), border_radius=15)
        pygame.draw.rect(self.screen, GOLD, (painel_x, painel_y, painel_w, painel_h), 3, border_radius=15)
        
        font_titulo = pygame.font.Font(None, 32)
        font_texto = pygame.font.Font(None, 26)
        font_peq = pygame.font.Font(None, 22)
        
        # Título
        titulo = font_titulo.render("ANÁLISE ESTATÍSTICA", True, GOLD)
        self.screen.blit(titulo, (painel_x + 30, painel_y + 15))
        
        y_offset = painel_y + 60
        
        # Mão Atual
        mao_text = font_texto.render(f"Mão: {self.stats['tipo_mao']}", True, WHITE)
        self.screen.blit(mao_text, (painel_x + 20, y_offset))
        y_offset += 40
        
        # Barras de Probabilidade
        vitoria = self.stats['vitoria']
        empate = self.stats['empate']
        derrota = self.stats['derrota']
        
        # Barra Vitória
        pygame.draw.rect(self.screen, LIGHT_GRAY, (painel_x + 20, y_offset, 320, 30), border_radius=5)
        if vitoria > 0:
            largura_vitoria = int(320 * vitoria / 100)
            pygame.draw.rect(self.screen, GREEN, (painel_x + 20, y_offset, largura_vitoria, 30), border_radius=5)
        text_v = font_peq.render(f"Vitória: {vitoria}%", True, WHITE)
        self.screen.blit(text_v, (painel_x + 30, y_offset + 5))
        y_offset += 40
        
        # Barra Empate
        pygame.draw.rect(self.screen, LIGHT_GRAY, (painel_x + 20, y_offset, 320, 30), border_radius=5)
        if empate > 0:
            largura_empate = int(320 * empate / 100)
            pygame.draw.rect(self.screen, GOLD, (painel_x + 20, y_offset, largura_empate, 30), border_radius=5)
        text_e = font_peq.render(f"Empate: {empate}%", True, WHITE)
        self.screen.blit(text_e, (painel_x + 30, y_offset + 5))
        y_offset += 40
        
        # Barra Derrota
        pygame.draw.rect(self.screen, LIGHT_GRAY, (painel_x + 20, y_offset, 320, 30), border_radius=5)
        if derrota > 0:
            largura_derrota = int(320 * derrota / 100)
            pygame.draw.rect(self.screen, RED, (painel_x + 20, y_offset, largura_derrota, 30), border_radius=5)
        text_d = font_peq.render(f"Derrota: {derrota}%", True, WHITE)
        self.screen.blit(text_d, (painel_x + 30, y_offset + 5))
        y_offset += 50
        
        # Outs
        outs_text = font_texto.render(f"Outs: {self.stats['outs']} cartas", True, WHITE)
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
        
        cat_text = font_texto.render(f"Força: {categoria}", True, cor_cat)
        self.screen.blit(cat_text, (painel_x + 20, y_offset))
        y_offset += 40
        
        # Fase do Jogo
        fase_text = font_peq.render(f"Fase: {self.fase}", True, LIGHT_GRAY)
        self.screen.blit(fase_text, (painel_x + 20, y_offset))
    
    def desenhar_historico(self):
        if not self.historico:
            return
        
        hist_x, hist_y = 50, 180
        hist_w, hist_h = 280, 320
        
        pygame.draw.rect(self.screen, (20, 60, 20), (hist_x, hist_y, hist_w, hist_h), border_radius=10)
        pygame.draw.rect(self.screen, GOLD, (hist_x, hist_y, hist_w, hist_h), 2, border_radius=10)
        
        font_titulo = pygame.font.Font(None, 28)
        font_texto = pygame.font.Font(None, 22)
        
        titulo = font_titulo.render("HISTÓRICO", True, GOLD)
        self.screen.blit(titulo, (hist_x + 80, hist_y + 10))
        
        y_offset = hist_y + 45
        
        for entrada in self.historico[:5]:
            resultado = entrada['resultado']
            ganho = entrada['ganho']
            
            cor = GREEN if ganho > 0 else (WHITE if ganho == 0 else RED)
            
            text_res = font_texto.render(resultado[:20], True, cor)
            self.screen.blit(text_res, (hist_x + 10, y_offset))
            
            ganho_str = f"+${ganho}" if ganho > 0 else f"${ganho}"
            text_ganho = font_texto.render(ganho_str, True, cor)
            self.screen.blit(text_ganho, (hist_x + hist_w - 70, y_offset))
            
            y_offset += 30
        
        # Estatísticas Gerais
        y_offset += 20
        pygame.draw.line(self.screen, GOLD, (hist_x + 10, y_offset), (hist_x + hist_w - 10, y_offset), 2)
        y_offset += 15
        
        taxa_vitoria = (self.total_vitorias / self.total_jogos * 100) if self.total_jogos > 0 else 0
        
        text_jogos = font_texto.render(f"Jogos: {self.total_jogos}", True, WHITE)
        self.screen.blit(text_jogos, (hist_x + 10, y_offset))
        y_offset += 25
        
        text_taxa = font_texto.render(f"Taxa: {taxa_vitoria:.1f}%", True, GREEN if taxa_vitoria >= 50 else RED)
        self.screen.blit(text_taxa, (hist_x + 10, y_offset))
    
    def processar_click(self, pos):
        if self.fase == "INICIO" or self.fase == "FIM":
            btn_nova = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            if btn_nova.collidepoint(pos):
                self.iniciar_rodada()
        
        elif self.fase == "PRE_FLOP":
            btn_call = pygame.Rect(WIDTH//2 - 220, 730, 150, 50)
            btn_fold = pygame.Rect(WIDTH//2 + 70, 730, 150, 50)
            
            if btn_call.collidepoint(pos):
                self.call()
            elif btn_fold.collidepoint(pos):
                self.fold()
        
        elif self.fase in ["FLOP", "TURN", "RIVER"]:
            btn_next = pygame.Rect(WIDTH//2 - 100, 730, 200, 50)
            if btn_next.collidepoint(pos):
                self.call()
    
    def executar(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.processar_click(event.pos)
            
            self.desenhar()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()