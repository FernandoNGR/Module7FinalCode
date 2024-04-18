import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.background = pygame.image.load("Graphics/Menu.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.font = pygame.font.Font(None, 64)
        self.text = self.font.render("Press ENTER to Start", True, (246, 90, 31))
        self.text_rect = self.text.get_rect(center=(self.width // 2, self.height - (self.height // 5)))

        self.show_text = True
        self.toggle_frequency = 720  # Toggle frequency (in frames)

    def display(self):
        menu_running = True
        toggle_counter = 0
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu_running = False

            # Toggle text visibility based on toggle frequency
            toggle_counter += 1
            if toggle_counter >= self.toggle_frequency:
                self.show_text = not self.show_text
                toggle_counter = 0

            self.screen.blit(self.background, (0, 0))
            if self.show_text:
                self.screen.blit(self.text, self.text_rect)
            pygame.display.flip()