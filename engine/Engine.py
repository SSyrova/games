import pygame


class Engine:
    running = False
    window = None
    logic = None
    clock = None

    def init(self):
        pygame.init()

    def run(self):
        Engine.window = pygame.display.set_mode((600, 400))
        Engine.clock = pygame.time.Clock()
        from engine.Logic import GameLogic
        Engine.logic = GameLogic()
        Engine.running = True
        while Engine.running:
            Engine.logic.input(pygame.event.get())
            Engine.logic.update()
            Engine.logic.render(Engine.window)
            Engine.clock.tick(60)
        pygame.quit()

    @staticmethod
    def stop():
        Engine.running = False