# This file was created by: Matthew Tran
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
from pygame.sprite import Sprite
from os import path
vec = pg.math.Vector2

SPRITESHEET = "theBell.png"

dir = path.dirname(__file__)
img_folder = path.join(dir, 'images')

# sets up file with multiple images...
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 4, height * 4))
        return image
    
class Animated_sprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.jumping = False
        self.walking = False
        self.current_frame = 0
        self.last_update = 0

#creates a class called "Player"
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        #Initializes super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #added player image to prite from the game class...
        self.spritesheet = Spritesheet(path.join(img_folder, 'theBell.png'))
        self.load_images()
        #sets color for player
        self.image.fill(TEAL)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #original moneybag amount
        self.moneybag = 0
        #sets original speed
        self.speed = 300
        #sets original hitpoint (health) level
        self.hitpoints = 100

    #function for "get_keys"
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        #sets what happens if the left key is pressed
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        #sets what happens if the right key is pressed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        #sets what happens if the up key is pressed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        #sets what happens if the down key is pressed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            
    #function for colliding with walls
    def collide_with_walls(self, dir):
        #if loop for colliding on the x-axis
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            #prevents player from going through wall on the x-axis
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        #if loop for colliding on the y-axis
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            #prevents player from going through wals on the y-axis
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    #function for colliding with a certain sprite
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            #Adds 1 to moneybag if collide with coin
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            #Increases speed by 50 if collide with powerup
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.speed += 50
            #decreases health if collide with mobs
            if str(hits[0].__class__.__name__) == "Mobs":
                print(hits[0].__class__.__name__)
                print("collided with mob")
                self.hitpoints -= 1
            #changes map if collides with changemap block
            if str(hits[0].__class__.__name__) == "ChangeMap":
                self.game.change_level("map2.txt")
            #quits game if health reaches 0
            if self.hitpoints == 0:
                quit(self)

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        #kills coin block if collided
        self.collide_with_group(self.game.coins, True)
        #kills powerup block if collided
        self.collide_with_group(self.game.power_ups, True)
        #prevents killing mob if collided
        self.collide_with_group(self.game.mobs, False)
        #decreases health if collided with mob
        if self.collide_with_group(self.game.mobs, False):
            self.hitpoints = -1
        #kills change map block if collided
        self.collide_with_group(self.game.change_map, True)
          
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")

#Creates a class called "Wall"
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #Initializes super class
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #Sets the color of the block
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#Creates a class called "Coin"
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #Initializes super class
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #Sets the color of coin
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#Creates a class called "PowerUp"
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #Initializes super class
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #Sets the color of the powerup
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#creates a class called "ChangeMap"
class ChangeMap(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.change_map
        #Initializes super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #sets the color for the change map block
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mobs(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        #Initializes super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 100, 100
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
        #if loop for colliding on the x-axis
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            #prevents player from going through wall on the x-axis
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        #if loop for colliding on the y-axis
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            #prevents player from going through wals on the y-axis
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    def update(self):
        #self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')