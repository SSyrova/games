import math
import pygame



class Object(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = None
        self.rect = None

    def input(self, events):
        pass

    def update(self, *args):
        pass

    def render(self, window):
        window.blit(self.image, self.rect)

class Player(Object):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('img/player/1.png'), (40,40))
        self.rect = self.image.get_rect()
        self.speedx = 0
        self.speedy = 0
        self.init_animation()
        self.speed = 3
        self.isBoost = False
        self.timer = 0

    def init_animation(self):
        self.idle_animation = [pygame.transform.scale(pygame.image.load('img/player/1.png'), (40, 40))]
        self.run_animation = [pygame.transform.scale(pygame.image.load('img/player/2.png'), (40, 40)),
                              pygame.transform.scale(pygame.image.load('img/player/3.jpg'), (40, 40)),
                              pygame.transform.scale(pygame.image.load('img/player/4.jpg'), (40, 40)),
                              pygame.transform.scale(pygame.image.load('img/player/5.jpg'), (40, 40)),
                              pygame.transform.scale(pygame.image.load('img/player/6.jpg'), (40, 40)),
                              pygame.transform.scale(pygame.image.load('img/player/7.jpg'), (40, 40))]
        self.current_animation = self.idle_animation
        self.animation_frame = 0
        self.max_animation_frame = ((len(self.idle_animation) * len(self.run_animation)) // math.gcd(len(self.idle_animation), len(self.run_animation))) * 10

    def animate(self):
        if self.speedx != 0:
            if self.current_animation != self.run_animation:
                self.animation_frame = 0
            self.current_animation = self.run_animation
        else:
            if self.current_animation != self.idle_animation:
                self.animation_frame = 0
            self.current_animation = self.idle_animation
        image = self.current_animation[self.animation_frame // 10 % len(self.current_animation)]
        if self.speedx >= 0:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
        if self.animation_frame >= self.max_animation_frame:
            self.animation_frame = 0
        else:
            self.animation_frame += 1

    def input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.speedx = - self.speed
                elif event.key == pygame.K_RIGHT:
                    self.speedx = self.speed
                elif event.key == pygame.K_SPACE:
                    self.speedy = -15
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT and self.speedx == -self.speed) or (event.key == pygame.K_RIGHT and self.speedx == self.speed):
                    self.speedx = 0

    def update(self, *args):
        self.calc_gravity()

        boosters = pygame.sprite.spritecollide(self, args[1], False)
        if boosters:
            self.speed = 15
            if self.speedx >= 0:
                self.speedx = self.speed
            elif self.speedx <= 0:
                self.speedx = - self.speed
            self.isBoost = True
            self.timer = 20
            for booster in boosters:
                booster.kill()

        if self.isBoost and self.timer > 0:
            self.timer -= 1

        if self.isBoost and self.timer == 0:
            self.isBoost = False
            self.speed = 3

        h = pygame.display.get_surface().get_height()
        if self.rect.bottom > h and self.speedy > 0:
            self.speedy = 0
            self.rect.bottom = h

        self.rect.centerx += self.speedx

        block_hit_list = pygame.sprite.spritecollide(self, args[0], False)
        for block in block_hit_list:
            if self.speedx > 0:
                self.rect.right = block.rect.left
            elif self.speedx < 0:
                self.rect.left = block.rect.right
            self.speedx = 0

        self.rect.centery += self.speedy

        block_hit_list = pygame.sprite.spritecollide(self, args[0], False)
        for block in block_hit_list:
            if self.speedy > 0:
                self.rect.bottom = block.rect.top
            elif self.speedy < 0:
                self.rect.top = block.rect.bottom
            self.speedy = 0

        self.animate()

    def calc_gravity(self):
        self.speedy += 0.5

class Block(Object):

    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('img/block/block2.jpg'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

class Coin(Object):

    def __init__(self, location: tuple):
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.transform.scale(pygame.image.load('img/coin/coin_1.png'), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = location[0]
        self.rect.centery = location[1]
        self.animation = []
        self.animation_frame = 0
        self.frame_per_sprite = 2
        self.max_animation_frame = 0
        self.init_animation()

    def init_animation(self):
        coin_1 = pygame.image.load('img/coin/coin_1.png')
        coin_2 = pygame.image.load('img/coin/coin_2.png')
        coin_3 = pygame.image.load('img/coin/coin_3.png')
        coin_4 = pygame.image.load('img/coin/coin_4.png')
        coin_5 = pygame.image.load('img/coin/coin_5.png')
        coin_6 = pygame.image.load('img/coin/coin_6.png')
        self.animation = [
            pygame.transform.scale(coin_1, (20, 20)),
            pygame.transform.scale(coin_2, (20, 20)),
            pygame.transform.scale(coin_3, (20, 20)),
            pygame.transform.scale(coin_4, (20, 20)),
            pygame.transform.scale(coin_5, (20, 20)),
            pygame.transform.scale(coin_6, (20, 20)),
        ]
        self.max_animation_frame = 6

    def update(self, player_rect):
        self.image = self.animation[self.animation_frame // self.frame_per_sprite]
        self.animation_frame += 1
        if self.animation_frame >= self.max_animation_frame * self.frame_per_sprite - 1:
            self.animation_frame = 0
        if self.rect.colliderect(player_rect):
            from engine.Level import Level
            Level.addScore(1)
            self.kill()


class Background(Object):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('img/background/background.jpg'), (pygame.display.get_surface().get_size()))

    def render(self, window):
        window.blit(self.image, (0, 0))

class Enemy(Object):
    def __init__(self, position,  * groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('img/enemy/rick.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]


class Booster(Object):
    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('img/booster/booster.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]