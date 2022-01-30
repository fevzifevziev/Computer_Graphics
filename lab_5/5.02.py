import pygame, sys, random
import numpy as np

class Main:
    def __init__(self, fps=60, screen_resolution=()):
        self.fps = fps
        pygame.init()
        self.screen = pygame.display.set_mode((1080,720))
        self.clock = pygame.time.Clock()
        self.display_width, self.display_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.bool_pos = 0
        self.x = 5
        self.conter = 0
        #0 - Левое Крыло; 2 - Правое крыло; 1 - Основа; 3 - Заднее Левое Крыло; 4 - Заднее Правое Крыло
        self.list_0_coordinates = [[215, 100], [255, 100],
                                    [365, 307], [265, 310]]
        self.list_2_coordinates = [[215, 560], [255, 560],
                                    [365, 353], [265, 350]]
        self.list_3_coordinates = [[0, 250], [20, 250],
                                    [90, 330], [30, 330]]
        self.list_4_coordinates = [[0, 410], [20, 410],
                                    [90, 330], [30, 330]]
        self.list_1_coordinates = [[505, 330], [495, 345], [480, 360],
                                    [50, 345], [30, 330],
                                    [50, 315], [480, 300],[495, 315]]
        self.p_list = [self.list_0_coordinates, self.list_1_coordinates, self.list_2_coordinates, self.list_3_coordinates, self.list_4_coordinates]
        #Тут Отрисовка перед циклом

    def run_while(self):
        while True:
            self.conter += 1
            if not self.bool_pos:
                self.drawing_in_a_loop()
            self.event_handler()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    self.bool_pos = 0
            if event.type == pygame.MOUSEBUTTONDOWN :
                self.pos = event.pos
                for p in self.p_list:
                    if self.point_in_polygon(p, self.pos):
                        self.fire()
                        self.bool_pos = not self.bool_pos
                        break
                #print(self.pos)
                #if self.pos

    def drawing_in_a_loop(self):
        if self.list_4_coordinates[0][0] >=  pygame.display.Info().current_w:
            self.list_0_coordinates = [[-290, 100], [-250, 100], [-140, 307], [-240, 310]]
            self.list_2_coordinates = [[-290, 560], [-250, 560], [-140, 353], [-240, 350]]
            self.list_3_coordinates = [[-505, 250], [-485, 250], [-415, 330], [-475, 330]]
            self.list_4_coordinates = [[-505, 410], [-485, 410], [-415, 330], [-475, 330]]
            self.list_1_coordinates = [[0, 330], [-10, 345], [-25, 360], [-455, 345],
                                    [-475, 330], [-455, 315], [-25, 300], [-10, 315]]
            self.p_list = [self.list_0_coordinates, self.list_1_coordinates, self.list_2_coordinates, self.list_3_coordinates, self.list_4_coordinates]

        self.screen.fill((125,249,255))
        for i in range(len(self.list_0_coordinates)):
            self.list_0_coordinates[i][0] += self.x
        for i in range(len(self.list_1_coordinates)):
            self.list_1_coordinates[i][0] += self.x
        for i in range(len(self.list_2_coordinates)):
            self.list_2_coordinates[i][0] += self.x
        for i in range(len(self.list_3_coordinates)):
            self.list_3_coordinates[i][0] += self.x
        for i in range(len(self.list_4_coordinates)):
            self.list_4_coordinates[i][0] += self.x

        pygame.draw.lines(self.screen, "black", True, self.list_0_coordinates, 5)
        pygame.draw.lines(self.screen, "black", True, self.list_2_coordinates, 5)
        pygame.draw.polygon(self.screen, (181,184,187), self.list_0_coordinates)
        pygame.draw.polygon(self.screen, (181,184,187), self.list_2_coordinates)
        pygame.draw.polygon(self.screen, (181,184,187), self.list_3_coordinates)
        pygame.draw.polygon(self.screen, (181,184,187), self.list_4_coordinates)
        pygame.draw.aalines(self.screen, "black", True, self.list_3_coordinates, 5)
        pygame.draw.aalines(self.screen, "black", True, self.list_4_coordinates, 5)
        pygame.draw.polygon(self.screen, (181,184,187), self.list_1_coordinates)
        pygame.draw.aalines(self.screen, "black", True, self.list_1_coordinates, 5)

    def point_in_polygon(self, p, point):
        result = False
        size = len(p)
        j = size - 1
        for i in range(size):
            if (p[i][1] < point[1] and p[j][1] >= point[1] or p[j][1] < point[1]
            and p[i][1] >= point[1]) and (p[i][0] + (point[1] - p[i][1]) / (p[j][1] - p[i][1]) * (p[j][0] - p[i][0]) < point[0]):
                result = not result
            j = i
        return result

    def fire(self):
        pygame.draw.circle(self.screen, "red", self.pos, 3)
        pygame.draw.circle(self.screen, "red", self.pos, 7, 1)
        pygame.draw.circle(self.screen, "red", self.pos, 9, 1)

Main(24).run_while()
