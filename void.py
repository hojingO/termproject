import pygame
import sys
import random
# 게임 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# 색깔 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0, 0 ,255)
YELLOW = (240, 170, 0)
PURPLE = (255, 0, 255)

# 플레이어 클래스 정의
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load('c:\hff.png').convert_alpha()  # 이미지 로드
        
        # self.image = pygame.transform.scale(self.image, (60, 60))
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_cooldown = 1000  # 쿨타임을 500밀리초로 설정

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # 화면 밖으로 나가지 않도록 제한
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_cooldown:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            return bullet
        return None
# 총알 클래스 정의
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20)) 
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# 적 클래스 정의
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speed = random.randint(4, 8)

class NewEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  
        self.image.fill(GRAY) 
        self.rect = self.image.get_rect() 
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  
        self.rect.y = random.randint(-100, -50)  # y축 위치 무작위 설정
        self.speed = random.randint(5, 11)  # 이동 속도 무작위 설정

    def update(self):
        self.rect.y += self.speed  # 아래쪽으로 이동
        if self.rect.top > SCREEN_HEIGHT:  # 적이 화면을 벗어나면
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # 다시 무작위 위치 설정
            self.rect.y = random.randint(-100, -50)
            self.speed = random.randint(5, 11)  # 다시 무작위 속도 설정

# 게임 오버 화면 출력 함수
def game_over_screen(screen):
    font = pygame.font.SysFont(None, 36)
    text = font.render("PRESS R KEY, RESTART", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

# 3초 카운트 다운 함수
def countdown(screen):
    font = pygame.font.SysFont(None, 100)
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        text = font.render(str(i), True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)

# 메인 함수
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("탄막 피하기 게임")
    clock = pygame.time.Clock()

    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    for _ in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    for _ in range(8): 
        new_enemy = NewEnemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)
    
    countdown(screen)
    score = 0
    start_ticks = pygame.time.get_ticks()
    font = pygame.font.SysFont(None, 36)

    # 게임 루프
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullet = player.shoot()
                    if bullet:
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            all_sprites.update()

            # 총알과 적의 충돌 체크
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            score = int(seconds * 10)
        

            # 플레이어와 적의 충돌 체크
            if pygame.sprite.spritecollide(player, enemies, False):
                game_over = True

        screen.fill(WHITE)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        
        if game_over:
            game_over_screen(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()