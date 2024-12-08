import pygame
import logic

pygame.init()

WINDOW = pygame.display.set_mode((logic.WINDOW_WIDTH, logic.WINDOW_HEIGHT))
pygame.display.set_caption("2048")

def main(window):
    clock = pygame.time.Clock()
    run = True        
         
    while run:
        clock.tick(logic.FPS)
        
        if not logic.state.game_active:                              
            logic.draw_start_screen(window)                    
        else:
            if logic.state.new_game:                
                logic.draw_start_screen(window)
                logic.state.new_game = False
            
            logic.draw(window)   
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                logic.click_combo(event)

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN] and logic.state.game_active:
                    direction = None
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                    elif event.key == pygame.K_UP:
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        direction = "down"

                    logic.move_tiles(WINDOW, clock, direction)     
                    
                    if logic.valid_end_game(logic.state.tiles):
                        pygame.time.delay(700)
                        logic.generate_tiles()
                    
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)

