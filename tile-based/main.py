# Pygame Template / Skeleton for a new project
import pygame as pg
import random
import os,sys
from settings import *
from sprites import *

class Game():
    '''Main class of the game'''

    def __init__(self):
        '''Initialize game window, etc'''
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        '''Start a new game'''
        pass

    def run(self):
        '''Gaem loop'''
        self.playing = True
        while self.playing:
            # keep loop running at the right speed 
            self.clock.tick(FPS)
            # Process input (events)
            self.events()
            # Update sprites acording events
            self.update()
            # Draw / render
            self.draw()

    def update(self):
        '''Gaem loop - Update'''
        pass

    def events(self):
        '''Gaem loop - Events'''
        for e in pg.event.get():
            # Check if quit
            if e.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen,BLUE, (x,0),(x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen,BLUE, (0,y),(WIDTH,y))
    def draw(self):
        '''Gaem loop - Draw'''
        self.screen.fill(BLACK)
        # *After* drawing everything, flip the display
        self.draw_grid()
        pg.display.flip()

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.new()
        game.run()
    pg.quit()