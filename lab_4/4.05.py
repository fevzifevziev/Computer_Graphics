import pygame, sys, math
import numpy as np
import random

class Main:
    def __init__(self, fps=60):
        self.fps = fps
        pygame.init()
        self.screen = pygame.display.set_mode((1080,720))
        self.clock = pygame.time.Clock()
        self.display_width, self.display_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        while True:

            self.set_points()

    def set_points(self):
        self.coordinates = []
        self.coordinatesNEW = []
        self.pos = (-5,-5)

        self.bool_start = 0
        self.bool_pos = 0

        while True:
            self.screen.fill("white")
            if len(self.coordinates) > 1:
                for i in range(len(self.coordinates)):
                    pygame.draw.aalines(self.screen, "black", True, self.coordinates)
            else:
                self.screen.fill("black", (self.pos, (3, 3)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_q:
                        if len(self.coordinates) > 2:
                            self.bool_start = 1
                            self.start()
                            pygame.display.set_caption("Задание точек завершено")
                        else:
                            pygame.display.set_caption("Нужно задать как минимум 3 точки!")
                    elif event.key == pygame.K_w:
                        self.bool_start = 0
                        self.coordinates = []
                        self.coordinatesNEW = []
                        self.pos = (-5, -5)
                        pygame.display.set_caption("Точки сброшены!")
                if event.type == pygame.MOUSEBUTTONDOWN :
                    self.pos = event.pos
                    self.bool_pos = 1
                    if not self.bool_start:
                        self.coordinates.append(self.pos)
                        pygame.display.set_caption(str(self.pos) + ".  Для начала триангуляции нажмите на - q")
            if self.bool_start == 1:
                break

            pygame.display.flip()
            self.clock.tick(self.fps)

    def start(self):
        self.pos = (0, 0)
        self.bool_pos = 0

        self.screen.fill("white")
        self.print_polygon(self.coordinates)

        if len(self.coordinates) > 0:
            for coords in self.coordinates:
                self.coordinatesNEW.append(coords)
        while True:
            self.triangles = []
            if not self.is_clockwise():
                self.coordinates.reverse()
            if_done = self.triangulate()
            if if_done:
                pygame.display.set_caption("Триангуляция прошла успешно.    Сброс точек - w")
                self.coordinates = []
                if len(self.coordinatesNEW) > 0:
                    for coords in self.coordinatesNEW:
                        self.coordinates.append(coords)

                hasPointOfPolygonMouse = self.hasPointOfPolygonMouse()
                if hasPointOfPolygonMouse[0] and self.bool_pos:
                    pygame.draw.polygon(self.screen, (random.randint(0, 256)%256,random.randint(0, 256)%256, random.randint(0, 256)%256), hasPointOfPolygonMouse[1])
                self.bool_pos = 0
            else:
                self.bool_start = 0
                self.coordinates = []
                self.coordinatesNEW = []
                self.pos = (-5, -5)
                pygame.display.set_caption("Произошла ошибка точки сброшены")
                self.set_points()
            #обработчик событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for tr in self.triangles:
                        print(tr)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE:
                        for tr in self.triangles:
                            print(tr)
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_w:
                        self.bool_start = 0
                        self.coordinates = []
                        self.coordinatesNEW = []
                        self.pos = (-5, -5)
                        pygame.display.set_caption("Точки сброшены!")
                        self.set_points()

                if event.type == pygame.MOUSEBUTTONDOWN :
                    self.pos = event.pos
                    self.bool_pos = 1
            pygame.display.flip()
            self.clock.tick(self.fps)

    def is_clockwise(self):
        assert len(self.coordinates) > 0
        s = 0.0
        for p1, p2 in zip(self.coordinates, self.coordinates[1:] + [self.coordinates[0]]):
            s += (p2[0] - p1[0]) * (p2[1] + p1[1])
        return s > 0.0

    def print_polygon(self, coordinates):
        pygame.draw.aalines(self.screen, "black", True, coordinates)

    # 2 Левая тройка векторов?
    def isLeft(self, i):
        A = self.coordinates[i%len(self.coordinates)]
        B = self.coordinates[(i+1)%len(self.coordinates)]
        C = self.coordinates[(i+2)%len(self.coordinates)]

        AB = {"x": B[0] - A[0], "y": B[1] - A[1]}
        AC = {"x": C[0] - A[0], "y": C[1] - A[1]}

        return AB["x"] * AC["y"] - AC["x"] * AB["y"] < 0

    def hasPointOfPolygonMouse(self):
        for triangle in self.triangles:
            A = triangle[0]
            B = triangle[1]
            C = triangle[2]
            for j in range(0, len(self.coordinates)):
                VP0  = self.cross(A, B, self.pos)
                VP1  = self.cross(B, C, self.pos)
                VP2  = self.cross(C, A, self.pos)
                s_l = np.sign([VP0, VP1, VP2])

                if s_l[0] == s_l[1] and s_l[1] == s_l[2] and s_l[0] == s_l[2]:
                     return (True, triangle)

                for h in range(len(s_l)):
                    if s_l[h] == 0:
                        if s_l[(h+1)%len(s_l)] == s_l[(h+2)%len(s_l)]:
                            return (True, triangle)
        return (False, (None, None))

    def cross(self, P1, P2, P): #ABxAP, BCxBP and CAxCP.
        vector_P1_P2 = (P2[0]-P1[0], P2[1]-P1[1])
        vector_P1_P = (P[0]-P1[0], P[1]-P1[1])

        return np.cross(vector_P1_P2, vector_P1_P)

    # 3 Есть ли другие точки внутри рассматриваемого треугольника?
    def hasPointOfPolygon(self, i):
        A = self.coordinates[i%len(self.coordinates)]
        B = self.coordinates[(i+1)%len(self.coordinates)]
        C = self.coordinates[(i+2)%len(self.coordinates)]

        for j in range((i+3)%len(self.coordinates), len(self.coordinates)+i%len(self.coordinates)):
            VP0  = self.cross(A, B, self.coordinates[j%len(self.coordinates)])
            VP1  = self.cross(B, C, self.coordinates[j%len(self.coordinates)])
            VP2  = self.cross(C, A, self.coordinates[j%len(self.coordinates)])
            s_l = np.sign([VP0, VP1, VP2])

            if s_l[0] == s_l[1] and s_l[1] == s_l[2] and s_l[0] == s_l[2]:
                 return False

            for h in range(len(s_l)):
                if s_l[h] == 0:
                    if s_l[(h+1)%len(s_l)] == s_l[(h+2)%len(s_l)]:
                        return False
        return True

    #Триангуляция
    def triangulate(self):
        i = 0
        crt = 0
        while len(self.coordinates) >= 3:
            crt += 1
            if self.isLeft(i) and self.hasPointOfPolygon(i):
                self.triangles.append([self.coordinates[(i)%len(self.coordinates)], self.coordinates[(i+1)%len(self.coordinates)], self.coordinates[(i+2)%len(self.coordinates)]])
                if len(self.coordinates) == 3:
                    break
                del self.coordinates[(i+1)%len(self.coordinates)]
            else:
                i += 1
                i = i%len(self.coordinates)
            if crt == len(self.coordinates) ** 2:
                return 0
        return 1

Main(24)
