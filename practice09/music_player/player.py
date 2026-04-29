import pygame
import os

# Инициализация
pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH, HEIGHT = 600, 250
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Professional Music Player")

# Цвета
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (40, 40, 40)
GREEN = (100, 200, 100)
BLUE = (100, 150, 255)

# Шрифты
font_big = pygame.font.SysFont("Arial", 32, bold=True)
font_small = pygame.font.SysFont("Arial", 22)

# Плейлист
playlist = [
    {"file": "music/alexgrohl-sweet-life-luxury-chill-438146.mp3", "title": "Sweet Life", "artist": "AlexGrohl"},
    {"file": "music/chill_background-the-weekend-117427.mp3", "title": "The Weekend", "artist": "Chill Background"},
    {"file": "music/ummbrella-deep-abstract-ambient_snowcap-401656.mp3", "title": "Deep Abstract Ambient", "artist": "Snowcap"}
]

current_track_idx = 0
is_playing = False
song_length = 0  # Длительность в секундах
current_pos = 0  # Текущая позиция в секундах

# Событие окончания трека для автоперехода
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

def load_track(track_index):
    global is_playing, song_length, current_pos
    track = playlist[track_index]
    if os.path.exists(track["file"]):
        pygame.mixer.music.load(track["file"])
        # Получаем длительность трека
        sound = pygame.mixer.Sound(track["file"])
        song_length = sound.get_length()
        
        pygame.mixer.music.play()
        is_playing = True
        current_pos = 0
    else:
        print(f"Файл не найден: {track['file']}")

def toggle_play():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    is_playing = not is_playing

def seek_track(mouse_x):
    global current_pos
    # Вычисляем позицию времени исходя из клика по полоске (от 50 до 550 пикселей)
    if 50 <= mouse_x <= 550:
        fraction = (mouse_x - 50) / 500
        current_pos = fraction * song_length
        pygame.mixer.music.play(start=current_pos)
        if not is_playing:
            pygame.mixer.music.pause()

# Загружаем первый трек сразу
load_track(current_track_idx)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(DARK_GRAY)
    
    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == SONG_END:
            current_track_idx = (current_track_idx + 1) % len(playlist)
            load_track(current_track_idx)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_play()
            if event.key == pygame.K_RIGHT:
                current_track_idx = (current_track_idx + 1) % len(playlist)
                load_track(current_track_idx)
            if event.key == pygame.K_LEFT:
                current_track_idx = (current_track_idx - 1) % len(playlist)
                load_track(current_track_idx)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Левый клик
                # Если кликнули в области прогресс-бара
                if 160 <= event.pos[1] <= 180:
                    seek_track(event.pos[0])

    # 2. Обновление времени (позиции)
    if is_playing:
        # Прибавляем время кадра к текущей позиции
        current_pos += clock.get_time() / 1000

    # 3. Отрисовка интерфейса
    track = playlist[current_track_idx]
    
    # Название и автор
    title_surf = font_big.render(track["title"], True, WHITE)
    artist_surf = font_small.render(track["artist"], True, GRAY)
    screen.blit(title_surf, (50, 40))
    screen.blit(artist_surf, (50, 85))

    # Статус (Играет/Пауза)
    status_text = "PLAYING" if is_playing else "PAUSED"
    status_surf = font_small.render(status_text, True, GREEN if is_playing else BLUE)
    screen.blit(status_surf, (50, 125))

    # Полоса прогресса (Background)
    pygame.draw.rect(screen, (60, 60, 60), (50, 165, 500, 10))
    # Полоса прогресса (Current)
    if song_length > 0:
        progress_width = (current_pos / song_length) * 500
        pygame.draw.rect(screen, GREEN, (50, 165, min(progress_width, 500), 10))

    # Таймер
    minutes = int(current_pos // 60)
    seconds = int(current_pos % 60)
    total_min = int(song_length // 60)
    total_sec = int(song_length % 60)
    time_surf = font_small.render(f"{minutes:02}:{seconds:02} / {total_min:02}:{total_sec:02}", True, GRAY)
    screen.blit(time_surf, (400, 185))

    # Подсказка
    hint_surf = font_small.render("Space: Play/Pause | Arrows: Prev/Next | Click bar to Seek", True, (100, 100, 100))
    screen.blit(hint_surf, (50, 215))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
