import pygame
background_colour = (255,255,255)
(width, height) = (1000, 1000)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Archery')
screen.fill(background_colour)
pygame.display.flip()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
def terminate():
    pygame.quit()


terminate()

