import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# -----------------------------
# НАСТРОЙКИ ЭКРАНА И ГРИДА
# -----------------------------
CELL = 20
GRID_W = 15
GRID_H = 20
WIDTH = CELL * GRID_W  # 300
HEIGHT = CELL * GRID_H # 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake KBTU Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 18)

# Цвета
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)

# -----------------------------
# ПЕРЕМЕННЫЕ ИГРЫ
# -----------------------------
snake = [(3, 2), (2, 2), (1, 2)]
direction = (1, 0)
next_direction = (1, 0)
score = 0
level = 1
speed = 5 # Начальная скорость
walls = set()
food = None

# -----------------------------
# ФУНКЦИИ
# -----------------------------

def load_level(level_number):
    """Загрузка стен из текстового файла"""
    global walls
    walls = set()
    filename = f"level{level_number}.txt"
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for y, line in enumerate(lines):
                for x, char in enumerate(line.strip()):
                    if char == "#":
                        walls.add((x, y))
    except FileNotFoundError:
        # Если уровни кончились, просто оставляем пустую карту или выходим
        print(f"Level {level_number} file not found. Victory!")
        pygame.quit()
        sys.exit()

def generate_food():
    """Генерация еды так, чтобы она не попала на змейку или стену"""
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in snake and pos not in walls:
            return pos

def draw_cell(pos, color):
    """Отрисовка одного квадратика (клетки)"""
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

def draw_background():
    """Шахматный фон"""
    for y in range(GRID_H):
        for x in range(GRID_W):
            color = WHITE if (x + y) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL))

def draw_game():
    """Отрисовка всех объектов на экране"""
    draw_background()
    for wall in walls: draw_cell(wall, BLACK) # Стены
    for i, part in enumerate(snake): # Змейка
        draw_cell(part, GREEN if i == 0 else DARK_GREEN)
    draw_cell(food, RED) # Еда
    
    # Счетчики
    s_text = font.render(f"Score: {score}", True, BLACK)
    l_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(s_text, (10, 10))
    screen.blit(l_text, (WIDTH - 100, 10))
    pygame.display.update()

def game_over():
    """Экран проигрыша"""
    screen.fill(WHITE)
    t1 = font.render("GAME OVER", True, RED)
    t2 = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(t1, (WIDTH//2 - 50, HEIGHT//2 - 20))
    screen.blit(t2, (WIDTH//2 - 50, HEIGHT//2 + 10))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

def next_level():
    """Переход на новый уровень"""
    global level, speed, food, snake, direction, next_direction
    level += 1
    speed += 2 # Увеличиваем сложность
    load_level(level)
    
    # Сбрасываем позицию змейки в безопасное место, чтобы не заспавниться в стене
    snake = [(3, 2), (2, 2), (1, 2)]
    direction = (1, 0)
    next_direction = (1, 0)
    food = generate_food()

# Подготовка первого уровня
load_level(level)
food = generate_food()

# -----------------------------
# ИГРОВОЙ ЦИКЛ
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                next_direction = (1, 0)

    direction = next_direction
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # 1. Проверка столкновения со стенами
    if new_head in walls: game_over()

    # 2. Проверка выхода за границы экрана
    if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
        game_over()

    # 3. Проверка столкновения с самим собой
    if new_head in snake: game_over()

    snake.insert(0, new_head)

    # 4. Проверка поедания еды
    if new_head == food:
        score += 1
        if score % 3 == 0: # Каждые 3 очка — новый уровень
            next_level()
        else:
            food = generate_food()
    else:
        snake.pop() # Убираем хвост, если ничего не съели

    draw_game()
    clock.tick(speed)
