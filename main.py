import pygame, sys
from maze import Maze
from config import HAUTEUR, LARGEUR, NB_COLONNES, NB_LIGNES, TAILLE_CELLULE, FPS

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()
maze = Maze(NB_LIGNES, NB_COLONNES)
maze.generate_recursive_backtracking()
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    fenetre.fill((0, 0, 0))
    maze.draw(fenetre, TAILLE_CELLULE)
    pygame.display.flip()
    clock.tick(FPS)
