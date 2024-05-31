import pygame

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img = pygame.image.load(f'assets/img/enemy1/Run-{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.passed = False

    def update(self, game_over):
        if not game_over:
            self.rect.x -= 5
            if self.rect.right < 0:
                self.kill()
            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)


class Drone1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img = pygame.image.load(f'assets/img/drone1/Walk-{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.passed = False
    def update(self, game_over):
        if not game_over:
            self.rect.x -= 5
            if self.rect.right < 0:
                self.kill()
            self.counter += 1
            cooldown = 5
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
        