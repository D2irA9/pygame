import pygame
img_past = '/data/data/com.myapp.myapp/files/app'
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((618, 264))
pygame.display.set_caption('Game')
pygame.display.set_icon(pygame.image.load(img_past+'img_png/icon_cat.png'))

fon = pygame.image.load('img_png/fon.jpg').convert()
walk_right = [
    pygame.image.load(img_past+'img_png/user_right/user_right4.png'),
    pygame.image.load(img_past+'img_png/user_right/user_right3.png'),
    pygame.image.load(img_past+'img_png/user_right/user_right2.png'),
    pygame.image.load(img_past+'img_png/user_right/user_right1.png'),
]
walk_left = [
    pygame.image.load(img_past+'img_png/user_left/user_left1.png'),
    pygame.image.load(img_past+'img_png/user_left/user_left2.png'),
    pygame.image.load(img_past+'img_png/user_left/user_left3.png'),
    pygame.image.load(img_past+'img_png/user_left/user_left4.png'),
]
player_anim_cont = 0
fon_x = 0

player_speed = 5
player_x = 50
player_y = 175

is_jump = False
jump_count = 8

zombie = pygame.image.load(img_past+'img_png/zombie.png')
zombie_list_in_game = []

fon_music = pygame.mixer.Sound(img_past+'music/fon_music.mp3')
# fon_music.play()

zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer, 3500)

label = pygame.font.Font(img_past+'fonts/Roboto-Black.ttf', 40)
lose_label = label.render('Ты проиграл!', False, (0, 0, 0))
restart_label = label.render('Заново', False, (25, 255, 0))
restart_label_rect = restart_label.get_rect(topleft=(200, 185))

potrom_left = 5
potrom = pygame.image.load(img_past+'img_png/potron.png')
potromns = []
gameplay = True

running = True
while running:

    screen.blit(fon, (fon_x, 0))
    screen.blit(fon, (fon_x + 618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if zombie_list_in_game:
            for i, el in enumerate(zombie_list_in_game):
                screen.blit(zombie, el)
                el.x -= 5

                if el.x < -10:
                    zombie_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_cont], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_cont], (player_x, player_y))

        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 500:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_w]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_cont == 3:
            player_anim_cont = 0
        else:
            player_anim_cont += 1

        fon_x -= 2
        if fon_x == -618:
            fon_x = 0

        if potromns:
            for i, el in enumerate(potromns):
                screen.blit(potrom, (el.x, el.y))
                el.x += 4
                if el.x > 630:
                    potromns.pop(i)
                if zombie_list_in_game:
                    for index, zombie_el in enumerate(zombie_list_in_game):
                        if el.colliderect(zombie_el):
                            zombie_list_in_game.pop(index)
                            potromns.pop(i)
    else:
        screen.fill((255, 77, 77, 0.43))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 50
            zombie_list_in_game.clear()
            potromns.clear()
            potrom_left = 5

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == zombie_timer:
            zombie_list_in_game.append(zombie.get_rect(topleft=(618, 175)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and potrom_left > 0:
            potromns.append(potrom.get_rect(topleft=(player_x + 30, player_y + 30)))
            potrom_left -= 1

    clock.tick(15)
