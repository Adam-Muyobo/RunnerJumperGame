import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"SCORE: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            screen.blit(snail_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]  # Remove off-screen obstacles
    return obstacle_list


def check_collisions(player, obstacles):
    for obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return False
    return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()

# obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

obstacle_rect_list = []

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(50, 300))
player_gravity = 0

# INTRO SCREEN

# Intro title
title_surf = test_font.render("RUNNER GAME", False, (111, 196, 169))
title_rect = title_surf.get_rect(center=(400, 80))

# Intro Score
score = 0
high_score = 0
# Intro screen player
player_stand_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(400, 200))

# Instructions
inst_surf = test_font.render("Press space to start!", False, (111, 196, 169))
inst_rect = inst_surf.get_rect(center=(400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                player_gravity = -20

            if event.type == pygame.KEYDOWN and player_rect.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                obstacle_rect_list.clear()  # Reset obstacles
                player_rect.midbottom = (50, 300)
                player_gravity = 0
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        if score >= high_score:
            high_score = score

        # Player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # COLLISIONS
        game_active = check_collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_rect)

        # current score
        intro_score_surf = test_font.render(f"Score {score}", False, (100, 10, 10))
        intro_score_rect = intro_score_surf.get_rect(center=(400, 330))

        # high score
        high_score_surf = test_font.render(f"High Score: {high_score}", False, (111, 196, 169))
        high_score_rect = high_score_surf.get_rect(center=(130, 80))
        if score == 0:
            screen.blit(inst_surf, inst_rect)
        else:
            screen.blit(intro_score_surf, intro_score_rect)
            screen.blit(high_score_surf, high_score_rect)
        screen.blit(player_stand_surf, player_stand_rect)

    pygame.display.update()
    clock.tick(60)
