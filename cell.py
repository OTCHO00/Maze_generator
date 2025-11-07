import pygame
from config import C_MUR

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.wall = { "N" : True,
                      "S" : True,
                      "E" : True,
                      "W" : True
                    }
        self.visited = False
        self.parent = None
        self.g_score = float('inf')
        self.h_score = 0
        self.f_score = float('inf')

    def remove_wall(self, direction):

        self.wall[direction] = False

    def has_wall(self, direction):

        return self.wall[direction]

    def draw(self, fenetre, cell_size):

        x, y = self.col * cell_size, self.row * cell_size

        if self.has_wall("N"):
            pygame.draw.line(fenetre, C_MUR, (x, y), (x + cell_size, y))
        if self.has_wall("S"):
            pygame.draw.line(fenetre, C_MUR, (x, y + cell_size), (x + cell_size, y + cell_size))
        if self.has_wall("E"):
            pygame.draw.line(fenetre, C_MUR, (x + cell_size, y), (x + cell_size, y + cell_size))
        if self.has_wall("W"):
            pygame.draw.line(fenetre, C_MUR, (x, y), (x, y + cell_size))