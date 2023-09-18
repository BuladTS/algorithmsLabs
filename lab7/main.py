# import pygame
# from random import choice
#
# RES = WIDTH, HEIGHT = 1202, 702
# TILE = 30
# cols, rows = WIDTH // TILE, HEIGHT // TILE
#
# pygame.init()
# sc = pygame.display.set_mode(RES)
# clock = pygame.time.Clock()
#
#
# def check_cell(x, y, grid_cells):
#     if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
#         return False
#     return grid_cells[x + y * cols]
#
#
# class Cell:
#     def __init__(self, x, y):
#         self.x, self.y = x, y
#         self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
#         self.visited = False
#         self.solution = False
#         self.visited_solution = False
#
#     def draw(self):
#         x, y = self.x * TILE, self.y * TILE
#         if self.visited:
#             pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))
#
#         if self.solution:
#             pygame.draw.rect(sc, pygame.Color('blue'), (self.x * TILE + 2, self.y * TILE + 2,
#                                                         TILE - 4, TILE - 4), border_radius=50)
#
#         if self.walls['top']:
#             pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
#         if self.walls['right']:
#             pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE,), 2)
#         if self.walls['bottom']:
#             pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x, y + TILE), 2)
#         if self.walls['left']:
#             pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), 2)
#
#     def check_neighbors_walls(self, grid_cells):
#         neighbors = []
#         top = check_cell(self.x, self.y - 1, grid_cells)
#         bottom = check_cell(self.x, self.y + 1, grid_cells)
#         right = check_cell(self.x + 1, self.y, grid_cells)
#
#         if top and check_walls_build(self, top):
#             neighbors.append(top)
#
#         if right and check_walls_build(self, right):
#             neighbors.append(right)
#         return choice(neighbors) if neighbors else bottom
#
#     def check_neighbors_solution(self, grid_cells):
#         neighbors = []
#         top = check_cell(self.x, self.y - 1, grid_cells)
#         bottom = check_cell(self.x, self.y + 1, grid_cells)
#         left = check_cell(self.x + 1, self.y, grid_cells)
#         right = check_cell(self.x - 1, self.y, grid_cells)
#
#         if top and check_walls_solution(self, top) and not top.visited_solution:
#             neighbors.append(top)
#         if bottom and check_walls_solution(self, bottom) and not bottom.visited_solution:
#             neighbors.append(bottom)
#         if right and check_walls_solution(self, right) and not right.visited_solution:
#             neighbors.append(right)
#         if left and check_walls_solution(self, left) and not left.visited_solution:
#             neighbors.append(left)
#         return choice(neighbors) if neighbors else False
#
#
# def check_walls_build(cell_1, cell_2):
#     dx = cell_1.x - cell_2.x
#     if dx == -1:
#         if cell_1.walls['right'] != cell_2.walls['left']:
#             return False
#     elif dx == 1:
#         if cell_1.walls['left'] != cell_2.walls['right']:
#             return False
#
#     dy = cell_1.y - cell_2.y
#     if dy == 1:
#         if cell_1.walls['top'] != cell_2.walls['bottom']:
#             return False
#     elif dy == -1:
#         if cell_1.walls['bottom'] != cell_2.walls['top']:
#             return False
#
#     return True
#
#
# def check_walls_solution(cell_1, cell_2):
#     dx = cell_1.x - cell_2.x
#     if dx == -1 and not cell_1.walls['right'] and not cell_2.walls['left']:
#         return True
#     elif dx == 1 and not cell_1.walls['left'] and not cell_2.walls['right']:
#         return True
#     dy = cell_1.y - cell_2.y
#     if dy == 1 and not cell_1.walls['top'] and not cell_2.walls['bottom']:
#         return True
#     elif dy == -1 and not cell_1.walls['bottom'] and not cell_2.walls['top']:
#         return True
#
#     return False
#
#
# def remove_walls(current_cell, next_cell):
#     dx = current_cell.x - next_cell.x
#     if dx == 1:
#         current_cell.walls['left'] = False
#         next_cell.walls['right'] = False
#     elif dx == -1:
#         current_cell.walls['right'] = False
#         next_cell.walls['left'] = False
#     dy = current_cell.y - next_cell.y
#     if dy == 1:
#         current_cell.walls['top'] = False
#         next_cell.walls['bottom'] = False
#     elif dy == -1:
#         current_cell.walls['bottom'] = False
#         next_cell.walls['top'] = False
#
#
# def main():
#     grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
#     current_cell = grid_cells[0]
#     stack = []
#     i_next = 1
#     flag_draw = True
#     flag_solution = True
#
#     while True:
#         sc.fill(pygame.Color('darkslategray'))
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#
#         [cell.draw() for cell in grid_cells]
#         current_cell.visited = True
#         # current_cell.draw_current_cell()
#
#         if flag_draw:
#             if i_next == len(grid_cells):
#                 flag_draw = False
#                 remove_walls(current_cell, current_cell.check_neighbors_walls(grid_cells))
#                 current_cell = grid_cells[0]
#                 next_cell = False
#             else:
#                 next_cell = grid_cells[i_next]
#                 i_next += 1
#             if next_cell:
#                 next_cell.visited = True
#                 remove_walls(current_cell, current_cell.check_neighbors_walls(grid_cells))
#                 current_cell = next_cell
#         elif flag_solution:
#             next_cell = current_cell.check_neighbors_solution(grid_cells)
#             grid_cells[0].solution = True
#             if next_cell:
#                 next_cell.visited_solution = True
#                 next_cell.solution = True
#                 stack.append(current_cell)
#                 current_cell = next_cell
#             elif stack:
#                 current_cell.solution = False
#                 current_cell = stack.pop()
#
#             if current_cell.x == cols - 1 and current_cell.y == rows - 1:
#                 flag_solution = False
#
#         pygame.display.flip()
#         clock.tick(30)
#
#
# def draw_maze(grid_cells):
#     current_cell = grid_cells[0]
#     i_next = 1
#     flag_draw = True
#     while flag_draw:
#         [cell.draw() for cell in grid_cells]
#         current_cell.visited = True
#
#         if flag_draw:
#             if i_next == len(grid_cells):
#                 next_cell = grid_cells[-1]
#                 flag_draw = False
#                 i_next = 1
#             else:
#                 next_cell = grid_cells[i_next]
#                 i_next += 1
#             if next_cell:
#                 next_cell.visited = True
#                 remove_walls(current_cell, current_cell.check_neighbors_walls(grid_cells))
#                 current_cell = next_cell
#
#
# if __name__ == '__main__':
#     main()
