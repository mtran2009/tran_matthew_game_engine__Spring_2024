# This file was created by: Matthew Tran
# added this comment to prove github is listening...
# Imports pygame as pg and imports settings code

'''
Beta:
    Death Screen ✔
    Different types of powerups/downs ✔
    Powerup/down timer ✔

Release version:
    Menu ✔
    More/Better Maps
    (maybe make random maps) 🤷
'''
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

#Map levels
Level1 = "map1.txt"
Level2 = "map2.txt"

#Function to draw a health bar
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    #Sets the size/dimensions of the health bar
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    #colors in the heathbar
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# Creates an object constructor called "Game"
class Game:
    # Allows us to assign properties to the class
    def __init__(self):
        # Initiates pygame
        pg.init()
        # Sets up the screen and its dimentions
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Allows us to edit the frames per second of the game (game clock)
        self.clock = pg.time.Clock()
        self.load_data()
#Defines the load data method
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        # self.img_folder = path.join(self.game_folder, 'images')
        # self.player_img = pg.image.load(path.join(self.img_folder, 'theBell.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        #opens level 1 map when game is run
        with open(path.join(self.game_folder, Level1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

#function to change the level when a certain block is hit
    def change_level(self, lvl):

        # Initialize groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.power_downs = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.change_map = pg.sprite.Group()
        self.coins = pg.sprite.Group()

        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        
        #draws blocks in the map for the levels
        for row, tiles in enumerate(self.map_data):
            print(row)
            #draws a ceratin block on the game according to assigned #s on a map
            for col, tile in enumerate(tiles):
                print(col)
                #Creates a wall for every "1" in the map
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                #Creates a player for ever "P" in the map
                if tile == 'P':
                    self.player = Player(self, col, row)
                #creates a coin for every "2" in the map
                if tile == '2':
                    Coin(self, col, row)
                #creates a powerup for every "3" in the map
                if tile == '3':
                    PowerUp(self, col, row)
                #creates a mob for every "M" in the map
                if tile == 'M':
                    Mobs(self, col, row)
                #creates a change map block for every "4" in the map
                if tile == '4':
                    ChangeMap(self, col, row)
                #creates a change map block for every "5" in the map
                if tile == '5':
                    PowerDown(self, col, row)
        # resets player moneybag
        self.player.moneybag = 0

# Defines the method new
    def new(self):
        print("create new game...")
        #Places are the sprites in a group
        self.all_sprites = pg.sprite.Group()
        #Places all the walls in a group
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.power_downs = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.change_map = pg.sprite.Group()
        # Sets size of player and gives player access to everything in the game with "self"
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)

        #draws blocks in the map for the levels
        for row, tiles in enumerate(self.map_data):
            print(row)
            #draws a ceratin block on the game according to assigned #s on a map
            for col, tile in enumerate(tiles):
                print(col)
                #Creates a wall for every "1" in the map
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                #Creates a player for ever "P" in the map
                if tile == 'P':
                    self.player = Player(self, col, row)
                #creates a coin for every "2" in the map
                if tile == '2':
                    Coin(self, col, row)
                #creates a powerup for every "3" in the map
                if tile == '3':
                    PowerUp(self, col, row)
                #creates a mob for every "M" in the map
                if tile == 'M':
                    Mobs(self, col, row)
                #creates a change map block for every "4" in the map
                if tile == '4':
                    ChangeMap(self, col, row)
                #creates a change map block for every "5" in the map
                if tile == '5':
                    PowerDown(self, col, row)

# Defines the method run
    def run(self):
        # While loop to run code while the the game is being played
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
# Defines the method quit
    def quit(self):
         pg.quit()
         sys.exit()
#Defines the method update
    def update(self):
        self.all_sprites.update()
        if self.player.hitpoints < 1:
            self.playing = False
        #shows death screen if health reaches 0
        if self.player.hitpoints == 0:
            self.show_death_screen()
#defines the method draw_grid
    def draw_grid(self):
        #sets the location and color of the horizontal lines
        for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        #sets the location and color of the vertical lines
        for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    #function that draws the text, setting the font and coordinates
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('comic sans')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

#Defines the draw method that draws everything in the game    
    def draw(self):
        #sets the background color of the screen
        self.screen.fill(BGCOLOR)
        #draws the grid
        self.draw_grid()
        #draws the sprites
        self.all_sprites.draw(self.screen)
        #draws and sets the color for the coin counter text
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        #draws the health bar
        draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.hitpoints)
        
        pg.display.flip()

    def events(self):
        #quits the game if pygame quits
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        # Sets bg color for start screen
        self.screen.fill(BGCOLOR)
        # Draws text on start screen
        self.draw_text(self.screen, "Choose a level", 24, WHITE, 13.5, 6)
        self.draw_text(self.screen, "Level 1", 24, WHITE, 14.9, 10)        
        self.draw_text(self.screen, "Level 2", 24, WHITE, 14.9, 12)        
        self.draw_text(self.screen, "Quit Game", 24, WHITE, 14.3, 14)
        pg.display.flip()

        # Event loop for level selection
        selecting_level = True
        while selecting_level:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    selecting_level = False
                    self.quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse_x, mouse_y = event.pos
                    # Check if Level 1 is clicked
                    if 14.7 * TILESIZE <= mouse_x <= 16.7 * TILESIZE and 10 * TILESIZE <= mouse_y <= 11 * TILESIZE:
                        self.change_level(Level1)
                        selecting_level = False
                    # Check if Level 2 is clicked
                    elif 14.7 * TILESIZE <= mouse_x <= 16.7 * TILESIZE and 12 * TILESIZE <= mouse_y <= 13 * TILESIZE:
                        self.change_level(Level2)
                        selecting_level = False
                    # Add more levels as needed
                    # Check if Quit Game is clicked
                    elif 14.7 * TILESIZE <= mouse_x <= 16.7 * TILESIZE and 14 * TILESIZE <= mouse_y <= 15 * TILESIZE:
                        selecting_level = False
                        self.quit()
    
    #function to show start screen when game is run
    def show_death_screen(self):
        #sets bg color for death screen
        self.screen.fill(BLACK)
        #draws text on death screen
        self.draw_text(self.screen, "You died! Choose a level to retry.", 24, WHITE, 10.6, 6)
        self.draw_text(self.screen, "Level 1", 24, WHITE, 14.9, 10)        
        self.draw_text(self.screen, "Level 2", 24, WHITE, 14.9, 12)        
        self.draw_text(self.screen, "Quit Game", 24, WHITE, 14.3, 14)
        pg.display.flip()

        # Event loop for level selection
        selecting_level = True
        while selecting_level:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    selecting_level = False
                    self.quit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse_x, mouse_y = event.pos
                    # Check if Level 1 is clicked
                    if 14.7 * TILESIZE <= mouse_x <= 16.7 * TILESIZE and 10 * TILESIZE <= mouse_y <= 11 * TILESIZE:
                        self.change_level(Level1)
                        selecting_level = False
                    # Check if Level 2 is clicked
                    elif 14.7 * TILESIZE <= mouse_x <= 16.7 * TILESIZE and 12 * TILESIZE <= mouse_y <= 13 * TILESIZE:
                        self.change_level(Level2)
                        selecting_level = False
                    # Add more levels as needed
                    # Check if Quit Game is clicked
                    elif 14.7 * TILESIZE <= mouse_x <= 16.7 * TILESIZE and 14 * TILESIZE <= mouse_y <= 15 * TILESIZE:
                        selecting_level = False
                        self.quit()

    #function to wait for key press
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                #if pygame quits, the game stops waiting for key press and quits
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                #if a key is pressed, the game stops waiting
                if event.type == pg.KEYUP:
                    waiting = False

#Instantiates the game
g = Game()
#Uses the game method run to run the program
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()  