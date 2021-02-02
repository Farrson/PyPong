import pygame
import sys
from game import Pong
from actors import PongBall


def main():
    pygame.init()
    screensize = (1000, 700)
    win = pygame.display.set_mode(screensize)
    pygame.display.set_caption("PONG")
    pong = Pong(screensize)
    ball = PongBall(screensize)
    running = True
    clock = pygame.time.Clock()

    # enter menu
    pong.display_main(win)

    while running:
        clock.tick(60)
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_p:
                    pong.pause_game(win)
                if evt.key == pygame.K_PLUS: # define a limit otherwise it breaks the game or adjust score condition
                    ball.speedx += 1
                    ball.speedy += 1
                    pong.paddle_left.speed += 1
                    pong.paddle_right.speed += 1
                if evt.key == pygame.K_MINUS:
                    ball.speedx -= 1
                    ball.speedy -= 1
                    pong.paddle_left.speed -= 1
                    pong.paddle_right.speed -= 1

        # game
        ball.update_pos(pong.paddle_left, pong.paddle_right)
        win.fill((0, 0, 0))
        ball.render(win)
        pong.paddle_left.render(win, screensize, ball)
        pong.paddle_right.render(win, screensize, ball)

        # if ball.rect.right >= screensize[0]:
         #    running = 0
        pong.point_scored(ball)
        # display score and options
        pong.display_score(win)
        pong.display_options(win, ball, pong.paddle_left, pong.paddle_right)
        # refresh screen
        pygame.display.flip()

    pygame.quit()


# run the game
main()
