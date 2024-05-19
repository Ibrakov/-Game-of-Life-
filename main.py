from pygame import *

font.init()


class Cell(sprite.Sprite):
    def __init__(self, x, y, size, is_alive=False):
        super().__init__()

        self.image = Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_alive = is_alive

    def update(self):
        fill_color = dead_cell_color
        if self.is_alive:
            fill_color = alive_cell_color

        self.image.fill(fill_color)
        win.blit(self.image, self.rect)


def update_state_cell(matrix: list[list[Cell]]):
    len_col = len(matrix)
    len_row = len(matrix[0])

    next_state = [
        [cell.is_alive for cell in row] for row in matrix
    ]

    for i in range(len_col):
        for j in range(len_row):
            count = sum([
                matrix[(i - 1) % len_col][(j - 1) % len_row].is_alive,
                matrix[i % len_col][(j - 1) % len_row].is_alive,
                matrix[(i + 1) % len_col][(j - 1) % len_row].is_alive,
                matrix[(i - 1) % len_col][j % len_row].is_alive,
                matrix[(i + 1) % len_col][j % len_row].is_alive,
                matrix[(i - 1) % len_col][(j + 1) % len_row].is_alive,
                matrix[i % len_col][(j + 1) % len_row].is_alive,
                matrix[(i + 1) % len_col][(j + 1) % len_row].is_alive
            ])

            if matrix[i][j].is_alive:
                next_state[i][j] = count == 2 or count == 3
            else:
                next_state[i][j] = count == 3

    for i in range(len_col):
        for j in range(len_row):
            matrix[i][j].is_alive = next_state[i][j]


def count_alive_cells(matrix: list[list[Cell]]) -> int:
    count = 0
    for row in matrix:
        for cell in row:
            if cell.is_alive:
                count += 1
    return count


background_color = (255, 255, 255)
alive_cell_color = (0, 255, 0)
dead_cell_color = (89, 70, 89)

width, height = 500, 500
cell_size = 9
margin = 1

win = display.set_mode((width, height))
display.set_caption("Game of life")

cells = []
for i in range((height-50) // (cell_size+margin)):
    row = []
    y = (cell_size + margin) * i
    for j in range(width // (cell_size+margin)):
        row.append(Cell((cell_size + margin) * j, y, cell_size))
    cells.append(row)

game, pause = True, True
FPS = 10

generation = 0
max_generation = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_p:
                pause = not pause
        if e.type == MOUSEBUTTONDOWN:
            row = e.pos[1] // (cell_size + margin)
            column = e.pos[0] // (cell_size + margin)
            if row < len(cells) and column < len(cells[0]):
                cells[row][column].is_alive = not cells[row][column].is_alive

    win.fill(background_color)
    for row in cells:
        for cell in row:
            cell.update()

    if not pause:
        generation += 1
        update_state_cell(cells)
    else:
        win.blit(font.SysFont("Arial", 16, bold=True).render(
            "||", True, (0, 0, 0)
        ), (10, height - 40))

    if not count_alive_cells(cells):
        max_generation = max(max_generation, generation)
        generation = 0

    win.blit(font.SysFont("Arial", 16, bold=True).render(
        f"Gen = {generation}", True, (0, 0, 0)
    ), (30, height - 40))

    win.blit(font.SysFont("Arial", 16, bold=True).render(
        f"Alive = {count_alive_cells(cells)}", True, (0, 0, 0)
    ), (120, height - 40))

    win.blit(font.SysFont("Arial", 16, bold=True).render(
        f"MaxGen = {max_generation}", True, (0, 0, 0)
    ), (210, height - 40))

    display.update()
    time.Clock().tick(FPS)
