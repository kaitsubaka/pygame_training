import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS =30
# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# game loop
running = True
# keep loop running at the right speed
while running:
    clock.tick(FPS)
    # Process input (events)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    # Update
    
    # Draw / render
    screen.fill(BLACK)
    # *After* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()