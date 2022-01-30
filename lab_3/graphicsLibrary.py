import pygame
import math
#-------------------------------------------------------------------------------

def pixel(surface, color, pos):
    surface.fill(color, (pos, (1, 1)))
#-------------------------------------------------------------------------------
# №1 Прямоугольник
def draw(surface, pos, color="white", borderFull=1, borderColor="black" , borderLeft=None, borderRight=None, borderTop=None, borderBottom=None, transparency=0):
    x1 = pos[0][0]
    x2 = pos[1][0]
    y1 = pos[0][1]
    y2 = pos[1][1]

    #Если пармаметтры не заполнены, то примут значение borderFull
    if borderLeft == None:
         borderLeft = borderFull
    if borderRight == None:
         borderRight = borderFull
    if borderTop == None:
         borderTop = borderFull
         borderBottom = borderFull

    #Внутреняя область
    listBorder = [borderLeft, borderRight, borderTop, borderBottom, borderFull]
    min = borderFull
    summ = 0
    for i in listBorder:
        summ += i
        if i < min:
            min = i
    if not((x2-x1)/2>borderFull and (y2-y1)/2>borderFull):
        min = 0

    if not transparency:
        for x in range(x1+min, x2+1-min):
            for y in range(y1+min, y2+1-min):
                pixel(surface, color, (x, y))

    #Рамка
    if summ != 0 and (x2-x1)/2>borderFull and (y2-y1)/2>borderFull :
        draw(surface, [[x1,y1], [x2,y1+borderTop]], color=borderColor, borderFull=0)
        draw(surface, [[x2-borderRight,y1], [x2,y2]], color=borderColor, borderFull=0)
        draw(surface, [[x1,y2-borderBottom], [x2,y2]], color=borderColor, borderFull=0)
        draw(surface, [[x1,y1], [x1+borderLeft,y2]], color=borderColor, borderFull=0)

#-------------------------------------------------------------------------------
# №2 Окружность
def circle(surface, x0, y0, radius, color="white", T_F=0):
    while radius > 1:
        x = 0; y = radius; gap = 0; delta = (2 - 2 * radius)
        while (y >= 0):
            pixel(surface, color, [x0 + x, y0 + y])
            pixel(surface, color, [x0 + x, y0 - y])
            pixel(surface, color, [x0 - x, y0 - y])
            pixel(surface, color, [x0 - x, y0 + y])
            gap = 2 * (delta + y) - 1
            if (delta < 0 and gap <= 0):
                x += 1
                delta += 2 * x + 1
                continue
            if (delta > 0 and gap > 0):
                y -= 1
                delta -= 2 * y + 1
                continue
            x += 1
            delta += 2 * (x - y)
            y -= 1
        radius -= 1

#-------------------------------------------------------------------------------
def alines(surface, borderColor, list_ccord, T_F=0):
    if T_F:
        draw_line(surface, borderColor, x1 = list_ccord[0][0], y1=list_ccord[0][1], x2=list_ccord[-1][0], y2=list_ccord[-1][1])
    for i in range(len(list_ccord)-1):
        draw_line(surface, borderColor, x1 = list_ccord[i][0], y1=list_ccord[i][1], x2=list_ccord[i+1][0], y2=list_ccord[i+1][1])
#-------------------------------------------------------------------------------

def polygon(surface, borderColor, list_ccord):
    for x in range( min(list_ccord, 0), max(list_ccord, 0) ):
        for y in range( min(list_ccord, 1), max(list_ccord, 1) ):
            if point_in_polygon(list_ccord, [x, y]):
                pixel(surface, borderColor, [x, y])
def min(l, b):
    minimum = l[0][b]
    for i in l:
        if i[b] < minimum:
            minimum = i[b]
    return minimum

def max(l, b):
    maximum = l[0][b]
    for i in l:
        if i[b] > maximum:
            maximum = i[b]
    return maximum

def point_in_polygon(p, point):
    result = False
    size = len(p)
    j = size - 1
    for i in range(size):
        if (p[i][1] < point[1] and p[j][1] >= point[1] or p[j][1] < point[1]
        and p[i][1] >= point[1]) and (p[i][0] + (point[1] - p[i][1]) / (p[j][1] - p[i][1]) * (p[j][0] - p[i][0]) < point[0]):
            result = not result
        j = i
    return result
#-------------------------------------------------------------------------------

def triangle(surface, borderColor, list_ccord):
    if len(list_ccord)==3:
        alines(surface, borderColor, list_ccord, T_F=1)

#-------------------------------------------------------------------------------
def draw_line(surface, borderColor, x1=0, y1=0, x2=0, y2=0):

        dx = x2 - x1
        dy = y2 - y1

        sign_x = 1 if dx>0 else -1 if dx<0 else 0
        sign_y = 1 if dy>0 else -1 if dy<0 else 0

        if dx < 0: dx = -dx
        if dy < 0: dy = -dy

        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy

        x, y = x1, y1

        error, t = el/2, 0

        pixel(surface, borderColor, (x, y))

        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            pixel(surface, borderColor, (x, y))

#-------------------------------------------------------------------------------
def drawSpline(surface, color, args):
    coords = [[args[0], args[1]]]
    num = 0
    for i in range(0, len(args), 2):
        coords.append([args[i], args[i+1]])
        if i > 0:
            deltaX = coords[int(i/2+1)][0] - coords[int(i/2)][0]
            deltaY = coords[int(i/2+1)][1] - coords[int(i/2)][1]
            num += math.sqrt(deltaX * deltaX + deltaY * deltaY)

    coords.append(coords[-1])

    for i in range(1, len(coords)-2):
        a = []
        b = []
        arrs = _SplineCoefficient(i, coords)   # считаем коэффициенты q

        for j in range(int(num)):
            points = []                           # создаём массив промежуточных точек
            t = j / num                       # шаг интерполяции
                                              # передаём массиву точек значения по методу beta-spline
            points.append(arrs[0][0] + t * (arrs[0][1] + t * (arrs[0][2] + t * arrs[0][3])))
            points.append(arrs[1][0] + t * (arrs[1][1] + t * (arrs[1][2] + t * arrs[1][3])))

            pixel(surface, color, (points[0], points[1]))


def _SplineCoefficient(i, coords):      # в функции рассчитываются коэффициенты a0-a3, b0-b3
    arrs = [[], []]

    arrs[0].append((coords[i - 1][0] + 4*coords[i][0] + coords[i + 1][0])/6)
    arrs[0].append((-coords[i - 1][0] + coords[i + 1][0])/2)
    arrs[0].append((coords[i - 1][0] - 2*coords[i][0] + coords[i + 1][0])/2)
    arrs[0].append((-coords[i - 1][0] + 3*coords[i][0] - 3*coords[i + 1][0] + coords[i + 2][0])/6)

    arrs[1].append((coords[i - 1][1] + 4*coords[i][1] + coords[i + 1][1])/6)
    arrs[1].append((-coords[i - 1][1] + coords[i + 1][1])/2)
    arrs[1].append((coords[i - 1][1] - 2*coords[i][1] + coords[i + 1][1])/2)
    arrs[1].append((-coords[i - 1][1] + 3*coords[i][1] - 3*coords[i + 1][1] + coords[i + 2][1])/6)

    return arrs
#-------------------------------------------------------------------------------
