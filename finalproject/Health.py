import pygame


class HealthBar:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.health = 3
        self.heart_image = pygame.image.load('Graphics/Health/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (75, 75))

    def decrease_health(self):
            self.health -= 1
            print("hp is",self.health)

    def is_dead(self):
        return self.health <= 0

    def draw(self):
        for i in range(self.health):
            self.screen.blit(self.heart_image, (self.x + i * self.heart_image.get_width(), self.y))