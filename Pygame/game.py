import pygame
import sys
import random

pygame.init()

WIDTH = 750
HEIGHT = 750
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
img = pygame.image.load('Pygame\player.png')
player_size = 50
player_speed = .17  # move distance
player_pos = [WIDTH/2, HEIGHT - 2*player_size]
#             left/right    up/down

enemy_size = 50
enemy_pos = [100, 0]
enemy_speed = .07
MAX_NO_OF_ENEMIES = 12

game_over = False
score = 0
myFont = pygame.font.SysFont("monospace", 35)
enemy_locations = [[random.randint(0, WIDTH), random.randint(0, int(HEIGHT/3)), enemy_speed]
                   for i in range(random.randint(3, 6))]

# key_left determines if a key is being held down its direction "left" or "right"
key_left = False
key_right = False


def check_key_presses():
    global key_left, player_pos, player_speed, key_up_down, key_right
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                key_left = True

            if event.key == pygame.K_RIGHT:
                key_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                key_left = False
            if event.key == pygame.K_RIGHT:
                key_right = False

    if key_left and player_pos[0] >= 0:
        player_pos[0] -= player_speed
    if key_right and player_pos[0] + player_size <= WIDTH:
        player_pos[0] += player_speed


def check_collision(enemies, player):
    global game_over
    for enemy in enemies:
        e_x = enemy[0]
        e_y = enemy[1]
        p_x = player[0]
        p_y = player[1]

        if (p_x <= e_x <= (p_x + player_size)) or (e_x <= p_x <= (e_x + enemy_size)):
            if (p_y <= e_y <= p_y + (player_size)) or (e_y <= p_y <= e_y + enemy_size):
                game_over = True
                return True


def update_enemy_location():
    global enemy_locations, enemy_speed, player_speed, player_size, score
    for i in range(len(enemy_locations)):
        # if enemy's height is within box boundaries update position else reset to beginning
        if 0 <= enemy_locations[i][1] <= HEIGHT:
            enemy_locations[i][1] += enemy_locations[i][2]
        else:
            score += 1
            enemy_locations[i][1] = 0
            enemy_locations[i][0] = random.randint(0, WIDTH)
            enemy_locations[i][2] = random.randint(1, 2)*enemy_speed
            if score % 5 == 0 and len(enemy_locations) <= MAX_NO_OF_ENEMIES:
                enemy_locations.append(
                    [random.randint(0, WIDTH), 0, enemy_speed])
            if score % 20 == 0:
                enemy_speed += .01
                player_speed += .01
        pygame.draw.rect(
            screen, BLACK, (enemy_locations[i][0], enemy_locations[i][1], player_size, player_size))


def draw_and_update():
    global player_pos, player_size
    pygame.draw.rect(
        screen, BLACK, (player_pos[0], player_pos[1], player_size, player_size))
    label = myFont.render(str(score), 1, BLACK)
    screen.blit(img, (player_pos[0], player_pos[1]))
    if score < 10:
        screen.blit(label, (WIDTH/2, 15))
    elif score < 100:
        screen.blit(label, (WIDTH/2 - 10, 15))
    elif score < 9999:
        screen.blit(label, (WIDTH/2 - 20, 15))
    pygame.display.update()


while not game_over:
    check_key_presses()
    screen.fill(WHITE)
    check_collision(enemy_locations, player_pos)
    update_enemy_location()
    draw_and_update()
