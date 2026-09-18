import pygame

from src.game.collision import *
from src.player.player import *
from src.game.generate import *


def main():
    pygame.init()

    clock = pygame.time.Clock()
    running = True

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode()
    (WIDTH, HEIGHT) = pygame.display.get_window_size()

    HEIGHT = int(HEIGHT*0.93)

    pygame.display.set_mode(size=(WIDTH, HEIGHT))
    
    pygame.display.set_caption("flappy bird")
    
    screenManager = Screen(width=WIDTH, height=HEIGHT)
    bird = Bird(x=BIRD_X, y=HEIGHT*0.25, r=BIRD_RAD, height=HEIGHT)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        #update
        screenManager.update()
        touch_bottom = bird.update()

        if touch_bottom:
            running = False

        #check box collisions
        player_pos = bird.getBall()
        boxes = screenManager.get_obstacles()

        for obstacle in boxes:
            if ball_box_collides(player_pos, obstacle):
                running = False

        #render
        screenManager.render_bg(screen)
        bird.render(screen)
        screenManager.render(screen)

        #update display
        pygame.display.flip()

if __name__ == "__main__":
    main()