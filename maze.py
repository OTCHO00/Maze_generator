import random
from cell import Cell
from collections import deque

class Maze:
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.start = (0, 0)
        self.end = (self.row - 1, self.col - 1)
        self.generated = False
        self.solved = False
        self.path = []
        self.maze = []

        for row in range(0, self.row):
            ligne = []
            for col in range(0, self.col):
                cell = Cell(row, col)
                ligne.append(cell)
            self.maze.append(ligne)

    def get_cell(self, row, col):
        
        return self.maze[row][col]

    def get_voisins(self, cell):
        
        voisins = []

        if 0 <= cell.row - 1 < self.row and 0 <= cell.col < self.col:
            voisins.append((cell.row - 1, cell.col, "N"))
        if 0 <= cell.row + 1 < self.row and 0 <= cell.col < self.col:
            voisins.append((cell.row + 1, cell.col, "S"))
        if 0 <= cell.row < self.row and 0 <= cell.col + 1 < self.col:
            voisins.append((cell.row, cell.col + 1, "E"))
        if 0 <= cell.row < self.row and 0 <= cell.col - 1 < self.col:
            voisins.append((cell.row, cell.col - 1, "W"))

        return voisins
    
    def get_voisin_inconnu(self, cell):

        voisins = self.get_voisins(cell)
        inconnus = []

        for (row, col, direction) in voisins:
            voisin = self.get_cell(row, col)
            if not voisin.visited:
                inconnus.append((row, col))
        
        return inconnus

    def remove_walls_between(self, cell1, cell2):
        
        if cell2.row < cell1.row:
            cell1.remove_wall("N")
            cell2.remove_wall("S")

        if cell2.row > cell1.row:
            cell1.remove_wall("S")
            cell2.remove_wall("N")
        
        if cell2.col > cell1.col:
            cell1.remove_wall("E")
            cell2.remove_wall("W")
        
        if cell2.col < cell1.col:
            cell1.remove_wall("W")
            cell2.remove_wall("E")

    def generate_recursive_backtracking(self):

        l = deque()
        depart = self.get_cell(self.start[0], self.start[1])
        depart.visited = True
        l.append(depart)

        while len(l) != 0:

            sommet = l[-1]
            voisins_non_visite = self.get_voisin_inconnu(sommet)

            if len(voisins_non_visite) >= 1:

                row, col = random.choice(voisins_non_visite)
                voisin = self.get_cell(row, col)
                self.remove_walls_between(sommet, voisin)
                voisin.visited = True
                l.append(voisin)

            else: 
                l.pop()

        self.generated = True

    def heuristic(self, cell1, cell2):

        distance = abs(cell1.row - cell2.row) + abs(cell1.col - cell2.col)

        return distance

    def get_accessible_neighbors(self, cell):
        
        voisin_accessible = []

        if not cell.has_wall("N") and 0 <= cell.row - 1 < self.row:
            voisin_accessible.append(self.get_cell(cell.row - 1, cell.col))
        
        if not cell.has_wall("S") and 0 <= cell.row + 1 < self.row:
            voisin_accessible.append(self.get_cell(cell.row + 1, cell.col))

        if not cell.has_wall("E") and 0 <= cell.col + 1 < self.col:
            voisin_accessible.append(self.get_cell(cell.row, cell.col + 1))

        if not cell.has_wall("W") and 0 <= cell.col - 1 < self.col:
            voisin_accessible.append(self.get_cell(cell.row, cell.col - 1))

        return voisin_accessible

    def solve_astar(self):
        
        open_set = []
        depart = self.get_cell(self.start[0], self.start[1])
        arrive = self.get_cell(self.end[0], self.end[1])
        depart.h_score = self.heuristic(depart, arrive)
        depart.g_score = 0
        depart.f_score = depart.g_score + depart.h_score
        open_set.append(depart)

        while len(open_set) != 0:

            current = min(open_set, key=lambda x: x.f_score)
            open_set.remove(current)

            if current == arrive:

                self.path.append(current)

                while current.parent != None: 

                    self.path.append(current.parent)
                    current = current.parent
                
                self.path.reverse()
                self.solved = True

                break

            else:

                for voisin in self.get_accessible_neighbors(current):
                    tentative_g_score = current.g_score + 1

                    if tentative_g_score < voisin.g_score:
                        voisin.g_score = tentative_g_score
                        voisin.parent = current
                        voisin.h_score = self.heuristic(voisin, arrive)
                        voisin.f_score = voisin.g_score + voisin.h_score 

                        if voisin not in open_set:
                            open_set.append(voisin)

                


    def draw(self, fenetre, cell_size):
        
        for row in range(0, self.row):
            for col in range(0, self.col):
                cell = self.get_cell(row, col)
                cell.draw(fenetre, cell_size)
