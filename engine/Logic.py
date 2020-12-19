import pygame

class Logic:

    def input(self, events):
        pass

    def update(self):
        pass

    def render(self, window):
        pass


class GameLogic(Logic):

    def __init__(self):
        from engine.Object import Player
        self.player = Player()
        from engine.Level import Level
        self.level = Level('level_1.txt')
        from engine.Object import Background
        self.background = Background()

    def input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                from engine import Engine
                Engine.stop()
        self.player.input(events)


    def update_camera(self):
        W_W, W_H = pygame.display.get_surface().get_size()
        if self.player.rect.centerx >= W_W / 2 and \
                self.level.level_offsetX > self.level.max_level_offsetX:
            diff = self.player.rect.centerx - W_W / 2
            self.player.rect.centerx = W_W / 2
            self.level.shiftLevel(-diff, 0)
        if self.player.rect.centerx <= W_W / 2 and \
                self.level.level_offsetX < 0:
            diff = W_W / 2 - self.player.rect.centerx
            self.player.rect.centerx = W_W / 2
            self.level.shiftLevel(diff, 0)

    def update(self):
        self.player.update(self.level.blocks, self.level.boosters)
        self.level.update(self.player.rect)
        self.update_camera()

    def render(self, window: pygame.SurfaceType):
        window.fill((255, 255, 255))
        self.background.render(window)
        self.level.render(window)
        self.player.render(window)
        pygame.display.flip()