import pygame
from pygame import Font, Surface, Clock, Sound


class PotatoGame:
    screen: Surface
    potato_image: Surface
    running: bool = True
    x: float = 0
    y: float = 0
    clock: Clock
    delta_time: float = 0.1
    font: Font
    is_moving_right: bool = False
    is_moving_left: bool = False
    is_moving_up: bool = False
    is_moving_down: bool = False
    sound: Sound
    movement_speed: float = 120

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        self.clock = pygame.time.Clock()
        self.load()

    def load(self):
        """Load all the required assets"""
        self.potato_image = pygame.image.load("potato.png").convert()
        self.font = pygame.font.Font(None, size=30)
        self.sound = pygame.mixer.Sound("clank.wav")

    def run(self):
        self.potato_image = pygame.transform.scale(self.potato_image, (self.potato_image.get_width() * 2, self.potato_image.get_height() * 2))
        self.potato_image.set_colorkey((0, 0, 0))

        while self.running:
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.potato_image, (self.x, self.y))
            hitbox = pygame.Rect(self.x, 30, self.potato_image.get_width(), self.potato_image.get_height())
            mouse_position = pygame.mouse.get_pos()

            target = pygame.Rect(300, 0, 160, 280)
            collision = hitbox.colliderect(target)
            m_collision = target.collidepoint(mouse_position)
            pygame.draw.rect(self.screen, (255 * collision, 255 * m_collision, 0), target)

            if self.is_moving_right:
                self.x += self.movement_speed * self.delta_time
            if self.is_moving_left:
                self.x -= self.movement_speed * self.delta_time
            if self.is_moving_up:
                self.y -= self.movement_speed * self.delta_time
            if self.is_moving_down:
                self.y += self.movement_speed * self.delta_time

            text = self.font.render('Hello World!', True, (0, 0, 0))
            self.screen.blit(text, (300, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.is_moving_right = True
                    if event.key == pygame.K_f:
                        self.sound.play()
                    if event.key == pygame.K_a:
                        self.is_moving_left = True
                    if event.key == pygame.K_w:
                        self.is_moving_up = True
                    if event.key == pygame.K_s:
                        self.is_moving_down = True
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.is_moving_right = False
                    if event.key == pygame.K_a:
                        self.is_moving_left = False
                    if event.key == pygame.K_w:
                        self.is_moving_up = False
                    if event.key == pygame.K_s:
                        self.is_moving_down = False

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1_000
            self.delta_time = max(0.001, min(0.1, self.delta_time))

        pygame.quit()
