





import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

def main():
   while True:

      print(pygame.mouse.get_pos()) 
      for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               return
            elif event.type == MOUSEWHEEL:
               print(event)
               print(event.x, event.y)
               print(event.flipped)
               #print(event.which)
               # can access properties with
               # proper notation(ex: event.y)
      clock.tick(60)

# Execute game:
main()



