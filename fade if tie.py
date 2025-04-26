import pygame
import sys

# Initialize
pygame.init()

# Setting up ma windowww 
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()



# Load two DIFFERENT images!!!!! omggg AHH
image1 = pygame.image.load('EndScreenBlank.png').convert()
image2 = pygame.image.load('EndScreenBothWin.png').convert()



# Optional: resize if needed
image1 = pygame.transform.scale(image1, (800, 600))
image2 = pygame.transform.scale(image2, (800, 600))

# Starting alpha (transparent)
alpha = 0
image2.set_alpha(alpha)

running = True
while running:
    screen.blit(image1, (0, 0))  # Draw the first image

    if alpha < 255:
        alpha += 2  # Increase transparency
        image2.set_alpha(alpha)

    screen.blit(image2, (0, 0))  # Draw the second image on top

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)  # 60 frames per second

pygame.quit()
sys.exit()