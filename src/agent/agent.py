from pathlib import Path
from collections import defaultdict
import pickle, random, os
from game.collision import clamp


from game.generate import Circle, Box
from config.constants import *


def round_to_n(val, n):
    return val//n

class Agent:
    def __init__(self, height):
        self.height = height
        self.table = self.load_data()
        self.actions = [False, True]

        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY


    def load_data(self):
        path = Path(__file__).resolve().parent / "q_table.pkl"

        if path.exists():
            with open(path, "rb") as f:
                q_table = defaultdict(float, pickle.load(f))
        else:
            q_table = defaultdict(float)

        print("====================================\n====================================\n====================================\n====================================\n====================================\n====================================\n====================================\n====================================\n")
        print(q_table)

        return q_table


    def save_data(self):
        path = Path(__file__).resolve().parent / "q_table.pkl"

        temp_path = path.with_suffix(".tmp")
        with open(temp_path, "wb") as f:
            pickle.dump(dict(self.table), f)
        os.replace(temp_path, path)


    def determine_state(self, player, player_vy, obstacles):
        if len(obstacles) > 0:
            obst_top = obstacles[0]
            obst_bt = obstacles[1]

            if obst_top.x + obst_top.w < player.x and len(obstacles) > 2:
                obst_top = obstacles[2]
                obst_bt = obstacles[3]       

            dx = obst_top.x - player.x
            dx = clamp(0, 300, dx)
            dx = round_to_n(dx, dx_BINSIZE)
            
            bottom_of_top = obst_top.y + obst_top.h
            top_of_bottom = obst_bt.y
            middle = 0.5 * (bottom_of_top + top_of_bottom)
            
            dy = round_to_n(middle - player.y, dy_BINSIZE)

            
            bottom_of_top = obst_top.y + obst_top.h
            top_of_bottom = obst_bt.y
            middle = 0.5*(bottom_of_top + top_of_bottom)
            
            dy = round_to_n(middle - player.y,dy_BINSIZE)  #distance to middle of obstacle gap

        else: #if no obstaclesa on screen, resort to default values
            dx = -10000
            dy = -10000

        vy = round_to_n(player_vy,vy_BINSIZE) #player velocity

        near_ceiling = 1 if player.y < 50 else 0 #if it is near ceiling to avoid constant suicide

        return (int(dx), int(dy), int(vy), near_ceiling)


    def get_action(self, state):
        if random.random() <= self.epsilon: #random state
            return random.choice(self.actions)

        #query table for state
        q_values = [self.get_q(state, a) for a in self.actions]
        q_max = max(q_values)

        choices = []

        for i in range(len(q_values)):
            if q_values[i] == q_max:
                choices.append(self.actions[i])

        
   
        return random.choice(choices)


    def get_expected_qmax(self, state):
        q_values = [self.get_q(state, a) for a in self.actions]
        q_max = max(q_values)
        
        return q_max


    def update_q(self, state, action, new_state, reward, dead):
        qmax = self.get_expected_qmax(new_state)
        current = self.get_q(state, action)

        target = reward if dead else (reward + GAMMA * qmax)

        self.table[(state, action)] = current + LR*(target - current)    


    def get_q(self, state, action):
        return self.table[(state, action)]

    def die(self):
        if self.epsilon > self.epsilon_min: #decay epsilon to reduce exploration over time
            self.epsilon *= self.epsilon_decay
        
        self.save_data()