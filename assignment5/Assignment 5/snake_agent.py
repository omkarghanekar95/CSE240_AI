import numpy as np
import helper
import random

#   This class has all the functions and variables necessary to implement snake game
#   We will be using Q learning to do this

class SnakeAgent:

    #   This is the constructor for the SnakeAgent class
    #   It initializes the actions that can be made,
    #   Ne which is a parameter helpful to perform exploration before deciding next action,
    #   LPC which ia parameter helpful in calculating learning rate (lr) 
    #   gamma which is another parameter helpful in calculating next move, in other words  
    #            gamma is used to blalance immediate and future reward
    #   Q is the q-table used in Q-learning
    #   N is the next state used to explore possible moves and decide the best one before updating
    #           the q-table
    def __init__(self, actions, Ne, LPC, gamma=0.7):
        self.actions = actions
        self.Ne = Ne
        self.LPC = LPC
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = helper.initialize_q_as_zeros()
        self.N = helper.initialize_q_as_zeros()


    #   This function sets if the program is in training mode or testing mode.
    def set_train(self):
        self._train = True

     #   This function sets if the program is in training mode or testing mode.       
    def set_eval(self):
        self._train = False

    #   Calls the helper function to save the q-table after training
    def save_model(self):
        helper.save(self.Q)

    #   Calls the helper function to load the q-table when testing
    def load_model(self):
        self.Q = helper.load()

    #   resets the game state
    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    #   This is a function you should write. 
    #   Function Helper:IT gets the current state, and based on the 
    #   current snake head location, body and food location,
    #   determines which move(s) it can make by also using the 
    #   board variables to see if its near a wall or if  the
    #   moves it can make lead it into the snake body and so on. 
    #   This can return a list of variables that help you keep track of
    #   conditions mentioned above.

    # def wall_check(self):
    #     if self.snake.xcor() > 200 or self.snake.xcor() < -200 or self.snake.ycor() > 200 or self.snake.ycor() < -200:
    #         self.reset_score()
    #         return True

    # def measure_distance(self):
    #     self.prev_dist = self.dist
    #     self.dist = math.sqrt((self.snake.xcor()-self.apple.xcor())**2 + (self.snake.ycor()-self.apple.ycor())**2)


    def helper_func(self, state):
        print("IN helper_func")
        print('state in helper' , state)
        cur_state = [0, 0, 0, 0, 0, 0, 0, 0]
        if state[0] < state[3]:
            cur_state[0] = 2
        if state[0] > state[3]:
            cur_state[0] = 1
        if state[0] == helper.GRID_SIZE:
            cur_state[2] = 1
        if state[0] == (helper.DISPLAY_SIZE - 2 * helper.GRID_SIZE):
            cur_state[2] = 2
        if state[0] < helper.GRID_SIZE:
            cur_state[2] = 0
            cur_state[3] = 0
        if state[0] > (helper.DISPLAY_SIZE - 2 * helper.GRID_SIZE):
            cur_state[2] = 0
            cur_state[3] = 0
        if state[1] < helper.GRID_SIZE:
            cur_state[2] = 0
            cur_state[3] = 0
        if state[1] > (helper.DISPLAY_SIZE - 2 * helper.GRID_SIZE):
            cur_state[2] = 0
            cur_state[3] = 0
        if state[1] > state[4]:
            cur_state[1] = 1
        if state[1] < state[4]:
            cur_state[1] = 2
        if state[1] == helper.GRID_SIZE:
            cur_state[3] = 1
        if (state[0] + helper.GRID_SIZE, state[1]) in state[2]:
            cur_state[7] = 1
        if (state[0] - helper.GRID_SIZE, state[1]) in state[2]:
            cur_state[6] = 1
        if state[1] == (helper.DISPLAY_SIZE - 2 * helper.GRID_SIZE):
            cur_state[3] = 2
        if (state[0], state[1] + helper.GRID_SIZE) in state[2]:
            cur_state[5] = 1
        if (state[0], state[1] - helper.GRID_SIZE) in state[2]:
            cur_state[4] = 1
        return tuple(cur_state)
        # [200, 200, [], 120, 120]
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE


    # Computing the reward, need not be changed.
    def compute_reward(self, points, dead):
        if dead:
            return -1
        elif points > self.points:
            return 1
        else:
            return -0.1

    #   This is the code you need to write. 
    #   This is the reinforcement learning agent
    #   use the helper_func you need to write above to
    #   decide which move is the best move that the snake needs to make 
    #   using the compute reward function defined above. 
    #   This function also keeps track of the fact that we are in 
    #   training state or testing state so that it can decide if it needs
    #   to update the Q variable. It can use the N variable to test outcomes
    #   of possible moves it can make. 
    #   the LPC variable can be used to determine the learning rate (lr), but if 
    #   you're stuck on how to do this, just use a learning rate of 0.7 first,
    #   get your code to work then work on this.
    #   gamma is another useful parameter to determine the learning rate.
    #   based on the lr, reward, and gamma values you can update the q-table.
    #   If you're not in training mode, use the q-table loaded (already done)
    #   to make moves based on that.
    #   the only thing this function should return is the best action to take
    #   ie. (0 or 1 or 2 or 3) respectively. 
    #   The parameters defined should be enough. If you want to describe more elaborate
    #   states as mentioned in helper_func, use the state variable to contain all that.
    def agent_action(self, state, points, dead):
        print("IN AGENT_ACTION")
        rew = self.compute_reward(points, dead)
        rstate = self.helper_func(state)
        print('state after helper and reward is ', rew, rstate)

        if not self._train:
            temp = self.Q[rstate][3] - 1
            for i in range(3, -1, -1):
                q = self.Q[rstate][i]
                if q > temp:
                    temp = q
                    self.a = i
        else:
            if self.a != None:
                if self.s != None:
                    if dead:
                        r = -1
                    elif points == self.points + 1:
                        r = 1
                    else:
                        r = -0.1
                    temp = self.Q[rstate][3] - 1
                    for i in range(3, -1, -1):
                        q = self.Q[rstate][i]
                        if q > temp:
                            temp = q
                    self.N[self.s][self.a] += 1
                    self.Q[self.s][self.a] += (self.LPC / (self.N[self.s][self.a] + self.LPC)) * (self.gamma * temp + r - self.Q[self.s][self.a])
            if dead:
                self.reset()
                return 1
            self.s = rstate
            self.points = points
            temp = self.Q[rstate][3] - 1
            for i in range(3, -1, -1):
                if self.N[rstate][i] < self.Ne:
                    p = 1
                else:
                    p = self.Q[rstate][i]
                if p > temp:
                    temp = p
                    self.a = i

        return self.a
        # YOUR CODE HERE