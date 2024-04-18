import pygame
from attack import Attack, AirAttack, WaterAttack, FireAttack, EarthAttack

class Defend:
    def __init__(self, screen, x, y, image_paths, direction, size=(200, 250)):
        self.screen = screen
        self.x = x
        self.y = y
        self.images = [pygame.transform.scale(pygame.image.load(image_path), size) for image_path in image_paths]
        self.current_image = 0  # This will track the current image of the animation

        self.direction = direction

        self.animation_speed = 10  # Determines how fast the animation plays
        self.animation_counter = 0  # Counts up to change the sprite based on animation_speed


        self.hits_left = 2

        if self.direction == ("left"):
            self.images = [pygame.transform.flip(image, True, False) for image in self.images]
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect(topleft=(x, y))


    def update(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)  # Cycle through images
            self.image = self.images[self.current_image]

    # def check_block(self, attack):
    #     return isinstance(attack, Attack) and attack.type != self.type

    def draw(self):
        # Draw the defense sprite
        self.screen.blit(self.image, self.rect)
        # Create a font object
        font = pygame.font.Font(None, 62)  # You can choose the font and size
        text = font.render(str(self.hits_left), True, (255, 255, 255))  # White color
        text_rect = text.get_rect()
        text_rect.center = (self.x + 100, self.y - 50)
        self.screen.blit(text, text_rect)


    #this is the hierachy of the elements
    def check_block(self, attack):
        return True

    def hit(self, attack):
        if self.check_block(self, attack):
            self.hits_left -= 1
        else:
            self.hits_left -= 2


class AirDefend(Defend):
    def __init__(self, screen, x, y, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/air/Airshield1.png','Graphics/AttackSprites/air/Airshield2.png','Graphics/AttackSprites/air/Airshield3.png'], direction)

    def check_block(self, attack):
        if isinstance(attack, EarthAttack):
            print("Air defend can't block earth attack!")
            return False
        return super().check_block(attack)

class WaterDefend(Defend):
    def __init__(self, screen, x, y, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/water/waterfall1.png','Graphics/AttackSprites/water/waterfall2.png','Graphics/AttackSprites/water/waterfall3.png','Graphics/AttackSprites/water/waterfall4.png','Graphics/AttackSprites/water/waterfall5.png'], direction)

    def check_block(self, attack):
        if isinstance(attack, AirAttack):
            print("Water defend can't block Air attack!")
            return False
        return super().check_block(attack)


class FireDefend(Defend):
    def __init__(self, screen, x, y, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/fire/Fire7.png', 'Graphics/AttackSprites/fire/Fire8.png', 'Graphics/AttackSprites/fire/Fire9.png'], direction)

    def check_block(self, attack):
        if isinstance(attack, WaterAttack):
            print("Fire defend can't block Water attack!")
            return False
        return super().check_block(attack)


class EarthDefend(Defend):
    def __init__(self, screen, x, y, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/earth/rockwall.png'],direction)
    def check_block(self, attack):
        if isinstance(attack, FireAttack):
            print("Earth defend can't block Fire attack!")
            return False
        return super().check_block(attack)


