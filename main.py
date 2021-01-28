# main game loop

import pygame
import time
import sys


class Pong(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.midx = screensize[0] // 2
        self.midy = screensize[1] // 2


class PongBall(object):
    def __init__(self, screensize):
        # ball should be at the center of game screen at the start
        self.screensize = screensize
        self.posx = screensize[0] // 2
        self.posy = screensize[1] // 2
        # define size and color of the ball
        self.width = 8
        self.height = 8
        self.color = [255, 255, 255]

        self.rect = pygame.Rect(self.posx - self.width,
                                self.posy - self.height,
                                self.width*2, self.height*2)

        # set direction and speed
        self.direction = [1, -1]
        self.speedx = 1
        self.speedy = 1

    def update_pos(self):
        self.posx += self.direction[0] * self.speedx
        self.posy += self.direction[1] * self.speedy
        # posx, posy instead of creating new rect everytime
        # use self.rect.center = posx...
        self.rect.center = (self.posx, self.posy)
        # stop the ball from going over the top of window
        if self.rect.top <= 0:
            self.direction[1] = 1
        # stop the ball from going below the window
        if self.rect.bottom >= self.screensize[1] - 1:
            self.direction[1] = -1

    def render(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)


class PlayerPaddle(object):
    def __init__(self, screensize):
        # set paddle size
        self.width = 10
        self.height = 100
        self.color = [255, 255, 255]
        # set paddle position (center of the rectangle)
        self.posx = 5  # player is always on left side
        self.posy = screensize[1] // 2  # midpoint
        # create paddle as rect
        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)
        # set speed and direction (0 so there is no automatic movement)
        self.speed = 5
        self.direction = 0

    def update(self):
        # paddles only move vertically, so only update y-pos
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            self.direction = 1
        if pressed[pygame.K_UP]:
            self.direction = -1

        self.posy += self.speed*self.direction
        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)
        # handle collisions with screensize
        # if self.rect.top < 0 or rect.bottom > screen[1]

    def render(self, canvas):
        self.update()
        # reset direction to stop paddle from moving
        self.direction = 0
        pygame.draw.rect(canvas, self.color, self.rect)


class BotPaddle(object):
    def __init__(self, screensize):
        # set paddle size
        self.width = 10
        self.height = 100
        self.color = [255, 255, 255]
        # set paddle position
        self.posx = screensize[0] - 5
        self.posy = screensize[1] // 2
        # create paddle as rect
        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)
        #
        self.speed = 10
        self.direction = 0

    def update(self):
        # paddles only move vertically, so only update y-pos
        self.posy += self.speed * self.direction
        self.rect.center = (self.posx, self.posy)
        # handle collisions with screensize
        # if self.rect.top < 0 or rect.bottom > screen[1]

    def render(self, canvas):
        self.update()
        pygame.draw.rect(canvas, self.color, self.rect)


def main():

    pygame.init()
    screensize = (800, 600)
    win = pygame.display.set_mode(screensize)
    pygame.display.set_caption("PONG")
    pong = Pong(screensize)
    ball = PongBall(screensize)
    player = PlayerPaddle(screensize)
    bot = BotPaddle(screensize)
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ball.update_pos()
        win.fill((0, 0, 0))
        ball.render(win)
        player.render(win)
        bot.render(win)
        pygame.display.flip()
        # time.sleep(0.1)
        if ball.rect.right >= screensize[0]:
            running = 0

    pygame.quit()


# run the game
main()
