import pygame
import random
import sys


grid = [[0 for _ in range(9)] for _ in range(9)]

def is_valid(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[r][col] for r in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == num:
                return False
    return True

def fill_grid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if fill_grid(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True  # Base case: grid is fully filled

def count_solutions(grid, limit=2):
    def solve(grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    count = [0]
    def count_recursive(grid):
        if count[0] >= limit:
            return
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            count_recursive(grid)
                            grid[row][col] = 0
                    return
        count[0] += 1

    count_recursive([row[:] for row in grid])
    return count[0]

def remove_numbers(grid):
    attempts = 81
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while grid[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

        backup = grid[row][col]
        grid[row][col] = 0

        copy_grid = [r[:] for r in grid]
        if count_solutions(copy_grid) != 1:
            grid[row][col] = backup  # Undo removal
        attempts -= 1
    return grid

fill_grid(grid)
grid = remove_numbers(grid)

            
for row_index, row in enumerate(grid):
    if row_index % 3 == 0:
        print("-" * 25)
    output = ""
    for col_index, num in enumerate(row):
        if col_index % 3 == 0:
            output += "| "
        output += str(num) + " "
        if col_index == 8:
            output += "|"
    print(output)
print("-" * 25)


pygame.init()
screen = pygame.display.set_mode((540, 540))

def draw_grid(screen):
    for i in range(10):  # 0 through 9 for 9 cells + edge
        width = 2
        if i % 3 == 0:
            width = 4  # Thicker line every 3 cells
        # Vertical lines
        pygame.draw.line(screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), width)
        # Horizontal lines
        pygame.draw.line(screen, (0, 0, 0), (0, i * 60), (540, i * 60), width)
        
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill((255, 255, 255))
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num != 0:
                font = pygame.font.Font(None, 40)
                text = font.render(str(num), True, (0, 0, 0))
                text_rect = text.get_rect(center=(col * 60 + 30, row * 60 + 30))
                screen.blit(text, text_rect)
    draw_grid(screen)
                
    pygame.display.flip()


pygame.quit()
sys.exit()