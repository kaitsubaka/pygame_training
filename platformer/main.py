# Jumpy! - platform game

import pygame as pg
import random
from settings import *
from sprites import *
import os



class Game():

    def __init__(self):
        # initialize game window, etc

        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    
    def load_data(self):
        #load high score
        self.dir = os.path.dirname(__file__)
        img_dir = os.path.join(self.dir,'img')
        self.snd_dir = os.path.join(self.dir,'snd')
        with open(os.path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load spritesheet img
        self.spritesheet = SpriteSheet(os.path.join(img_dir,SPRITE_SHEET))
        self.jump_sound = pg.mixer.Sound(os.path.join(self.snd_dir,'Jump33.wav'))

    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(self,*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(os.path.join(self.snd_dir, 'Yippee.ogg'))
        self.run()

    def run(self):
        # Game loop
        pg.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing: 
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)
        
    
    def update(self):
        # Game loop - Update
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if lowest.rect.bottom < hit.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
                    self.player.jumping = False
        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT/3:
            self.player.pos.y += int(max(abs(self.player.vel.y),3))
            for plat in self.platforms:
                plat.rect.y += int(max(abs(self.player.vel.y),3))
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        # Die!
        if self.player.rect.bottom >HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= int(max(self.player.vel.y,10))
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False
        # Spawn new platform to keep some average number
        while len(self.platforms)<6:
            width = random.randrange(50,100)
            p = Platform(self,random.randrange(0,WIDTH-width), random.randrange(-75, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)
        


    
    def events(self):
        # Game loop - Events
        for e in pg.event.get():
            if e.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                self.player.jump()
            if e.type == pg.KEYUP and e.key == pg.K_SPACE:
                self.player.jump_cut()


    def draw(self):
        # Game loop - Draw
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image,self.player.rect)
        self.draw_text(str(self.score),22,WHITE,int(WIDTH/2),15)
        # *After* drawing everything, flip the display
        pg.display.update()


    def show_start_screen(self):
        # Game start screen
        pg.mixer.music.load(os.path.join(self.snd_dir, 'Happy Tune.ogg'))
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE,WIDTH/2, HEIGHT*3 / 4)
        self.draw_text("Highscore: " + str(self.highscore), 22, WHITE,WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    
    def  show_go_screen(self):
        # Game over/ continue
        pg.mixer.music.load(os.path.join(self.snd_dir, 'Happy Tune.ogg'))
        pg.mixer.music.play(loops = -1)
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Score: " + str(self.score), 22, WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE,WIDTH/2, HEIGHT*3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!!",22,WHITE,WIDTH/2,HEIGHT/2 + 40)
            with open(os.path.join(self.dir,HS_FILE),'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("Highscore: " + str(self.highscore), 22, WHITE,WIDTH/2, HEIGHT/2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if e.type == pg.KEYUP:
                    waiting =False
    
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop= (int(x),int(y))
        self.screen.blit(text_surface,text_rect)


if __name__ == '__main__':
    game = Game()
    game.show_start_screen()
    while game.running:
        game.new()
        game.show_go_screen()

    pg.quit()