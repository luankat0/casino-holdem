# Casino Hold'em - Versão Modularizada

## 📁 Estrutura do Projeto

```
casino_holdem/
├── game_logic.py      # Lógica do jogo
├── game_interface.py  # Interface gráfica
├── main.py            # Arquivo principal de execução
└── README.md          # Este arquivo
└── LICENSE            # Licensa MIT
```

## 🎯 Arquitetura Modular

### **1. game_logic.py** - Camada de Lógica
Contém toda a lógica do jogo sem dependências de interface gráfica:

- **Classes de Dados:**
  - `Naipe`: Enum com símbolos de naipes (♣♦♥♠)
  - `TipoMao`: Enum com ranking de mãos (Carta Alta até Royal Flush)
  - `Carta`: Representa uma carta individual
  - `Baralho`: Gerencia o deck completo com embaralhamento

- **Motor de Avaliação:**
  - `AvaliadorMao`: Avalia e compara mãos de poker
    - `avaliar_mao()`: Determina o melhor tipo de mão possível
    - `_avaliar_5_cartas()`: Avalia uma combinação específica de 5 cartas
    - `_is_sequencia()`: Verifica se há sequência

- **Análise Estatística:**
  - `CalculadorProbabilidades`: Calcula probabilidades em tempo real
    - `calcular_equity()`: Simulação Monte Carlo para % de vitória
    - `calcular_outs()`: Identifica cartas que melhoram a mão

- **Controle do Jogo:**
  - `GameLogic`: Gerencia o estado completo do jogo
    - Controle de fichas e apostas
    - Fases do jogo (INICIO, PRE_FLOP, FLOP, TURN, RIVER, FIM)
    - Histórico de partidas
    - Estatísticas acumuladas

### **2. game_interface.py** - Camada de Interface
Responsável por toda a renderização gráfica usando Pygame:

- **Classe Principal:**
  - `GameInterface`: Gerencia toda a interface visual
    - `desenhar_tela()`: Renderiza a tela completa
    - `desenhar_carta()`: Desenha cartas individuais
    - `desenhar_botoes()`: Renderiza botões interativos
    - `desenhar_painel_stats()`: Painel de análise estatística
    - `desenhar_historico()`: Exibe histórico de partidas
    - `processar_click()`: Trata eventos de mouse

- **Configurações Visuais:**
  - Definições de cores
  - Dimensões de elementos
  - Fontes em diferentes tamanhos

### **3. main.py** - Arquivo de Execução
Ponto de entrada do aplicativo que conecta lógica e interface:

- Instancia `GameLogic` e `GameInterface`
- Loop principal do jogo
- Tratamento de exceções e encerramento limpo

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install pygame
```

### Executar o Jogo
```bash
python main.py
```

## 📊 Estatísticas e Análise

O painel de análise estatística exibe:

- **Equity em tempo real**: % de vitória calculada por Monte Carlo
- **Tipo de mão atual**: Par, Trinca, Flush, etc.
- **Outs disponíveis**: Cartas que melhoram sua mão
- **Categoria de força**: Muito Forte / Forte / Média / Fraca
- **Histórico de jogos**: Últimas 5 partidas
- **Taxa de vitória geral**: Performance acumulada

## 🎲 Regras do Casino Hold'em

1. **Ante**: Aposta inicial obrigatória
2. **Cartas iniciais**: Jogador e dealer recebem 2 cartas
3. **Decisão**: CALL (2x ante) ou FOLD
4. **Flop**: 3 cartas comunitárias
5. **Turn**: 4ª carta comunitária
6. **River**: 5ª carta comunitária
7. **Showdown**: Comparação de mãos

**Qualificação do Dealer**: Par de 4s ou melhor

## 📝 Notas Técnicas

- **Simulações Monte Carlo**: 500 iterações para balancear precisão e performance
- **Taxa de atualização**: 60 FPS
- **Resolução**: 1400x900 pixels
- **Cartas no baralho**: 52 (deck padrão)

## 🆘 Suporte

Se encontrar problemas:
1. Verifique se o Pygame está instalado corretamente
2. Certifique-se de ter Python 3.7+
3. Execute `python main.py` no diretório correto
4. Verifique o console para mensagens de erro detalhadas

---

**Desenvolvido usando Python e Pygame**