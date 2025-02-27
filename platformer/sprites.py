# Sprite classes for platform
import pygame as pg
from settings import *
from random import choice,randrange
vec = pg.math.Vector2
class SpriteSheet:
    # utility class for loading and parsing sprites
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0), (x,y,width,height))
        image = pg.transform.scale(image,(width//2,height//2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.pos = vec(40,HEIGHT - 100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def  load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614,1063,120,191),
                                self.game.spritesheet.get_image(690,405,120,201)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r =[self.game.spritesheet.get_image(678,860,120,201),
                        self.game.spritesheet.get_image(692,1458,120,207)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        self.walk_frames_l =[]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame,True,False))
        self.jump_frame = self.game.spritesheet.get_image(382,763,150,181)
        self.jump_frame.set_colorkey(BLACK)
    
    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap the sides of the screen
        if self.pos.x > WIDTH + self.rect.width//2:
            self.pos.x = 0 - self.rect.width//2
        if self.pos.x < 0 - self.rect.width//2:
            self.pos.x = WIDTH  + self.rect.width//2
            
        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if not self.vel.x == 0:
            self.walking = True
        else:
            self.walking = False
        if self. jumping:
            self.image = self.jump_frame
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
        if self.walking and not self.jumping and now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
            last_bottom = self.rect.bottom
            if self.vel.x > 0:
                self.image = self.walk_frames_r[self.current_frame]
            else:
                self.image = self.walk_frames_l[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = last_bottom

        if not self.jumping and not self.walking and now - self.last_update > 200:
            last_bottom = self.rect.bottom
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            self.image = self.standing_frames[self.current_frame]
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = last_bottom
        
        self.mask = pg.mask.from_surface(self.image)
    
    def jump_cut(self):
        if self.jumping and self.vel.y < -4:
            self.vel.y = -4

    def jump(self):
        #jump only if standing on a platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2 
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping= True
            self.vel.y = -PLAYER_JUMP

class Cloud(pg.sprite.Sprite):
    def  __init__(self,game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = choice(self.game.cloud_imgs)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50,100)/100
        self.image = pg.transform.scale(self.image,(int(self.rect.width*scale),int(self.rect.height*scale)))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500,-50)
    def update(self):
        if self.rect.top > HEIGHT:
            self.kill()

class Platform(pg.sprite.Sprite):
    def  __init__(self,game,x,y):
        self._layer = PLAT_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.images = [self.game.spritesheet.get_image(0,288,380,94),
                                self.game.spritesheet.get_image(233,1662,201,100)]
        self.image =  choice(self.images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game,self)

class Pow(pg.sprite.Sprite):
    def  __init__(self,game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.game.spritesheet.get_image(820,1805,71,70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def  __init__(self,game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(566,510,122,139)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(568,1534,122,135)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1,4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT//2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy <0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        self.mask = pg.mask.from_surface(self.image)
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
        