import pygame

from src.game.collision import *
from src.player.player import *
from src.game.generate import *
from src.agent.agent import *


def render(screen, screenManager, bird):
    #render
    screenManager.render_bg(screen)
    bird.render(screen)
    screenManager.render(screen)
    
    #update display
    pygame.display.flip()


def main():
    pygame.init()

    clock = pygame.time.Clock()

    info = pygame.display.get_desktop_sizes()[0]
    WIDTH, HEIGHT = info[0], int(info[1] * 0.93)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("flappy bird")

    if AGENT:
        agent = Agent(HEIGHT)

    while True:
        running = True
        screenManager = Screen(width=WIDTH, height=HEIGHT)
        bird = Bird(x=BIRD_X, y=HEIGHT*0.5, r=BIRD_RAD, height=HEIGHT)

        while running:
            if not TRAINING: clock.tick(FPS)   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if not AGENT and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            #run action through agent
            if AGENT:
                prev_bird = bird.getBall()
                prev_obstacles = screenManager.get_obstacles()
                prev_state = agent.determine_state(prev_bird, bird.getVy(), prev_obstacles)
                
                action = agent.get_action(prev_state)
                if action:
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

            #update agent
            if AGENT:
                new_state = agent.determine_state(bird.getBall(), bird.getVy(), screenManager.get_obstacles())

                prev_obstacle_x = prev_obstacles[0].x + prev_obstacles[0].w

                if not running:
                    reward = -100
                #check passed
                elif prev_obstacle_x - prev_bird.x > 0 and new_state[0] < 0:
                    reward = 15
                
                else:
                    reward = 1

                agent.update_q(prev_state, action, new_state, reward, not running)

                if not running:
                    render(screen, screenManager, bird)
                    agent.die()

            if not TRAINING: render(screen, screenManager, bird)

if __name__ == "__main__":
    main()