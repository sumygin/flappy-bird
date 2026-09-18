import pygame

from src.game.collision import *
from src.player.player import *
from src.game.generate import *
from src.agent.agent import *


def render(screen, screenManager, bird, font=None, pipes_passed=None, trials=None, width=None, height=None):
    # render bg
    screenManager.render_bg(screen)
    bird.render(screen)
    screenManager.render(screen)

    if font and pipes_passed is not None and trials:
        #generate text surfaces
        avg = pipes_passed / trials if trials > 0 else 0
        score_surface = font.render(f"Avg pipes passed: {avg:.2f}", True, RED)
        trials_surface = font.render(f"Trials: {trials}", True, RED)

        #draw text
        screen.blit(score_surface, (20, 30))
        screen.blit(trials_surface, (20, 60))
    
    # Push to display
    pygame.display.flip()


def main():
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    info = pygame.display.get_desktop_sizes()[0]
    WIDTH, HEIGHT = info[0], int(info[1] * 0.93)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("flappy bird")

    pipes_passed = 0
    trials = 1

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

            #check if passed box
            passed = False

            obstacles = screenManager.get_obstacles()
            if len(obstacles) > 0:
                first_box = obstacles[0]

                if not first_box.passed and BIRD_X > first_box.x + first_box.w:
                    passed = True
                    first_box.passed = True

            #update agent
            if AGENT:
                new_state = agent.determine_state(bird.getBall(), bird.getVy(), screenManager.get_obstacles())

                if not running:
                    reward = -100
                #check passed
                elif passed:
                    reward = 15
                    pipes_passed += 1
                
                else:
                    reward = 1

                agent.update_q(prev_state, action, new_state, reward, not running)

                if not running: 
                    if TRAINING: render(screen, screenManager, bird, font, pipes_passed, trials, WIDTH, HEIGHT)
                    agent.die()

            if not TRAINING: render(screen, screenManager, bird, font, pipes_passed, trials, WIDTH, HEIGHT)

        trials += 1

if __name__ == "__main__":
    main()