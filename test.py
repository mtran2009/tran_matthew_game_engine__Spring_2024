import pygame
pygame.init()

# Set up display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.Font(None, 36)

# Define menu items
menu_items = ["Start Game", "Options", "Quit"]

# Define positions for menu items
menu_item_positions = [(screen_width // 2, 200), 
                       (screen_width // 2, 300), 
                       (screen_width // 2, 400)]

def draw_menu():
    screen.fill(WHITE)
    for i, item in enumerate(menu_items):
        text = font.render(item, True, BLACK)
        text_rect = text.get_rect(center=menu_item_positions[i])
        screen.blit(text, text_rect)
    pygame.display.flip()

def main_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is on any menu item
                for i, pos in enumerate(menu_item_positions):
                    if pygame.Rect(pos[0]-100, pos[1]-30, 200, 60).collidepoint(event.pos):
                        if i == 0:
                            # Start Game
                            print("Starting game...")
                        elif i == 1:
                            # Options
                            print("Options menu...")
                        elif i == 2:
                            # Quit
                            running = False
        draw_menu()

    pygame.quit()

main_menu()
