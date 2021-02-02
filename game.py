import pygame
import sys
from actors import PlayerPaddle, BotPaddle

KEYSET1 = [pygame.K_UP, pygame.K_DOWN]
KEYSET2 = [pygame.K_w, pygame.K_s]


class Pong(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.midx = screensize[0] // 2
        self.midy = screensize[1] // 2
        self.score_a = 0
        self.score_b = 0
        self.paddle_left = PlayerPaddle(screensize, 0, KEYSET1)
        self.paddle_right = BotPaddle(screensize, 1)

    def point_scored(self, ball):
        if ball.posx < 0:
            self.score_b += 1
            ball.reset()
        if ball.posx > self.screensize[0]:
            self.score_a += 1
            ball.reset()

    def create_Button(self,txt, canvas, x, y, color, size, boxed):
        font = pygame.font.Font(None, size)
        button_txt = font.render(txt, True, color)
        rect = button_txt.get_rect()
        rect.center = (x, y)
        canvas.blit(button_txt, rect)
        if boxed:
            padding = 20
            box = rect[0] - padding, rect[1] - padding / 2, rect[2] + padding * 2, rect[3] + padding
            pygame.draw.rect(canvas, pygame.color.Color("white"), box, 5)
        return rect

    def display_main(self, canvas):
        # set background for main menu
        canvas.fill([80, 120, 80])
        headline = self.create_Button("WELCOME TO PONG", canvas, 500, 70, pygame.color.Color("pink"), 60, False)
        settings = self.create_Button(">>SETTINGS<<", canvas, 500, 140, pygame.color.Color("pink"), 50, False)
        mode = self.create_Button("Choose Mode: ", canvas, 300, 300, pygame.color.Color("skyblue"), 40, True)
        button1 = self.create_Button("Start", canvas, 300, 250, pygame.color.Color("skyblue"), 40, True)
        button2 = self.create_Button("Singleplayer", canvas, 520, 300, pygame.color.Color("skyblue"), 30, True)
        button3 = self.create_Button("Multiplayer", canvas, 700, 300, pygame.color.Color("skyblue"), 30, True)

        pygame.display.flip()
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # click "Start" button
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button1.collidepoint(pos):
                        return
                # handle "choose mode" options
                    if button2.collidepoint(pos):
                        padding = 20
                        rect = button2
                        box = rect[0] - padding, rect[1] - padding / 2, rect[2] + padding * 2, rect[3] + padding
                        pygame.draw.rect(canvas, pygame.color.Color("orange"), box, 5)
                        # reset the "multiplayer" button
                        rect2 = button3
                        box2 = rect2[0] - padding, rect2[1] - padding / 2, rect2[2] + padding * 2, rect2[3] + padding
                        pygame.draw.rect(canvas, pygame.color.Color("white"), box2, 5)
                        self.paddle_right = BotPaddle(self.screensize, 1)
                        pygame.display.flip()
                    if button3.collidepoint(pos):
                        padding = 20
                        rect = button3
                        box = rect[0] - padding, rect[1] - padding / 2, rect[2] + padding * 2, rect[3] + padding
                        pygame.draw.rect(canvas, pygame.color.Color("orange"), box, 5)
                        # reset the "singleplayer" button
                        rect2 = button2
                        box2 = rect2[0] - padding, rect2[1] - padding / 2, rect2[2] + padding * 2, rect2[3] + padding
                        pygame.draw.rect(canvas, pygame.color.Color("white"), box2, 5)
                        self.paddle_right = PlayerPaddle(self.screensize, 1, KEYSET2)
                        pygame.display.flip()




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

