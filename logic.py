import pygame
import random
import math

pygame.init()

FPS = 60

# window size 
WIDTH, HEIGHT, HEIGHT_HEADER = 600, 600, 50

BORDER = 20
MARGIN = 10

WINDOW_WIDTH, WINDOW_HEIGHT = WIDTH + BORDER, HEIGHT + HEIGHT_HEADER

ROWS = 4
COLS = 4

RECT_HEIGHT = (HEIGHT // COLS) 
RECT_WIDTH = (WIDTH  // ROWS) 

# grid 
OUTLINE_THICKNESS = 10
MOVE_VEL = 30

# background
BACKGROUND_COLOR = (250,248,240) #default
BACKGROUND_COLOR_RECT = (156,139,124)
BACKGROUND_COLOR_START = BACKGROUND_COLOR 
BACKGROUND_COLOR_GRID = (189,172,151)

# colors
OUTLINE_COLOR = (156,139,124)
FONT_COLOR = (156,139,124) #default
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BUTTON = (234,231,217)
BUTTON_PRESS = (189,172,151)

# fonts
FONT = pygame.font.SysFont("comicsans", 50, bold=True)
FONT_TITLE = pygame.font.SysFont("comicsans", 40, bold=True)
FONT_LABEL = pygame.font.SysFont("comicsans", 20, bold=True)
FONT_COMBOBOX = pygame.font.SysFont("comicsans", 15)

# combo
COMBOBOX_RECT = pygame.Rect(WIDTH -160, 25, 150, 30)
COMBOBOX_OPTIONS = ["Fácil 6x6", "Médio 5x5", "Normal 4x4", "Díficil 3x3"]
SELECTION_OPTION = COMBOBOX_OPTIONS[2]
COMBOBOX_OPEN = False

class GameState:
    def __init__(self):
        self.tiles = {}
        self.game_active = False
        self.game_won = False
        self.game_over = False
        self.new_game = False
        self.score = 0

    def reset(self):
        self.tiles = generate_tiles()
        self.score = 0

state = GameState()

class Tile:
    COLORS = {
        2: ((238, 228, 218), (119, 110, 101)),
        4: ((235,216,182), (117,100,82)),
        8: ((242, 177, 118), (255, 255, 255)),
        16: ((247,149,99), (255, 255, 255)), 
        32: ((247,129,101), (255, 255, 255)),
        64: ((247,102,68), (249, 246, 242)),
        128: ((237, 207, 114), (249, 246, 242)),
        256: ((237, 204, 97), (249, 246, 242)),
        512: ((237, 200, 80), (249, 246, 242)),
        1024: ((237, 197, 63), (249, 246, 242)),
        2048: ((237, 194, 46), (249, 246, 242)),
        "default": ((60, 58, 50), (249, 246, 242)),  # Para valores acima de 2048        
    }
    
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x, self.y = calc_pos(row, col)

    def get_color(self):
        return self.COLORS.get(self.value, self.COLORS["default"])

    def draw(self, window):
        bg_color, txt_color = self.get_color()
        pygame.draw.rect(window, bg_color, (self.x + MARGIN, self.y + HEIGHT_HEADER, RECT_WIDTH, RECT_HEIGHT), 0, 15)
            
        text = FONT.render(str(self.value), 1, txt_color)
        window.blit(
            text,
            (
                self.x + MARGIN + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + HEIGHT_HEADER +(RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]        

def calc_pos(row, col):    
    x = col * RECT_WIDTH  
    y = row * RECT_HEIGHT
    return x, y

def printTile(tiles):
    for tile in tiles.values():
        print("x", tile.x, "y", tile.y, "r", tile.row, "c", tile.col)

# move tile
def move_tiles(window, clock, direction):    
        
    if direction == "left":
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: state.tiles.get(f"{tile.row}{tile.col - 1}")        
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True
    elif direction == "right":
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: state.tiles.get(f"{tile.row}{tile.col + 1}")
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: state.tiles.get(f"{tile.row - 1}{tile.col}")
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: state.tiles.get(f"{tile.row + 1}{tile.col}")
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False
    
    updated = True
    merged_tiles = set()
    changed = False
    
    while updated:
        clock.tick(FPS)
        updated = False
        
        sorted_tiles = sorted(state.tiles.values(), key=lambda t: (t.row, t.col), reverse=(direction in ["right", "down"]))
        
        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta) 
                changed = True                         
            elif (
                tile.value == next_tile.value
                and tile not in merged_tiles
                and next_tile not in merged_tiles
            ):                
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    merged_tiles.add(next_tile)
                    tile.value = 0 
                    changed = True
                    state.score += next_tile.value                    

            elif move_check(tile, next_tile):
                tile.move(delta)
                changed = True
            else:                
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, sorted_tiles)    
    end_move(changed)
      
    if changed:        
        draw(window)        
    
    return changed

# update new tiles
def update_tiles(window, sorted_tiles):
    state.tiles.clear()
    for tile in sorted_tiles:
        state.tiles[f"{tile.row}{tile.col}"] = tile

    draw(window)

# end move
def end_move(changed):
    if changed:
        row, col = get_random_pos(state.tiles)
        state.tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

# valid end game
def valid_end_game(tiles):        
    if any(tile.value == 2048 for tile in tiles.values()):  # Vitória
        end_game(victory=True)
        return True

    if len(tiles) == ROWS * COLS:  # Sem posições vazias
        for tile in tiles.values():
            for get_next_tile in [
                lambda t: tiles.get(f"{t.row}{t.col + 1}"),
                lambda t: tiles.get(f"{t.row}{t.col - 1}"),
                lambda t: tiles.get(f"{t.row + 1}{t.col}"),
                lambda t: tiles.get(f"{t.row - 1}{t.col}"),
            ]:
                if get_next_tile(tile) and get_next_tile(tile).value == tile.value:
                    return False  # Movimento válido ainda existe
        end_game(victory=False)  # Nenhum movimento válido
        return True

    return False

#click combo levels
def click_combo(event):
    global COMBOBOX_OPEN, COMBOBOX_RECT, SELECTION_OPTION, ROWS, COLS, RECT_WIDTH, RECT_HEIGHT, MOVE_VEL
    
    def getFont(index):
        global FONT
        fonts = {3: 55, 4: 50, 5: 40, 6: 35}
        nfont = fonts.get(index)
        FONT = pygame.font.SysFont("comicsans", nfont, bold=True)   
        
    if COMBOBOX_RECT.collidepoint(event.pos):
        COMBOBOX_OPEN = not COMBOBOX_OPEN  # Abrir/fechar menu suspenso
    elif COMBOBOX_OPEN:
                # Verificar clique em uma opção
        for i, option in enumerate(COMBOBOX_OPTIONS):
            option_rect = pygame.Rect(COMBOBOX_RECT.x, COMBOBOX_RECT.y + COMBOBOX_RECT.height * (i + 1), COMBOBOX_RECT.width, COMBOBOX_RECT.height)
            if option_rect.collidepoint(event.pos):
                SELECTION_OPTION = option                        
                COMBOBOX_OPEN = False  # Fechar menu suspenso
                            
                for i in range(3, 7):
                    if str(i) in SELECTION_OPTION:
                        ROWS = i
                        COLS = i 
                        getFont(i)               
                        break
                
                if ROWS == 3 or ROWS == 6:
                    MOVE_VEL = 20
                else:
                    MOVE_VEL = 30    

                RECT_HEIGHT = (HEIGHT // COLS)                 
                RECT_WIDTH = (WIDTH  // ROWS) 
            else:
                COMBOBOX_OPEN = False  # Fechar menu suspenso se clicar fora
    
#draw combo
def draw_comboBox(window, options, selected_option, open_status):
    # comboBox    
    pygame.draw.rect(window, BUTTON_PRESS, COMBOBOX_RECT, border_radius=5)
    text = FONT_COMBOBOX.render(selected_option, True, BLACK)
    window.blit(text, (COMBOBOX_RECT.x + 10, COMBOBOX_RECT.y + 5))
    
    # open/close
    #arrow = "▼" if not open_status else "▲"
    arrow = "+" if not open_status else "-"
    arrow_text = FONT_COMBOBOX.render(arrow, True, BLACK)
    window.blit(arrow_text, (COMBOBOX_RECT.right - 30, COMBOBOX_RECT.y + 5))
    
    if open_status:
        # draw options
        for i, option in enumerate(options):
            option_rect = pygame.Rect(COMBOBOX_RECT.x, COMBOBOX_RECT.y + COMBOBOX_RECT.height * (i + 1), COMBOBOX_RECT.width, COMBOBOX_RECT.height)
            pygame.draw.rect(window, (238,228,218), option_rect, border_radius=5)
            option_text = FONT_COMBOBOX.render(option, True, BLACK)
            window.blit(option_text, (option_rect.x + 10, option_rect.y + 5))

#draw header
def draw_header(window):     
    text = FONT_LABEL.render("Score: " + str(state.score), True, FONT_COLOR)    
    window.blit( text, (WIDTH - text.get_width() - 70, 10))
    
    text = FONT_LABEL.render("New game", True, BUTTON)     
    x = MARGIN 
    y = 10
    w = text.get_width() + 20
    h = text.get_height() + 5

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # check if the mouse is over the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, BUTTON_PRESS, (x, y, w, h), 0, 15)
        if click[0] == 1: 
            newgame()
    else:
        pygame.draw.rect(window, FONT_COLOR, (x, y, w, h), 0, 15)
    
    window.blit( text, (MARGIN + 10, 10))
    
    pygame.display.update()

# draw grid tile
def draw_grid(window):    
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT + HEIGHT_HEADER
        pygame.draw.line(window, OUTLINE_COLOR, (MARGIN, y), (WIDTH, y), OUTLINE_THICKNESS)        

    for col in range(1, COLS):
        x = col * RECT_WIDTH + MARGIN
        pygame.draw.line(window, OUTLINE_COLOR, (x, HEIGHT_HEADER), (x, HEIGHT + HEIGHT_HEADER), OUTLINE_THICKNESS)
    
    pygame.draw.rect(window, OUTLINE_COLOR, (MARGIN, HEIGHT_HEADER, WIDTH, HEIGHT), OUTLINE_THICKNESS, 15)        

# draw tiles  
def draw(window):        
    window.fill(BACKGROUND_COLOR)
    
    pygame.draw.rect(window, BACKGROUND_COLOR_GRID, (MARGIN, HEIGHT_HEADER, WIDTH, HEIGHT), 0, 15)        
    
    for tile in state.tiles.values():
        tile.draw(window)

    draw_grid(window)
    draw_header(window)
    pygame.display.update()

# draw text tile
def draw_text(text, color, window, x, y, center = True):
    text = FONT_TITLE.render(text, True, color)
    window.blit(
        text,
        (                
            x - text.get_width() / 2 if center else x,
            y - text.get_height() / 2 if center else y,
        ),
    )

# draw button
def draw_button(window, text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # check if the mouse is over the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, active_color, (x, y, w, h), 0, 15)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, inactive_color, (x, y, w, h), 0, 15)

    # draw text button
    draw_text(text, BUTTON , window, x + w // 2, y + h // 2)

# draw star game screen
def draw_start_screen(window):    
    global COMBOBOX_RECT, COMBOBOX_OPTIONS, SELECTION_OPTION, COMBOBOX_OPEN

    window.fill(BACKGROUND_COLOR_START)
    draw_text("2048", FONT_COLOR, window, 20, 10, False)
    draw_comboBox(window, COMBOBOX_OPTIONS, SELECTION_OPTION, COMBOBOX_OPEN)
    
    if state.game_over or state.game_won:
        if state.game_won:
            draw_text("YOU WON!", GREEN, window, WIDTH // 2, HEIGHT // 3 + 50)
        else:
            draw_text("GAME OVER!", RED, window, WIDTH // 2, HEIGHT // 3 + 50)
    
    draw_button(window, "START", WIDTH // 2 - 75, HEIGHT // 2, 150, 50, FONT_COLOR, BUTTON_PRESS, start_game)    
        
    pygame.display.update()
    
# genarate random position
def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col

# generate two random tiles to start game
def generate_tiles():
    tiles = {}    
    
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

# ajusta vars new game
def newgame():    
    state.game_active = False
    state.game_over = False
    state.game_won = False    
    state.new_game = True
    
# start vars game
def start_game():      
    state.game_active = True
    state.game_over = False
    state.game_won = False    
    state.reset()


# end vars game
def end_game(victory):       
    state.game_active = False
    state.game_over = True
    state.game_won = victory        
   