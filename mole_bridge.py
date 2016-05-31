#!/usr/bin/env python2
import pygame
pygame.init()
pygame.font.init()
import states

# Constants
RUNNING = True
SIZE = (500, 500)

scrn = pygame.display.set_mode(SIZE)
font = pygame.font.SysFont('monospace', 25, True)
curr_state = states.MainState(scrn, font)

pygame.display.set_caption('Mole Bridge Visualized')

while RUNNING:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: RUNNING = False
        curr_state.handle(e)

    # Update
    curr_state.update()

    scrn.fill((0, 0, 0))

    # Draw
    curr_state.draw()

    pygame.display.flip()


pygame.quit()
