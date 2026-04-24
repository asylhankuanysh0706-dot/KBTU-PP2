import pygame
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KBTU Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 16)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 215, 0)
GRAY = (220, 220, 220)

# Основной холст (где сохраняется рисунок)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Настройки инструментов
tool = "brush"
color = BLACK
brush_size = 5
drawing = False
start_pos = None

# Палитра цветов
colors = [BLACK, RED, GREEN, BLUE, YELLOW]
color_rects = []
for i, c in enumerate(colors):
    rect = pygame.Rect(10 + i * 45, 10, 35, 35)
    color_rects.append((rect, c))

def draw_ui():
    """Отрисовка интерфейса поверх холста"""
    screen.blit(canvas, (0, 0)) # Рисуем холст
    
    # Верхняя панель управления
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 55))
    pygame.draw.line(screen, BLACK, (0, 55), (WIDTH, 55), 2)
    
    # Рисуем квадратики палитры
    for rect, c in color_rects:
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 2) # Обводка
        if c == color: # Подсветка выбранного цвета
            pygame.draw.rect(screen, WHITE, rect, 3)

    # Инструкции
    msg = f"Tool: {tool.upper()} | B-Brush, R-Rect, C-Circle, E-Eraser"
    text = font.render(msg, True, BLACK)
    screen.blit(text, (300, 18))

# --- ОСНОВНОЙ ЦИКЛ ---
while True:
    curr_mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Горячие клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b: tool = "brush"
            if event.key == pygame.K_r: tool = "rect"
            if event.key == pygame.K_c: tool = "circle"
            if event.key == pygame.K_e: tool = "eraser"

        # Нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1. Проверка выбора цвета
            for rect, c in color_rects:
                if rect.collidepoint(event.pos):
                    color = c
            
            # 2. Начало рисования (если кликнули ниже панели)
            if event.pos[1] > 55:
                drawing = True
                start_pos = event.pos

        # Отпускание мыши
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                # Фиксируем фигуры на основном холсте (canvas)
                if tool == "rect":
                    r = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), 
                                    abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(canvas, color, r, 2)
                elif tool == "circle":
                    radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, color, start_pos, radius, 2)
                
                drawing = False

        # Процесс рисования для кисти и ластика (в реальном времени на canvas)
        if drawing and (tool == "brush" or tool == "eraser"):
            current_color = color if tool == "brush" else WHITE
            size = brush_size if tool == "brush" else 20
            pygame.draw.circle(canvas, current_color, curr_mouse_pos, size)

    # --- ОТРИСОВКА ---
    draw_ui()

    # ПРЕДПРОСМОТР (рисуем временную фигуру на screen, пока тянем мышь)
    if drawing:
        if tool == "rect":
            r = pygame.Rect(min(start_pos[0], curr_mouse_pos[0]), min(start_pos[1], curr_mouse_pos[1]), 
                            abs(curr_mouse_pos[0] - start_pos[0]), abs(curr_mouse_pos[1] - start_pos[1]))
            pygame.draw.rect(screen, color, r, 2)
        elif tool == "circle":
            radius = int(((curr_mouse_pos[0]-start_pos[0])**2 + (curr_mouse_pos[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, color, start_pos, radius, 2)

    pygame.display.update()
    clock.tick(60)
