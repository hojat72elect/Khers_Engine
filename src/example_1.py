import pygame

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((640, 640))

potato_image = pygame.image.load("potato.png").convert()
potato_image = pygame.transform.scale(potato_image, (potato_image.get_width() * 2, potato_image.get_height() * 2))

potato_image.set_colorkey((0, 0, 0))

running = True
x = 0
clock = pygame.time.Clock()
delta_time = 0.1

font = pygame.font.Font(None, size=30)
is_moving_right = False
is_moving_left = False
sound = pygame.mixer.Sound("clank.wav")
movement_speed = 120

while running:
    screen.fill((255, 255, 255))
    screen.blit(potato_image, (x, 30))

    hitbox = pygame.Rect(x, 30, potato_image.get_width(), potato_image.get_height())
    mouse_position = pygame.mouse.get_pos()

    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint(mouse_position)
    pygame.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target)

    if is_moving_right:
        x += movement_speed * delta_time
    elif is_moving_left:
        x -= movement_speed * delta_time

    text = font.render('Hello World!', True, (0, 0, 0))
    screen.blit(text, (300, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                is_moving_right = True
            if event.key == pygame.K_f:
                sound.play()
            if event.key == pygame.K_a:
                is_moving_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                is_moving_right = False
            if event.key == pygame.K_a:
                is_moving_left = False

    pygame.display.flip()
    delta_time = clock.tick(60) / 1_000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()
