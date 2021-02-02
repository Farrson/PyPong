import pygame
import time


class BotPaddle(object):
    def __init__(self, screensize, position):
        # set paddle size
        self.width = 10
        self.height = 100
        self.color = [255, 255, 255]
        self.posx = 0
        self.posy = 0
        # set paddle position (center of the rectangle)
        if position == 0:
            self.posx = 5  # player is always on left side
            self.posy = 50 + screensize[1] // 2  # midpoint
        elif position == 1:
            self.posx = screensize[0] - 5
            self.posy = 50 + screensize[1] // 2
        else:
            raise ValueError("Paddle position is either 0 or 1")
        # create paddle as rect
        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)
        # set speed and direction (0 so there is no automatic movement)
        self.speed = 5
        self.direction = 0

    def update(self, screensize, pongball):
        # adjust using timeouts and/or probability to make BOT beatable
        if self.posy > pongball.posy:
            self.direction = -1
        if self.posy < pongball.posy:
            self.direction = 1

        self.posy += self.speed * self.direction
        # handle collisions with screensize
        self.posy += self.speed * self.direction
        # paddle cant go beyond top of the screen
        if self.posy - self.height // 2 < 100:
            self.posy = self.height // 2 + 100
        # paddle cant leave bottom the screen
        if self.posy + self.height // 2 > screensize[1]:
            self.posy = screensize[1] - self.height // 2

        self.rect.center = (self.posx, self.posy)
        # handle collisions with screensize
        # if self.rect.top < 0 or rect.bottom > screen[1]

    def render(self, canvas, screensize, pongball):
        self.update(screensize, pongball)
        pygame.draw.rect(canvas, self.color, self.rect)


class PlayerPaddle(BotPaddle):
    def __init__(self, screensize, position, keyset):
        super().__init__(screensize, position)
        self.keyset = keyset

    def update(self, screensize):
        # paddles only move vertically, so only update y-pos
        pressed = pygame.key.get_pressed()
        if pressed[self.keyset[1]]:
            self.direction = 1
        if pressed[self.keyset[0]]:
            self.direction = -1
        # handle collisions with screensize
        self.posy += self.speed * self.direction
        # paddle cant go beyond top of the screen
        if self.posy - self.height // 2 < 100:
            self.posy = self.height // 2 + 100
        # paddle cant leave bottom the screen
        if self.posy + self.height // 2 > screensize[1]:
            self.posy = screensize[1] - self.height // 2

        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)

    def render(self, canvas, screensize, ball):
        self.update(screensize)
        # reset direction to stop paddle from moving
        self.direction = 0
        pygame.draw.rect(canvas, self.color, self.rect)




class PongBall(object):
    def __init__(self, screensize):
        # ball should be at the center of game screen at the start
        self.screensize = screensize
        self.posx = screensize[0] // 2
        self.posy = 50 + screensize[1] // 2
        # define size and color of the ball
        self.width = 8
        self.height = 8
        self.color = [255, 255, 255]
        self.rect = pygame.Rect(self.posx - self.width,
                                self.posy - self.height,
                                self.width*2, self.height*2)

        # set direction and speed
        self.direction = [1, -1]
        self.speedx = 7
        self.speedy = 7

    def update_pos(self, paddleA, paddleB):
        self.posx += self.direction[0] * self.speedx
        self.posy += self.direction[1] * self.speedy
        # posx, posy instead of creating new rect everytime
        # use self.rect.center = posx...
        self.rect.center = (self.posx, self.posy)
        # stop the ball from going over the top of window
        if self.rect.top <= 100:
            self.direction[1] = 1
        # stop the ball from going below the window
        if self.rect.bottom >= self.screensize[1] - 1:
            self.direction[1] = -1
        # handle collision with paddles
        if self.rect.colliderect(paddleA):
            self.direction[0] = 1
        if self.rect.colliderect(paddleB):
            self.direction[0] = -1

    def render(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)

    def reset(self):
        self.posx = self.screensize[0] // 2
        self.posy = 50 + self.screensize[1] // 2
        # ADD: change directions x and y
        # give players time to prepare for the game to reestart
        time.sleep(0.5)
