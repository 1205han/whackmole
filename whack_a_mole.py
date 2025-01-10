import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 设置字体
font = pygame.font.Font(None, 36)

# 加载地鼠图片
try:
    mole_image = pygame.image.load('mole.png')
    mole_image = pygame.transform.scale(mole_image, (80, 80))
except FileNotFoundError:
    print("地鼠图片未找到，使用红色矩形代替")
    mole_image = pygame.Surface((80, 80))
    mole_image.fill(RED)

# 设置地鼠洞的位置
holes = [
    (100, 200),
    (300, 200),
    (500, 200),
    (700, 200),
    (100, 400),
    (300, 400),
    (500, 400),
    (700, 400)
]

# 游戏变量
score = 0
time_left = 30
clock = pygame.time.Clock()
mole_position = None
mole_visible = False
mole_timer = 0

def draw_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def draw_mole():
    if mole_visible:
        screen.blit(mole_image, mole_position)

def spawn_mole():
    global mole_position, mole_visible, mole_timer
    mole_position = random.choice(holes)
    mole_visible = True
    mole_timer = pygame.time.get_ticks()
    print("Mole spawned at:", mole_position)  # 调试信息

def hide_mole():
    global mole_visible
    mole_visible = False
    print("Mole hidden")  # 调试信息

def check_click(pos):
    global score
    if mole_visible and mole_position[0] <= pos[0] <= mole_position[0] + 80 and mole_position[1] <= pos[1] <= mole_position[1] + 80:
        score += 1
        hide_mole()

# 游戏主循环
running = True
spawn_mole()
start_ticks = pygame.time.get_ticks()

print("Game started")  # 调试信息

while running:
    screen.fill(WHITE)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_click(event.pos)

    # 更新地鼠状态
    if mole_visible and pygame.time.get_ticks() - mole_timer > 1000:
        hide_mole()
    if not mole_visible and pygame.time.get_ticks() - mole_timer > 500:
        spawn_mole()

    # 绘制地鼠洞
    for hole in holes:
        pygame.draw.circle(screen, BLACK, (hole[0] + 40, hole[1] + 40), 40)

    # 绘制地鼠
    draw_mole()

    # 显示得分和时间
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Time Left: {time_left - (pygame.time.get_ticks() - start_ticks) // 1000}", 10, 50)

    # 检查游戏是否结束
    if (pygame.time.get_ticks() - start_ticks) // 1000 >= time_left:
        draw_text(f"Game Over! Final Score: {score}", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # 更新屏幕
    pygame.display.flip()
    clock.tick(30)

# 退出游戏
pygame.quit()
sys.exit()