import math
import pygame


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):

        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y -
                             2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, (248, 188, 4), (self.x - 5, self.y - 5,
                         self.width + 10, self.height + 10), 2, 3)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                         self.width, self.height), 0, 2, 3)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 28)
            text = font.render(self.text, 1, (194, 221, 228))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


class Page():
    def __init__(self, screenSize) -> None:
        self.screenSize = screenSize
        self.startButton = Button(
            (33, 5, 53), screenSize[0] / 2 - 60, screenSize[1] / 2 + 40, 100, 50, 'Start')
        self.quitButton = Button(
            (201, 55, 76), screenSize[0] / 2 - 60, screenSize[1] / 2 + 120, 100, 50, 'Quit')
        self.retry = Button(
            (33, 5, 53), screenSize[0] / 2 - 60, screenSize[1] / 2 + 40, 100, 50, 'Retry')
        self.font = pygame.font.SysFont('comicsans', 100)

    def startPage(self, screen):
        image = pygame.image.load(
            f'./assets/1.png')
        image = pygame.transform.scale(image, (150, 300))
        image = pygame.transform.rotate(
            image, math.degrees(-3 * math.pi / 4))
        punchy = self.font.render("Punchy ", 1, (248, 188, 4))
        earth = self.font.render("Earth", 1, (16, 126, 87))
        screen.blit(
            image, (self.screenSize[0] / 2 - 300, self.screenSize[1]/2 - 250))
        screen.blit(
            punchy, (self.screenSize[0] / 2 - 300, self.screenSize[1]/2 - 250))
        screen.blit(
            earth, (self.screenSize[0] / 2 + 50, self.screenSize[1]/2 - 200))
        self.startButton.draw(screen)
        self.quitButton.draw(screen)
    
    
    def endPage(self, screen):
        gameO = self.font.render("Game", 1, (85, 145, 169))
        over = self.font.render("Over", 1, (118, 16, 30))
        screen.blit(
            gameO, (self.screenSize[0] / 2 - 300, self.screenSize[1]/2 - 100))
        screen.blit(
            over, (self.screenSize[0] / 2 + 50, self.screenSize[1]/2 - 50))
        self.retry.draw(screen)
        self.quitButton.draw(screen)

    def winPage(self, screen):
        you = self.font.render("You", 1, (248, 188, 4))
        won = self.font.render("Won", 1, (203, 229, 142))
        screen.blit(
            you, (self.screenSize[0] / 2 - 200, self.screenSize[1]/2 - 100))
        screen.blit(
            won, (self.screenSize[0] / 2 + 50, self.screenSize[1]/2 - 50))
        self.retry.draw(screen)
        self.quitButton.draw(screen)
