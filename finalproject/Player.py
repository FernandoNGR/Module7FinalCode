import pygame
from attack import Attack, WaterAttack, AirAttack, EarthAttack, FireAttack
from Health import HealthBar
from defend import AirDefend, WaterDefend, FireDefend, EarthDefend

class Player:
    def __init__(self, screen, x, y, size, speed, images, P2_controls=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.P2_controls = P2_controls
        self.screen_width = screen.get_width()

        self.defend_height = self.y + 100
        self.attacking = False
        self.attacks = []

        self.current_defend = []

        #animation seq
        self.images = [pygame.image.load(image).convert_alpha() for image in images]
        if P2_controls: #75 is the horizontal size of the heart
            health_bar_x = self.screen_width - 3*75
            self.images = [pygame.transform.flip(image, True, False) for image in self.images]
        else:
            health_bar_x = 0
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(midtop=(self.x, self.y))
        self.animation_speed = 25
        self.animation_counter = 0

        #attack velocity
        self.velocity = 4

        #try to achieve like a RectMode(center)
        self.x = x - size // 2

        #add flip for player 2
        self.health_bar = HealthBar(screen, health_bar_x, 20)

        #new added stuff:
        self.is_dead = False


    def handle_input(self,predict):
        self.predict = predict
        self.valid = True

        keys = pygame.key.get_pressed()
        direction = 'right' if not self.P2_controls else 'left'
        if self.P2_controls:
            if len(self.predict) == 2:
                if keys[pygame.K_a] and len(self.attacks) < 1 or self.predict[0] == 0 and self.predict[1] == 5 or \
                        self.predict[0] == 0 and self.predict[1] == 4:
                    self.attacking = True
                    self.attacks.append(
                        AirAttack(self.screen, self.x, self.y + self.size // 2, self.velocity, direction))
                    self.valid = False
                elif keys[pygame.K_s] and len(self.attacks) < 1 or self.predict[0] == 1 and self.predict[1] == 5 or \
                        self.predict[0] == 1 and self.predict[1] == 4:
                    self.attacking = True
                    self.attacks.append(
                        WaterAttack(self.screen, self.x, self.y + self.size // 2, self.velocity, direction))
                    self.valid = False
                elif keys[pygame.K_d] and len(self.attacks) < 1 or self.predict[0] == 3 and self.predict[1] == 5 or \
                        self.predict[0] == 3 and self.predict[1] == 4:
                    self.attacking = True
                    self.attacks.append(
                        EarthAttack(self.screen, self.x, self.y + self.size // 2, self.velocity, direction))
                    self.valid = False
                elif keys[pygame.K_w] and len(self.attacks) < 1 or self.predict[0] == 2 and self.predict[1] == 5 or \
                        self.predict[0] == 2 and self.predict[1] == 4:
                    self.attacking = True
                    self.attacks.append(
                        FireAttack(self.screen, self.x, self.y + self.size // 2, self.velocity, direction))
                    self.valid = False

                elif keys[pygame.K_2] and len(self.current_defend) < 1 or self.predict[0] == 1 and self.predict[1]==6 and len(self.current_defend) < 1:
                    defend = WaterDefend(self.screen, self.x - 1.5*self.size , self.defend_height, direction)
                    self.current_defend.append(defend)
                    self.valid = False
                elif keys[pygame.K_1] and len(self.current_defend) < 1 or self.predict[0] == 0 and self.predict[1]==6 and len(self.current_defend) < 1 :
                    defend = AirDefend(self.screen, self.x - 1.5*self.size, self.defend_height, direction)
                    self.current_defend.append(defend)
                    self.valid = False
                elif keys[pygame.K_3] and len(self.current_defend) < 1 or self.predict[0] == 3 and self.predict[1]==6 and len(self.current_defend) < 1:
                    defend = EarthDefend(self.screen, self.x - 1.5*self.size, self.defend_height, direction)
                    self.current_defend.append(defend)
                    self.valid = False
                elif keys[pygame.K_4] and len(self.current_defend) < 1 or self.predict[0] == 2 and self.predict[1]==6 and len(self.current_defend) < 1:
                    defend = FireDefend(self.screen, self.x - 1.5*self.size, self.defend_height, direction)
                    self.current_defend.append(defend)
                    self.valid = False

        else:
            if keys[pygame.K_LEFT] and len(self.attacks) < 1:
                self.attacking = True
                self.attacks.append(AirAttack(self.screen, self.x + 10, self.y + self.size // 2, self.velocity, direction))
            elif keys[pygame.K_DOWN] and len(self.attacks) < 1:
                self.attacking = True
                self.attacks.append(WaterAttack(self.screen, self.x + 10, self.y + self.size // 2, self.velocity, direction))
            elif keys[pygame.K_UP] and len(self.attacks) < 1:
                self.attacking = True
                self.attacks.append(FireAttack(self.screen, self.x + 10, self.y + self.size // 2, self.velocity, direction))
            elif keys[pygame.K_RIGHT] and len(self.attacks) < 1:
                self.attacking = True
                self.attacks.append(EarthAttack(self.screen, self.x + 10, self.y + self.size // 2, self.velocity, direction))

            elif keys[pygame.K_5] and len(self.current_defend) < 1:
                defend = WaterDefend(self.screen, self.x + self.size, self.defend_height, direction)
                self.current_defend.append(defend)
            elif keys[pygame.K_6] and len(self.current_defend) < 1:
                defend = AirDefend(self.screen, self.x +self.size, self.defend_height, direction)
                self.current_defend.append(defend)
            elif keys[pygame.K_7] and len(self.current_defend) < 1:
                defend = EarthDefend(self.screen, self.x + self.size, self.defend_height, direction)
                self.current_defend.append(defend)
            elif keys[pygame.K_8] and len(self.current_defend) < 1:
                defend = FireDefend(self.screen, self.x + self.size, self.defend_height, direction)
                self.current_defend.append(defend)

        if keys[pygame.K_o]:
            self.y -= self.speed
        if keys[pygame.K_l]:
            self.y += self.speed
        return self.valid

    def check_attack_collision(self, other_player):
        # Check for collisions between attacks and defenses first
        for attack in other_player.attacks:
            for defend in self.current_defend:
                if pygame.Rect(attack.x, attack.y, attack.image.get_width(), attack.image.get_height()).colliderect(
                        pygame.Rect(defend.x, defend.y, defend.image.get_width(), defend.image.get_height())):
                    if defend not in attack.hit_defenses:
                        print("Collision detected between attack and defense")
                        if attack.hit(defend):
                            other_player.attacks.remove(attack)
                        if defend.hits_left <= 0:
                            self.current_defend.remove(defend)
                            return True


        # Then check for collisions between attacks
        for attack in self.attacks:
            for other_attack in other_player.attacks:
                if pygame.Rect(attack.x, attack.y, attack.image.get_width(), attack.image.get_height()).colliderect(
                        pygame.Rect(other_attack.x, other_attack.y, other_attack.image.get_width(),other_attack.image.get_height())):
                    collision_result = attack.check_attack_collision(other_attack)
                    if collision_result:
                        if collision_result == 'both':
                            self.attacks.remove(attack)
                            other_player.attacks.remove(other_attack)
                        else:
                            other_player.attacks.remove(other_attack)
                        return True
        return False

    # collision for if the player is hit [extend to make it look like player is damaged]
    def is_hit(self, other_player):
        for attack in other_player.attacks:
            if pygame.Rect(self.x, self.y, self.size, self.size).colliderect(pygame.Rect(attack.x, attack.y, attack.image.get_width(), attack.image.get_height())):
                other_player.attacks.remove(attack)

                self.health_bar.decrease_health()
                return True
        return False

    def draw(self):
        self.screen.blit(self.image, self.rect)

        for attack in self.attacks:
            attack.move()
            attack.draw()
        # Removes attacks off-screen
        self.attacks = [attack for attack in self.attacks if 0 < attack.x < self.screen_width]

        for defend in self.current_defend:
            defend.draw()

        self.health_bar.draw()


    def update(self,predict):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]

        self.valid = self.handle_input(predict)
        self.draw()

        for defend in self.current_defend:
            defend.update()

        for attack in self.attacks:
            attack.update()
        return self.valid
        # if self.health_bar.is_dead():
        #     self.animation_speed = 0
        #     self.images = [pygame.transform.rotate(image, 90) for image in self.images]
        #     self.y + 100

    def display_win_screen(self, win_message):
        font = pygame.font.Font(None, 100)
        text = font.render(win_message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        quit()