# Jumpy! - platform game

import pygame as pg
import random
from settings import *

class Game():

    def __init__(self):
        # initialize game window, etc

        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
            
    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing: 
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    
    def update(self):
        # Game loop - Update
        self.all_sprites.update()
    
    def events(self):
        # Game loop - Events
        for e in pg.event.get():
            if e.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *After* drawing everything, flip the display
        pg.display.flip()


    def show_start_screen(self):
        # Game start screen
        pass
    
    def  show_go_screen(self):
        # Game over/ continue
        pass
    
game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()