# main game loop ( refactor )

import pygame
import sys
import time


class Pong(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.midx = screensize[0] // 2
        self.midy = screensize[1] // 2
        self.score_a = 0
        self.score_b = 0

    def point_scored(self, ball):
        if ball.posx < 0:
            self.score_b += 1
            ball.reset()
        if ball.posx > self.screensize[0]:
            self.score_a += 1
            ball.reset()

    def display_options(self, canvas, ball, player_one, player_two):
        font = pygame.font.Font(None, 20)
        pause_key = font.render("P - Pause", True, pygame.color.Color('orange'))
        speedup_key = font.render("+ - Speed up", True, pygame.color.Color('orange'))
        speeddown_key = font.render("- - Speed down", True, pygame.color.Color('orange'))

        canvas.blit(pause_key, [5, 5])
        canvas.blit(speedup_key, [5, 25])
        canvas.blit(speeddown_key, [5, 45])

    def display_score(self, canvas):
        pygame.draw.line(canvas, [255, 255, 255], [0, 100], [self.screensize[0], 100], 5)
        font = pygame.font.Font(None, 80)
        score_display_a = font.render(str(self.score_a), True, [255, 255, 255])
        score_display_b = font.render(str(self.score_b), True, [255, 255, 255])
        score_vs = font.render("-", True, [255, 255, 255])
        canvas.blit(score_display_a, [400, 20])
        canvas.blit(score_display_b, [585, 20])
        canvas.blit(score_vs, [500, 20])

    def pause_game(self, canvas):
        font = pygame.font.Font(None, 120)
        font2 = pygame.font.Font(None, 60)
        pause_txt = font.render("PAUSE", False, pygame.color.Color('red'))
        pause_subtxt = font2.render("press >SPACE< to continue", True, pygame.color.Color('red'))
        canvas.blit(pause_txt, [350, 200])
        canvas.blit(pause_subtxt, [250, 300])
        pygame.display.flip()
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_SPACE:
                        return


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


class PlayerPaddle(object):
    def __init__(self, screensize):
        # set paddle size
        self.width = 10
        self.height = 100
        self.color = [255, 255, 255]
        # set paddle position (center of the rectangle)
        self.posx = 5  # player is always on left side
        self.posy = 50 + screensize[1] // 2  # midpoint
        # create paddle as rect
        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)
        # set speed and direction (0 so there is no automatic movement)
        self.speed = 5
        self.direction = 0

    def update(self, screensize):
        # paddles only move vertically, so only update y-pos
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_DOWN]:
            self.direction = 1
        if pressed[pygame.K_UP]:
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

    def render(self, canvas, screensize):
        self.update(screensize)
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
        self.posy = 50 + screensize[1] // 2
        # create paddle as rect
        self.rect = pygame.Rect(self.posx - self.width // 2,
                                self.posy - self.height // 2,
                                self.width, self.height)
        #
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


def main():

    pygame.init()
    screensize = (1000, 700)
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
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_p:
                    pong.pause_game(win)
                if evt.key == pygame.K_PLUS:
                    ball.speedx += 1
                    ball.speedy += 1
                    player.speed += 1
                    bot.speed += 1
                if evt.key == pygame.K_MINUS:
                    ball.speedx -= 1
                    ball.speedy -= 1
                    player.speed -= 1
                    bot.speed -= 1

        # game
        ball.update_pos(player, bot)
        win.fill((0, 0, 0))
        ball.render(win)
        player.render(win, screensize)
        bot.render(win, screensize, ball)

        # if ball.rect.right >= screensize[0]:
         #    running = 0
        pong.point_scored(ball)
        # display score and options
        pong.display_score(win)
        pong.display_options(win, ball, player, bot)
        # refresh screen
        pygame.display.flip()

    pygame.quit()


# run the game
main()
