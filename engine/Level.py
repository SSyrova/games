import pygame


class Level():

    score = None

    def __init__(self, filename):
        _map = open(filename, 'r').read().splitlines()
        pygame.font.init()
        self.size = (len(_map[0]), len(_map))
        self.blocks = []
        self.block_group = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        Level.score = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 15)

        W_W, W_H = pygame.display.get_surface().get_size()
        offsetY = W_H - self.size[1] * 20
        if offsetY < 0:
            offsetY = 0

        for h in range(self.size[1]):
            for w in range(self.size[0]):
                c = _map[h][w]
                if c == 'X':
                    from engine.Object import Block
                    block = Block((w * 20 + 10, h * 20 + 10 + offsetY))
                    self.blocks.append(block)
                    self.block_group.add(block)
                if c == 'C':
                    from engine.Object import Coin
                    coin = Coin((w * 20 + 10, h * 20 + 10 + offsetY))
                    self.coins.add(coin)
                if c == 'E':
                    from engine.Object import Enemy
                    enemy = Enemy((w * 20 + 10, h * 20 + 10 + offsetY))
                    self.enemies.add(enemy)

        self.level_offsetX = 0
        self.level_offsetY = 0
        self.max_level_offsetX = W_W - self.size[0] * 20
        self.max_level_offsetY = W_H - self.size[1] * 20

    @staticmethod
    def addScore(score):
        Level.score += score

    def shiftLevel(self, offsetX, offsetY):
        if offsetX:
            if self.level_offsetX + offsetX > 0:
                offsetX = -self.level_offsetX
            elif self.level_offsetX + offsetX < self.max_level_offsetX:
                offsetX = self.max_level_offsetX - self.level_offsetX
            self.level_offsetX += offsetX
        if offsetY:
            if self.level_offsetY + offsetY > 0:
                offsetY = -self.level_offsetY
            elif self.level_offsetY + offsetY < self.max_level_offsetY:
                offsetY = self.max_level_offsetY - self.level_offsetY
            self.level_offsetY += offsetY
        for block in self.blocks:
            block.rect.x += offsetX
            block.rect.y += offsetY
        for coin in self.coins:
            coin.rect.x += offsetX
            coin.rect.y += offsetY

    def update(self, player_rect):
        for coin in self.coins:
            coin.update(player_rect)

    def render(self, window):
        self.block_group.draw(window)
        self.coins.draw(window)
        self.enemies.draw(window)
        score_text = self.font.render("Score: " + str(Level.score), 1, (0, 0, 0))
        window.blit(score_text, (5, 10))