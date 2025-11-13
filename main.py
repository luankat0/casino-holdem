import pygame
import sys
from game_logic import GameLogic
from game_interface import GameInterface

def main():
    # Inicializar a lógica do jogo
    game_logic = GameLogic()
    
    # Inicializar a interface
    game_interface = GameInterface(game_logic)
    
    running = True
    
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game_interface.processar_click(event.pos)
            
            game_interface.desenhar_tela()
            game_interface.get_clock().tick(game_interface.get_fps())
    
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()