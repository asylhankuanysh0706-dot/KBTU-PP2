import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock - Perfect Alignment")

# Загрузка
clock_img = pygame.image.load("images/clock.png").convert_alpha()
left_hand = pygame.image.load("images/left_hand.png").convert_alpha()
right_hand = pygame.image.load("images/right_hand.png").convert_alpha()

center = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
font = pygame.font.SysFont("Arial", 50, bold=True)

def blit_rotate_shoulder(surf, image, center_point, shoulder_offset, angle):
    """
    Рисует руку так, чтобы точка плеча была всегда в center_point.
    shoulder_offset: вектор от ЦЕНТРА картинки руки до ПЛЕЧА на этой картинке.
    """
    # 1. Поворачиваем саму картинку
    rotated_image = pygame.transform.rotate(image, angle)
    
    # 2. Поворачиваем вектор смещения плеча
    # Важно: в pygame.math.Vector2.rotate углы идут в обратную сторону, ставим минус
    rotated_offset = shoulder_offset.rotate(-angle)
    
    # 3. Находим новый центр повернутой картинки
    # Мы вычитаем повернутое смещение из центра часов
    rect = rotated_image.get_rect(center = center_point - rotated_offset)
    
    surf.blit(rotated_image, rect)

# --- НАСТРОЙКА (ВАЖНО) ---
# Нам нужно найти расстояние от геометрического центра картинки руки до её плеча.
# Если плечо находится внизу картинки, вектор будет смотреть вниз (положительный Y).
# Пример: если картинка высотой 200px, а плечо в самом низу, смещение будет (0, 100).
offset_l = pygame.math.Vector2(0, 80) # Подбери эти числа для левой руки
offset_r = pygame.math.Vector2(0, 80) # Подбери эти числа для правой руки

# Корректировка угла (если руки в файле смотрят не вверх)
base_offset = 0

clock_timer = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    now = datetime.datetime.now()
    
    # Углы
    sec_angle = (-now.second * 6) + base_offset
    min_angle = (-(now.minute + now.second/60.0) * 6) + base_offset

    screen.fill((255, 255, 255))
    
    # Циферблат
    screen.blit(clock_img, clock_img.get_rect(center=center))

    # Рисуем руки с фиксацией плеча в центре
    blit_rotate_shoulder(screen, right_hand, center, offset_r, min_angle)
    blit_rotate_shoulder(screen, left_hand, center, offset_l, sec_angle)

    # Цифровые часы
    time_str = now.strftime("%H:%M:%S")
    digital_text = font.render(time_str, True, (0, 0, 0))
    screen.blit(digital_text, (WIDTH//2 - digital_text.get_width()//2, 40))

    pygame.display.flip()
    clock_timer.tick(60)

pygame.quit()
