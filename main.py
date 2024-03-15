# This file was created by: Matthew Tran
# added this comment to prove github is listening...
# Imports pygame as pg and imports settings code
'''
moving enemies and player death
coin counter ✔
new maps ✔
'''
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

Level1 = "map.txt"
Level2 = "map2.txt"

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
#Defines the load data method, displays high score for game
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(self.game_folder, Level1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # resets player moneybag
        self.player.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, Level2), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '2':
                    Coin(self, col, row)
                if tile == '3':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Mobs(self, col, row)
                if tile == '4':
                    ChangeMap(self, col, row)

# Defines the method new
    def new(self):
        print("create new game...")
        #Places are the sprites in a group
        self.all_sprites = pg.sprite.Group()
        #Places all the walls in a group
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.change_map = pg.sprite.Group()
        # Sets size of player and gives player access to everything in the game with "self"
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == '2':
                    Coin(self, col, row)
                if tile == '3':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Mobs(self, col, row)
                if tile == '4':
                    ChangeMap(self, col, row)

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
#defines the method draw_grid
    def draw_grid(self):
        #sets the location and color of the horizontal lines
        for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        #sets the location and color of the vertical lines
        for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

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
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
        
        pg.display.flip()

    def events(self):
        #quits the game if pygame quits
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     #if A key pressed, player will move one x position to the left
            #     if event.key == pg.K_a:
            #         self.player1.move(dx=-1)
            #     #if D key pressed, player will move one x position to the right
            #     if event.key == pg.K_d:
            #         self.player1.move(dx=1)
            #     #if S key pressed, player will move one y position down
            #     if event.key == pg.K_s:
            #         self.player1.move(dy=1)
            #     #if W key pressed, player will move one y position up
            #     if event.key == pg.K_w:
            #         self.player1.move(dy=-1)
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
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