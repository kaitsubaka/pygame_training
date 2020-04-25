import pygame
import random
import os


img_dir = os.path.join(os.path.dirname(__file__),"img")
snd_dir = os.path.join(os.path.dirname(__file__),"snd")

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup practice!!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (int(x),int(y))
    surf.blit(text_surface,text_rect)

def spawn_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,int(fill),BAR_HEIGHT)
    pygame.draw.rect(surf,WHITE,outline_rect,2)
    pygame.draw.rect(surf,GREEN,fill_rect)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)

def show_go_screen():
    screen.blit(bacground, bacground_rect)
    draw_text(screen,'STHUP!!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen,"Arrow key move, Space to fire", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, 'Press a key to begin', 18, WIDTH/2, HEIGHT*3 /4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYUP:
                waiting = False

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ship_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 15
        # pygame.draw.circle(self.image, RED,self.rect.center,self.radius)
        self.rect.centerx = int(WIDTH /2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
    
    def update(self):
        #time out for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000 :
            self.hidden = False
            self.rect.centerx = int(WIDTH/2)
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx =  5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (int(WIDTH / 2), HEIGHT + 200)  

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        # pygame.draw.circle(self.image, RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.ro_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left > WIDTH+20 or self.rect.right < -25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150,-100)
            self.speedy = random.randrange(1,8)
    
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.ro_speed) % 360
            new_image = pygame.transform.rotate(self.image_original,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Bullet(pygame.sprite.Sprite):
    def  __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = lazer_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 10:
            self.kill()
class Pow(pygame.sprite.Sprite):
    def  __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
    
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()
class Explosion(pygame.sprite.Sprite):
    def  __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.frame = 0
        self.image = explosion_anim[self.size][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def  update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#load all game graphics
bacground = pygame.image.load(os.path.join(img_dir,"bg.png")).convert()
bacground_rect = bacground.get_rect()
ship_img = pygame.image.load(os.path.join(img_dir,"ship.png")).convert()
ship_mini_image = pygame.transform.scale(ship_img,(25,19))
ship_mini_image.set_colorkey(BLACK)
meteor_img = pygame.image.load(os.path.join(img_dir,"meteor.png")).convert()
lazer_img = pygame.image.load(os.path.join(img_dir,"lazer.png")).convert()
meteor_images = []
meteor_list = ['meteor.png','meteorsmall1.png','meteorsmall2.png', 'meteorbig1.png', 'meteorbig2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir,img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['ship'] = []
for i in range(9):
    file_name = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir,file_name)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    file_name = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_dir,file_name)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['ship'].append(img)

powerup_imgs = {}
powerup_imgs['shield'] = pygame.image.load(os.path.join(img_dir,'shield_gold.png')).convert()
powerup_imgs['gun'] = pygame.image.load(os.path.join(img_dir,'bolt_gold.png')).convert()
#load sounds
shoot_sound =pygame.mixer.Sound(os.path.join(snd_dir,"pew.wav"))
shield_sound =pygame.mixer.Sound(os.path.join(snd_dir,"pow4.wav"))
boost_sound =pygame.mixer.Sound(os.path.join(snd_dir,"pow5.wav"))
expl_sounds = []
for snd in ['Explosion.wav','Explosion3.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir,snd)))
ship_explo_snd = pygame.mixer.Sound(os.path.join(snd_dir,'rumble1.ogg'))
pygame.mixer.music.load(os.path.join(snd_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)

# game loop
game_over = True
running = True
# keep loop running at the right speed
pygame.mixer.music.play(loops=-1)
while running:
    clock.tick(FPS)
    if game_over:
        game_over= False
        show_go_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        ship = Ship()
        all_sprites.add(ship)
        for i in range(8):
            spawn_mob()
        score = 0
    # Process input (events)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()
    # check  to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True,pygame.sprite.collide_circle)
    for hit in hits:
        score += 70 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        spawn_mob()
        


    # check  to see if a mob hit the player
    hits = pygame.sprite.spritecollide(ship, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        ship.shield -= hit.radius
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        spawn_mob()
        if ship.shield <= 0:
            ship_explo_snd.play()
            death_explosion = Explosion(ship.rect.center,'ship')
            all_sprites.add(death_explosion)
            ship.hide()
            ship.lives -= 1
            ship.shield = 100
    #check if a powerup hits player
    hits = pygame.sprite.spritecollide(ship,powerups,True)
    for hit in hits:
        if hit.type == 'shield':
            ship.shield += random.randrange(10,30)
            shield_sound.play()
            if ship.shield > 100:
                ship.shield = 100
        if hit.type == 'gun':
            boost_sound.play()
            ship.powerup()
    #if player died and the explosion has finished
    if ship.lives == 0 and not death_explosion.alive():
        game_over = True       
    # Draw / render
    screen.fill(BLACK)
    screen.blit(bacground, bacground_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2, 10)
    draw_shield_bar(screen,5,5,ship.shield)
    draw_lives(screen,WIDTH - 100, 5,ship.lives,ship_mini_image)
    # *After* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()