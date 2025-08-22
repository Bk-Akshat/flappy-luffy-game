import pygame, sys, random, os

pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Luffy 🏴‍☠️")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 250)

# Load Images
luffy_img = pygame.image.load("luffy.png")
luffy_img = pygame.transform.scale(luffy_img, (60, 60))

coin_img = pygame.image.load("coin.png") if os.path.exists("coin.png") else None
if coin_img:
    coin_img = pygame.transform.scale(coin_img, (30, 30))

# Load Sounds
jump_sound = pygame.mixer.Sound("jump.mp3")
coin_sound = pygame.mixer.Sound("coin.wav")
crash_sound = pygame.mixer.Sound("crash.mp3")

# Background Music
if os.path.exists("bg_music.mp3"):
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.play(-1)  # Loop forever

# Fonts
font = pygame.font.SysFont("Arial", 30)

# Game Variables
gravity = 0.5
luffy_y = HEIGHT // 2
luffy_x = 80
luffy_movement = 0

pipes = []
COIN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(COIN_EVENT, 4000)

# Score
score = 0
high_score = 0
coins = []
coin_score = 0

# Functions
def draw_text(text, size, x, y, color=BLACK):
    font = pygame.font.SysFont("Arial", size, True)
    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)

def create_pipe():
    height = random.randint(150, 400)
    pipe_top = pygame.Rect(WIDTH, height - 500, 70, 500)
    pipe_bottom = pygame.Rect(WIDTH, height + 150, 70, 500)
    return pipe_top, pipe_bottom

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 4
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), pipe)

def check_collision(luffy_rect, pipes, coins):
    global running
    for pipe in pipes:
        if luffy_rect.colliderect(pipe):
            crash_sound.play()
            return False
    if luffy_rect.top <= -50 or luffy_rect.bottom >= HEIGHT:
        crash_sound.play()
        return False
    for coin in coins[:]:
        if luffy_rect.colliderect(coin):
            coins.remove(coin)
            global coin_score
            coin_score += 1
            coin_sound.play()
    return True

def show_score():
    draw_text(f"Score: {score}", 25, WIDTH//2, 30)
    draw_text(f"Coins: {coin_score}", 25, WIDTH//2, 60)

def update_high_score(score, high_score):
    return max(score, high_score)

def create_coin():
    y = random.randint(100, HEIGHT-100)
    return pygame.Rect(WIDTH, y, 30, 30)

# Landing Page
def main_menu():
    while True:
        screen.fill(SKY)
        draw_text("Flappy Luffy", 50, WIDTH//2, HEIGHT//2 - 100, BLACK)
        draw_text("Press SPACE to Start", 30, WIDTH//2, HEIGHT//2, BLACK)
        draw_text("Press ESC to Quit", 25, WIDTH//2, HEIGHT//2 + 50, BLACK)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Main Game Loop
def game_loop():
    global luffy_y, luffy_movement, pipes, score, high_score, coins, coin_score
    luffy_y = HEIGHT // 2
    luffy_movement = 0
    pipes = []
    coins = []
    score = 0
    coin_score = 0
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1500)

    running = True
    while running:
        screen.fill(SKY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    luffy_movement = -8
                    jump_sound.play()
            if event.type == SPAWNPIPE:
                pipes.extend(create_pipe())
            if event.type == COIN_EVENT:
                coins.append(create_coin())

        luffy_movement += gravity
        luffy_y += luffy_movement
        luffy_rect = luffy_img.get_rect(center=(luffy_x, luffy_y))
        screen.blit(luffy_img, luffy_rect)

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Coins
        for coin in coins:
            coin.x -= 4
            if coin_img:
                screen.blit(coin_img, coin)
            else:
                pygame.draw.circle(screen, (255, 215, 0), coin.center, 15)

        # Collision
        if not check_collision(luffy_rect, pipes, coins):
            high_score = update_high_score(score + coin_score, high_score)
            return

        # Scoring
        for pipe in pipes:
            if pipe.centerx == luffy_x:
                score += 0.5

        show_score()

        pygame.display.update()
        clock.tick(FPS)

# Scoreboard Page
def scoreboard():
    while True:
        screen.fill(SKY)
        draw_text("Game Over", 50, WIDTH//2, HEIGHT//2 - 100, BLACK)
        draw_text(f"Score: {score}", 35, WIDTH//2, HEIGHT//2 - 30, BLACK)
        draw_text(f"Coins: {coin_score}", 35, WIDTH//2, HEIGHT//2 + 10, BLACK)
        draw_text(f"High Score: {high_score}", 30, WIDTH//2, HEIGHT//2 + 60, BLACK)
        draw_text("Press SPACE to Play Again", 25, WIDTH//2, HEIGHT//2 + 120, BLACK)
        draw_text("Press ESC to Quit", 25, WIDTH//2, HEIGHT//2 + 160, BLACK)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Run Game
while True:
    main_menu()
    game_loop()
    scoreboard()
