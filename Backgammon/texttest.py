import pygame
import sys

LEFT, CENTER, RIGHT = range(3)
TOP, MIDDLE, BOTTOM = range(3)


class RenderText(pygame.sprite.Sprite):
    # pos = None
    # pos_rel = None

    def __init__(self, screen, text='text', pos=(0, 0), pos_rel=(LEFT, TOP),
                 font=None, size=20, color=(255, 255, 255), antialias=True):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.text = text
        self.pos = pos
        self.pos_rel = pos_rel
        self.screen = screen
        self.antialias = antialias

        self.rerender()

    def update(self):
        pass

    def calculate_position(self):
        return (
            self.pos_rel[0]*(self.screen.get_size()[0]/2 - self.rect.width/2)
            + (1-2*(self.pos_rel[0]/2))*self.pos[0],
            self.pos_rel[1]*(self.screen.get_size()[1]/2 - self.rect.height/2)
            + (1-2*(self.pos_rel[1]/2))*self.pos[1],
            )

    def print_text(self, text, pos=None):
        self.text = text
        if pos:
            self.pos = pos
        self.rerender()

    def rerender(self):
        self.image = self.font.render(self.text, self.antialias, self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.calculate_position()


if __name__ == '__main__':
    class Example(object):
        def __init__(self):
            pass

        def initialize(self):
            pygame.init()
            # self.screen = \
            #     pygame.display.set_mode(pygame.display.list_modes()[0])
            self.screen = pygame.display.set_mode((640, 480))
            pygame.display.set_caption('textrender example')

            self.clock = pygame.time.Clock()
            self.sprites = pygame.sprite.RenderUpdates()

            self.status_text = RenderText(
                self.screen, 'FPS', size=42, pos=[50, 50],
                pos_rel=(RIGHT, BOTTOM))

            self.sprites.add(self.status_text)

            pos_text = (
                ['LEFT', 'CENTER', 'RIGHT'],
                ['TOP', 'MIDDLE', 'BOTTOM'],
                )

            for x in range(3):
                for y in range(3):
                    self.sprites.add(RenderText(
                        self.screen, pos_text[0][x] + ', ' + pos_text[1][y],
                        pos=(20, 20), pos_rel=(x, y)))

            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((25, 25, 125))

            self.screen.blit(self.background, (0, 0))
            pygame.display.update()

        def run(self):
            self.initialize()

            while True:
                self.clock.tick(30)
                self.status_text.print_text('FPS: %d' % self.clock.get_fps())
                self.sprites.clear(self.screen, self.background)

                dirty = self.sprites.draw(self.screen)
                pygame.display.update(dirty)

                events = pygame.event.get()   
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit()


    Example().run()
