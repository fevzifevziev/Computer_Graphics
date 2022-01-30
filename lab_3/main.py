import math
import random
import pygame
import sys
import graphicsLibrary

pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
display_width, display_height = pygame.display.Info().current_w, pygame.display.Info().current_h

x = 0
y = 0
i = -1

screen.fill("white")

for i in range(100):
    graphicsLibrary.drawSpline(screen, "green", [670+i*10,719, 680+i*10,712, 692+i*10,701, 694+i*10,690])

#graphicsLibrary.polygon(screen, "black", [(456, 364),(557, 397), (454, 322), (474, 306), (222, 123)])

graphicsLibrary.circle(screen, display_width-55, 0+50, 50, color="yellow", T_F=0)
for fi in range(0, 60, 1):
    x = 60*math.cos(fi)+display_width-55
    y = 60*math.sin(fi)+50
    graphicsLibrary.draw_line(screen, "yellow", x1=display_width-55, y1=50, x2=x, y2=y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    pygame.display.flip()
    clock.tick(60)
