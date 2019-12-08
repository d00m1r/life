'''
sets and allows you to work with the field for the game of life
'''
import pygame

SCALE = 5
screen = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 69, 0)#orangered
GREEN = (0, 200, 0)
BLUE = (65, 105, 255)#royal blue
YELLOW = (225, 225, 0)

def set_mode(size, bcolor = GREY, scale = SCALE):
    """
    Создает окно заданного размера
    :param size: размеры окна в клетках
    :param bcolor: цвет границ
    :param scale: размер клеток (20 пикс. по дефолту)
    :return: "холст" окна
    """
    global screen

    screen = pygame.display.set_mode([size[0] * SCALE, size[1] * SCALE])

    for i in range(0, size[0]):
        pygame.draw.line(screen, bcolor, [i * SCALE, 0], [i * SCALE, size[1] * SCALE])
    for i in range(0, size[1]):
        pygame.draw.line(screen, bcolor, [0, i * SCALE], [size[0] * SCALE, i * SCALE])

    return screen


def fill(screen_color, bcolor=[200, 200, 200]):
    """
    Заливает окно цветом
    :param screen_color: цвет окна
    :param bcolor: цвет границ
    """
    global screen
    surface = screen
    surface.fill(screen_color)
    w, h = surface.get_size()
    for i in range(0, w):
        pygame.draw.line(surface, bcolor, [i * SCALE, 0], [i * SCALE, h * SCALE])
    for i in range(0, h):
        pygame.draw.line(surface, bcolor, [0, i * SCALE], [w * SCALE, i * SCALE])


def draw_cell(surface, color, pos):
    return pygame.draw.rect(surface, color, [pos[0] * SCALE, pos[1] * SCALE,  SCALE-1, SCALE-1])
