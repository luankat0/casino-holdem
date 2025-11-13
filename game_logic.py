import random
from enum import Enum
from collections import Counter
import itertools

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
    
    def __le__(self, other):
        return self.value[0] <= other.value[0]

    def __gt__(self, other):
        return self.value[0] > other.value[0]

    def __ge__(self, other):
        return self.value[0] >= other.value[0]

    def __eq__(self, other):
        if isinstance(other, TipoMao):
            return self.value[0] == other.value[0]
        return False

class Carta:
    VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
        self.valor_numerico = self.VALORES.index(valor) + 2
    
    def __repr__(self):
        return f"{self.valor}{self.naipe.value}"

class Baralho:
    def __init__(self):
        self.cartas = [Carta(valor, naipe) for naipe in Naipe for valor in Carta.VALORES]
        self.embaralhar()
    
    def embaralhar(self):
        random.shuffle(self.cartas)
    
    def dar_carta(self):
        if len(self.cartas) == 0:
            return None
        return self.cartas.pop()
    
    def cartas_restantes(self):
        return len(self.cartas)

class AvaliadorMao:
    @staticmethod
    def avaliar_mao(cartas):
        if len(cartas) < 5:
            cartas_ordenadas = sorted(cartas, key=lambda x: x.valor_numerico, reverse=True)
            return (TipoMao.CARTA_ALTA, [c.valor_numerico for c in cartas_ordenadas])
        
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
        if not mao_jogador or len(mao_jogador) == 0:
            return {'vitoria': 0, 'empate': 0, 'derrota': 100}
        
        cartas_conhecidas = mao_jogador + cartas_comunitarias
        baralho_restante = [Carta(v, n) for n in Naipe for v in Carta.VALORES 
                           if not any(c.valor == v and c.naipe == n for c in cartas_conhecidas)]
        
        if len(baralho_restante) < 7:
            return {'vitoria': 50, 'empate': 10, 'derrota': 40}
        
        vitorias = empates = derrotas = 0
        cartas_faltantes = 5 - len(cartas_comunitarias)
        
        for _ in range(num_simulacoes):
            random.shuffle(baralho_restante)
            
            # Garantir que temos cartas suficientes
            if len(baralho_restante) < cartas_faltantes + 2:
                continue
            
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
        
        total = vitorias + empates + derrotas
        if total == 0:
            return {'vitoria': 33.3, 'empate': 33.3, 'derrota': 33.4}
        
        return {
            'vitoria': round(vitorias / total * 100, 1),
            'empate': round(empates / total * 100, 1),
            'derrota': round(derrotas / total * 100, 1)
        }
    
    @staticmethod
    def calcular_outs(mao_jogador, cartas_comunitarias):
        if len(cartas_comunitarias) >= 5 or not mao_jogador:
            return 0
        
        cartas_conhecidas = mao_jogador + cartas_comunitarias
        
        if len(cartas_conhecidas) < 5:
            tipo_atual = TipoMao.CARTA_ALTA
        else:
            tipo_atual, _ = AvaliadorMao.avaliar_mao(cartas_conhecidas)
        
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

class GameLogic:
    def __init__(self):
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
            return False
        
        self.baralho = Baralho()
        self.mao_jogador = [self.baralho.dar_carta() for _ in range(2)]
        self.mao_dealer = [self.baralho.dar_carta() for _ in range(2)]
        self.cartas_comunitarias = []
        self.fichas -= self.aposta_ante
        self.fase = "PRE_FLOP"
        self.mensagem = "Suas cartas foram distribuídas. CALL (2x ante) ou FOLD?"
        self.atualizar_stats()
        return True
    
    def call(self):
        if self.fase == "PRE_FLOP":
            if self.fichas < self.aposta_ante * 2:
                self.mensagem = "Fichas insuficientes para CALL!"
                return
            self.fichas -= self.aposta_ante * 2
            self.fase = "FLOP"
            
            # Verificar se há cartas suficientes
            if self.baralho.cartas_restantes() < 5:
                self.mensagem = "Erro: cartas insuficientes no baralho!"
                self.fase = "FIM"
                return
            
            self.cartas_comunitarias = [self.baralho.dar_carta() for _ in range(3)]
            self.mensagem = "FLOP revelado. Clique em CONTINUAR para o TURN."
            self.atualizar_stats()
            
        elif self.fase == "FLOP":
            if self.baralho.cartas_restantes() < 1:
                self.mensagem = "Erro: cartas insuficientes no baralho!"
                self.fase = "FIM"
                return
            
            self.fase = "TURN"
            self.cartas_comunitarias.append(self.baralho.dar_carta())
            self.mensagem = "TURN revelado. Clique em CONTINUAR para o RIVER."
            self.atualizar_stats()
            
        elif self.fase == "TURN":
            if self.baralho.cartas_restantes() < 1:
                self.mensagem = "Erro: cartas insuficientes no baralho!"
                self.fase = "FIM"
                return
            
            self.fase = "RIVER"
            self.cartas_comunitarias.append(self.baralho.dar_carta())
            self.mensagem = "RIVER revelado. Clique em CONTINUAR para SHOWDOWN."
            self.atualizar_stats()
            
        elif self.fase == "RIVER":
            self.showdown()
    
    def fold(self):
        if self.fase == "PRE_FLOP":
            self.mensagem = f"Você desistiu. Perdeu ${self.aposta_ante}."
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
            self.mensagem = f"Dealer não qualificou! Você ganhou ${ganho}. Sua mão: {tipo_jogador.value[1]}"
            self.adicionar_historico("VITÓRIA (Dealer não qualificou)", ganho)
        elif tipo_jogador > tipo_dealer or (tipo_jogador == tipo_dealer and valores_jogador > valores_dealer):
            ganho = self.aposta_ante * 2
            self.fichas += total_apostado + ganho
            self.mensagem = f"Você venceu! Ganhou ${ganho}. {tipo_jogador.value[1]} vs {tipo_dealer.value[1]}"
            self.adicionar_historico("VITÓRIA", ganho)
        elif tipo_jogador == tipo_dealer and valores_jogador == valores_dealer:
            self.fichas += total_apostado
            self.mensagem = f"Empate! Apostas devolvidas. {tipo_jogador.value[1]}"
            self.adicionar_historico("EMPATE", 0)
        else:
            self.mensagem = f"Dealer venceu. Perdeu ${total_apostado}. {tipo_dealer.value[1]} vs {tipo_jogador.value[1]}"
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
    
    def get_taxa_vitoria(self):
        return (self.total_vitorias / self.total_jogos * 100) if self.total_jogos > 0 else 0