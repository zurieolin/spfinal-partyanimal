import pygame, random, os

pygame.init()

BASE_DIR = os.path.dirname(__file__)
def asset(name):
    return os.path.join(BASE_DIR, "assets", name)

try:
    pygame.mixer.init()
    pygame.mixer.music.load(asset("music.mp3"))
    pygame.mixer.music.play(-1)
except:
    pass

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Honey Comb")

bee = pygame.transform.scale(pygame.image.load(asset("bee.png")).convert_alpha(), (80, 80))
flower_size = 45
flower = pygame.transform.scale(pygame.image.load(asset("flower.png")).convert_alpha(), (flower_size, flower_size))
bg = pygame.transform.scale(pygame.image.load(asset("honeycomb_bg.png")).convert(), (WIDTH, HEIGHT))

x, y = WIDTH//2, HEIGHT//2
fx, fy = random.randint(0, WIDTH-flower_size), random.randint(0, HEIGHT-flower_size)
score, lives = 0, 3
speed = 5
timer = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 36)
big = pygame.font.SysFont(None, 72)
title_font = pygame.font.SysFont(None, 90)

clock = pygame.time.Clock()
running = True
game_over = False
game_started = False

while running:
    screen.blit(bg, (0,0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    if not game_started:
        screen.blit(title_font.render("Honey Comb", True, (0,0,0)), (WIDTH//2 - 200, HEIGHT//2 - 100))
        screen.blit(font.render("Press SPACE to Start", True, (0,0,0)), (WIDTH//2 - 150, HEIGHT//2))

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_started = True
            timer = pygame.time.get_ticks()

    elif not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= speed
        if keys[pygame.K_RIGHT]: x += speed
        if keys[pygame.K_UP]: y -= speed
        if keys[pygame.K_DOWN]: y += speed

        screen.blit(bee, (x,y))
        screen.blit(flower, (fx,fy))

        bee_rect = pygame.Rect(x,y,80,80)
        flower_rect = pygame.Rect(fx,fy,flower_size,flower_size)

        limit = max(1200, 3000 - score*80)

        if pygame.time.get_ticks() - timer > limit:
            lives -= 1
            fx, fy = random.randint(0, WIDTH-flower_size), random.randint(0, HEIGHT-flower_size)
            timer = pygame.time.get_ticks()

        if bee_rect.colliderect(flower_rect):
            score += 1
            fx, fy = random.randint(0, WIDTH-flower_size), random.randint(0, HEIGHT-flower_size)
            timer = pygame.time.get_ticks()

        if lives <= 0:
            game_over = True
            pygame.mixer.music.stop()

        screen.blit(font.render(f"Score: {score}", True, (0,0,0)), (10,10))
        screen.blit(font.render(f"Lives: {lives}", True, (200,0,0)), (10,50))

    else:
        screen.blit(big.render("GAME OVER", True, (0,0,0)), (250,200))
        screen.blit(font.render("Press R to Restart", True, (0,0,0)), (280,300))

        if pygame.key.get_pressed()[pygame.K_r]:
            score, lives = 0, 3
            game_over = False
            game_started = False
            timer = pygame.time.get_ticks()
            try:
                pygame.mixer.music.play(-1)
            except:
                pass

    pygame.display.update()
    clock.tick(60)

pygame.quit()