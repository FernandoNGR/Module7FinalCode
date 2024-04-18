import pygame

class Attack():
    def __init__(self, screen, x, y, image_paths, velocity, direction, size=(150, 75)):
        self.screen = screen
        self.x = x
        self.y = y
        self.images = [pygame.transform.scale(pygame.image.load(image_path), size) for image_path in image_paths]
        self.current_image = 0  # This will track the current image of the animation

        self.velocity = velocity
        self.direction = direction

        self.animation_speed = 10  # Determines how fast the animation plays
        self.animation_counter = 0  # Counts up to change the sprite based on animation_speed

        if self.direction == ("left"):
            self.images = [pygame.transform.flip(image, True, False) for image in self.images]
        self.image = self.images[self.current_image]

        #change the rect to whatever idk
        self.rect = self.image.get_rect(midbottom=(x, y))


        # eh?
        self.hit_defenses = []

    def hit(self, defend):
        if defend not in self.hit_defenses:
            if defend.check_block(self):  # If the defense can block the attack
                defend.hits_left -= 1
            else:  # If the attack beats the defense
                defend.hits_left -= 2
            self.hit_defenses.append(defend)
            return True  # Indicate that the attack should be remov

    def move(self):
        if self.direction == "right":
            self.x += self.velocity
        elif self.direction == "left":
            self.x -= self.velocity
        self.rect = (self.x, self.y)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.move()
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)  # Cycle through images
            self.image = self.images[self.current_image]


class AirAttack(Attack):
    def __init__(self, screen, x, y, velocity, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/air/airslice1.png','Graphics/AttackSprites/air/airslice2.png','Graphics/AttackSprites/air/airslice3.png'], velocity, direction)

    def check_attack_collision(self, other_projectile):
        if isinstance(other_projectile, WaterAttack):
            print("Air attack beats water attack!")
            return True

        #maybe remove the or is instance and use this for defence
        elif isinstance(other_projectile, AirAttack) or isinstance(other_projectile, FireAttack):
            print("Both attacks are destroyed!")
            return 'both'
        return False

class WaterAttack(Attack):
    def __init__(self, screen, x, y, velocity, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/water/waterattack1.png','Graphics/AttackSprites/water/waterattack2.png','Graphics/AttackSprites/water/waterattack3.png','Graphics/AttackSprites/water/waterattack4.png','Graphics/AttackSprites/water/waterattack5.png'], velocity, direction)

    def check_attack_collision(self, other_projectile):
        if isinstance(other_projectile, FireAttack):
            print("Water attack beats fire attack!")
            return True


        elif isinstance(other_projectile, WaterAttack) or isinstance(other_projectile, EarthAttack):
            print("Both attacks are destroyed!")
            return 'both'
        return False

class FireAttack(Attack):
    def __init__(self, screen, x, y, velocity, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/fire/Fire1.png', 'Graphics/AttackSprites/fire/Fire2.png', 'Graphics/AttackSprites/fire/Fire3.png'], velocity, direction, size = (175,75))

    def check_attack_collision(self, other_projectile):
        if isinstance(other_projectile, EarthAttack):
            print("Fire attack beats earth attack!")
            return True

        elif isinstance(other_projectile, FireAttack):
            print("Both fire attacks are destroyed!")
            return 'both'
        return False

class EarthAttack(Attack):
    def __init__(self, screen, x, y, velocity, direction):
        super().__init__(screen, x, y, ['Graphics/AttackSprites/earth/Rock1.png','Graphics/AttackSprites/earth/Rock2.png','Graphics/AttackSprites/earth/Rock3.png','Graphics/AttackSprites/earth/Rock4.png'], velocity, direction, size = (100,100))

    def check_attack_collision(self, other_projectile):
        if isinstance(other_projectile, AirAttack):
            print("Earth attack beats air attack!")
            return True

        elif isinstance(other_projectile, EarthAttack):
            print("Both earth attacks are destroyed!")
            return 'both'
        return False
