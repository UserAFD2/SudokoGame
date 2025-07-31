import pygame
import random
import sys


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
    numbers_left = {9: 9, 8: 9, 7: 9, 6: 9, 5: 9, 4: 9, 3: 9, 2: 9, 1: 9}
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
        else:
            numbers_left[backup] -= 1
        attempts -= 1
    return grid, numbers_left

import copy

grid = [[0 for _ in range(9)] for _ in range(9)]
fill_grid(grid)
solved_puzzle = copy.deepcopy(grid)
grid, numbers_left = remove_numbers(grid)

            
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
screen = pygame.display.set_mode((800, 800))

def draw_grid(grid_surface, mouse_pos, incorrect_number, incorrect_pos):
    mouse_grid_pos = int(mouse_pos[0] / 60), int(mouse_pos[1] / 60)
    mouse_grid_pos = (mouse_grid_pos[0] * 60 - 120, mouse_grid_pos[1] * 60 - 120)
    for i in range(9):
        pygame.draw.rect(grid_surface, (150, 150, 150), (mouse_grid_pos[0], i*60, 60, 60))
        pygame.draw.rect(grid_surface, (150, 150, 150), (i*60, mouse_grid_pos[1], 60, 60))
    if incorrect_number:
        pygame.draw.rect(grid_surface, (150, 10, 10), (incorrect_pos[0], incorrect_pos[1], 60, 60))
        
    #pygame.draw.rect(grid_surface, (100, 100, 100), (mouse_grid_pos[0], mouse_grid_pos[1], 60, 60))
    for i in range(10):  # 0 through 9 for 9 cells + edge
        width = 2
        if i % 3 == 0:
            width = 4  # Thicker line every 3 cells
        # Vertical lines
        pygame.draw.line(grid_surface, (0, 0, 0), (i * 60, 0), (i * 60, 540), width)
        # Horizontal lines
        pygame.draw.line(grid_surface, (0, 0, 0), (0, i * 60), (540, i * 60), width)

print("Solved puzzle: ")
for row_index, row in enumerate(solved_puzzle):
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
grid_surface = pygame.Surface((540, 540))
grid_surface.fill((255, 255, 255))
current_number = 0
start_time = 0
incorrect_number = False
incorrect_pos = (0, 0)
finished_puzzle = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                current_number = 0
            elif event.key == pygame.K_1:
                current_number = 1
            elif event.key == pygame.K_2:
                current_number = 2
            elif event.key == pygame.K_3:
                current_number = 3
            elif event.key == pygame.K_4:
                current_number = 4
            elif event.key == pygame.K_5:
                current_number = 5
            elif event.key == pygame.K_6:
                current_number = 6
            elif event.key == pygame.K_7:
                current_number = 7
            elif event.key == pygame.K_8:
                current_number = 8
            elif event.key == pygame.K_9:
                current_number = 9
            elif event.key == pygame.K_SPACE:
                finished_puzzle = False
                
                grid = [[0 for _ in range(9)] for _ in range(9)]
                fill_grid(grid)
                solved_puzzle = copy.deepcopy(grid)
                grid, numbers_left = remove_numbers(grid)
            
                
    
    screen.fill((255, 255, 255))
    grid_surface.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()
    if current_time-start_time > 200 and incorrect_number:
        incorrect_number = False

    draw_grid(grid_surface, mouse_pos, incorrect_number, incorrect_pos)
    

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[1] or mouse_buttons[2] or mouse_buttons[0]:
        mouse_grid_pos = int(mouse_pos[0] / 60), int(mouse_pos[1] / 60)
        mouse_grid_pos = (mouse_grid_pos[0] * 60 - 120, mouse_grid_pos[1] * 60 - 120)
        mouse_grid_pos = (int(mouse_grid_pos[0] / 60), int(mouse_grid_pos[1] / 60))
        if 9 > mouse_grid_pos[0] >= 0 and 9 > mouse_grid_pos[1] >= 0:
            if current_number == solved_puzzle[mouse_grid_pos[1]][mouse_grid_pos[0]]:
                if grid[mouse_grid_pos[1]][mouse_grid_pos[0]] == 0:
                    grid[mouse_grid_pos[1]][mouse_grid_pos[0]] = current_number
                    numbers_left[current_number] += 1
            else:
                incorrect_number = True
                incorrect_pos = int(mouse_pos[0] / 60), int(mouse_pos[1] / 60)
                incorrect_pos = (incorrect_pos[0] * 60 - 120, incorrect_pos[1] * 60 - 120)
                start_time = pygame.time.get_ticks()
    
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num != 0:
                font = pygame.font.Font(None, 40)
                text = font.render(str(num), True, (0, 0, 0))
                text_rect = text.get_rect(center=(col * 60 + 30, row * 60 + 30))
                
                grid_surface.blit(text, text_rect)

    for i in range(10):
        if i != 0 and numbers_left[i] > 7:
            font = pygame.font.Font(None, 20)
            text = font.render(str(i), True, (200, 200, 200))  
        elif i == current_number:
            font = pygame.font.Font(None, 80)
            text = font.render(str(i), True, (0, 0, 0))
        else:
            font = pygame.font.Font(None, 40)
            text = font.render(str(i), True, (100, 100, 100))
        text_rect = text.get_rect(center=(i*40+240, 60))
    
        screen.blit(text, text_rect)
    if grid == solved_puzzle:
        font = pygame.font.Font(None, 50)
        text = font.render("You solved the puzzle!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(400, 700))
        pygame.draw.rect(screen, (255,255,255), text_rect)
        screen.blit(text, text_rect)
        finished_puzzle = True
    screen.blit(grid_surface, (130, 130))
                
    pygame.display.flip()


pygame.quit()
sys.exit()