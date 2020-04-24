import pygame
import random
import os


img_dir = os.path.join(os.path.dirname(__file__),"img")
snd_dir = os.path.join(os.path.dirname(__file__),"snd")

WIDTH = 480
HEIGHT = 600
FPS = 60

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
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,WHITE,outline_rect,2)
    pygame.draw.rect(surf,GREEN,fill_rect)

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
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx =  5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

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

#load all game graphics
bacground = pygame.image.load(os.path.join(img_dir,"bg.png")).convert()
bacground_rect = bacground.get_rect()
ship_img = pygame.image.load(os.path.join(img_dir,"ship.png")).convert()
meteor_img = pygame.image.load(os.path.join(img_dir,"meteor.png")).convert()
lazer_img = pygame.image.load(os.path.join(img_dir,"lazer.png")).convert()
meteor_images = []
meteor_list = ['meteor.png','meteorsmall1.png','meteorsmall2.png', 'meteorbig1.png', 'meteorbig2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir,img)).convert())

#load sounds
shoot_sound =pygame.mixer.Sound(os.path.join(snd_dir,"pew.wav"))
expl_sounds = []
for snd in ['Explosion.wav','Explosion3.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(snd_dir,snd)))
pygame.mixer.music.load(os.path.join(snd_dir,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ship = Ship()
all_sprites.add(ship)
for i in range(8):
    spawn_mob()
score = 0


# game loop
running = True
# keep loop running at the right speed
pygame.mixer.music.play(loops=-1)
while running:
    clock.tick(FPS)
    # Process input (events)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                ship.shoot()
    # Update
    all_sprites.update()
    # check  to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True,pygame.sprite.collide_circle)
    for hit in hits:
        score += 70 - hit.radius
        random.choice(expl_sounds).play()
        spawn_mob()

    # check  to see if a mob hit the player
    hits = pygame.sprite.spritecollide(ship, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        ship.shield -= hit.radius
        spawn_mob()
        if ship.shield < 0:
            running = False        
    # Draw / render
    screen.fill(BLACK)
    screen.blit(bacground, bacground_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2, 10)
    draw_shield_bar(screen,5,5,ship.shield)
    # *After* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()