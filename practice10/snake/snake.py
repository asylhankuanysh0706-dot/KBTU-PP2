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
font_big = pygame.font.SysFont("Verdana", 24, bold=True)

# Цвета
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
GREEN = (46, 204, 113)
DARK_GREEN = (39, 174, 96)
RED = (231, 76, 60)

# -----------------------------
# ПЕРЕМЕННЫЕ ИГРЫ
# -----------------------------
snake = [(3, 2), (2, 2), (1, 2)]
direction = (1, 0)
next_direction = (1, 0)
score = 0
level = 1
speed = 5
walls = set()
food = None

# -----------------------------
# ФУНКЦИИ
# -----------------------------

def load_level(level_number):
    """Загрузка стен из текстового файла"""
    global walls
    walls.clear() # Очищаем старые стены
    filename = f"level{level_number}.txt"
    try:
        with open(filename, "r") as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line.strip()):
                    if char == "#":
                        walls.add((x, y))
    except FileNotFoundError:
        # Если уровни закончились
        show_message("VICTORY! YOU FINISHED ALL LEVELS", GREEN)
        pygame.quit()
        sys.exit()

def generate_food():
    """Генерация еды без попадания в змейку или стену"""
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in snake and pos not in walls:
            return pos

def show_message(text, color):
    """Функция для вывода сообщений по центру экрана"""
    screen.fill(WHITE)
    msg = font_big.render(text, True, color)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.update()
    pygame.time.delay(2000) # Пауза на 2 секунды

def next_level():
    """Переход на новый уровень с уведомлением"""
    global level, speed, food, snake, direction, next_direction
    
    show_message(f"NEXT LEVEL: {level + 1}", BLACK)
    
    level += 1
    speed += 2 # Увеличиваем скорость
    load_level(level)
    
    # Спавним змейку в центре (безопасная зона)
    safe_x, safe_y = GRID_W // 2, GRID_H // 2
    snake = [(safe_x, safe_y), (safe_x-1, safe_y), (safe_x-2, safe_y)]
    direction = (1, 0)
    next_direction = (1, 0)
    food = generate_food()

def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL - 1, CELL - 1))

def draw_game():
    screen.fill(WHITE)
    # Рисуем шахматный фон
    for y in range(GRID_H):
        for x in range(GRID_W):
            if (x + y) % 2 != 0:
                pygame.draw.rect(screen, GRAY, (x * CELL, y * CELL, CELL, CELL))
    
    for wall in walls: draw_cell(wall, BLACK) # Стены
    for i, part in enumerate(snake): # Змейка
        draw_cell(part, GREEN if i == 0 else DARK_GREEN)
    draw_cell(food, RED) # Еда
    
    # Текст статистики
    score_txt = font.render(f"Score: {score}", True, BLACK)
    level_txt = font.render(f"Lvl: {level}", True, BLACK)
    screen.blit(score_txt, (10, 10))
    screen.blit(level_txt, (WIDTH - 80, 10))
    pygame.display.update()

# --- СТАРТ ИГРЫ ---
load_level(level)
food = generate_food()

# --- ОСНОВНОЙ ЦИКЛ ---
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

    # Проверки коллизий
    if (new_head in walls or 
        new_head in snake or 
        not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H)):
        show_message("GAME OVER", RED)
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # Проверка еды
    if new_head == food:
        score += 1
        if score % 3 == 0: # Каждые 3 очка — новый уровень
            next_level()
        else:
            food = generate_food()
    else:
        snake.pop()

    draw_game()
    clock.tick(speed)
