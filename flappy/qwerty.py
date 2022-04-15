import copy
import random


class FlappyEnv(object):
    def __init__(self, use_pipes=False, deterministic=False):
        self.use_pipes = use_pipes
        self.deterministic = deterministic
        self.v = 0
        self.pipes = []
        self.currentState = None
        self.birdY = 0

    def reset(self):
        # This should completely reset your environment and return a new, fresh observation
        # This is like quitting and starting a new game.
        # The observation should be a 3D list of integers of dimension 4 x 50 x 50

        self.v = 0
        self.pipes = []
        self.birdY = 25

        observation = []

        for i in range(4):
            observation.append([])
            for j in range(50):
                observation[i].append([])
                for k in range(50):
                    observation[i][j].append(0)

        # draw ground and ceiling
        for i in range(50):
            observation[2][0][i] = 1
            observation[2][1][i] = 1
            observation[2][48][i] = 1
            observation[2][49][i] = 1

        # draw bird

        observation = self.drawBird(self.birdY, observation)
        self.currentState = copy.deepcopy(observation)

        return observation

    def drawBird(self, y, observation):
        newOb = copy.deepcopy(observation)
        # erase previous bird
        for i in range(50):
            for j in range(50):
                if newOb[2][i][j] == 2:
                    newOb[2][i][j] = 0

        # draw new bird
        for i in range(23, 28):
            newOb[2][y - 2][i] = 2
            newOb[2][y - 1][i] = 2
            newOb[2][y][i] = 2
            newOb[2][y + 1][i] = 2
            newOb[2][y + 2][i] = 2

        return newOb

    """
            observation=[]
            for i in range(4):
                observation.append([])
                for j in range(50):
                    observation[i].append([])
                    for k in range(50):
                        observation[i][j].append(0)
            """

    def step(self, action):
        # The input `action` is an integer in {0, 1} representing the action of the agent
        # 0 is doing nothing, 1 is "tapping the screen."
        # The observation should be a 3D list of integers of dimension 4 x 50 x 50
        # The reward should be a scalar value in {-1.0, 0, or 1.0}
        # done should be a boolean indicating whether the bird has crashed

        observation = copy.deepcopy(self.currentState)

        reward = 0
        done = False

        observation[0] = copy.deepcopy(self.currentState[1])
        observation[1] = copy.deepcopy(self.currentState[2])
        observation[2] = copy.deepcopy(self.currentState[3])

        # fill stage 3 with 0s

        # draw ground and ceiling
        for i in range(50):
            observation[3][0][i] = 1
            observation[3][1][i] = 1

            observation[3][5][i] = 1
            # observation[3][6][i]=1

            observation[3][48][i] = 1
            observation[3][49][i] = 1

        # move pipes
        for i in self.pipes:
            i[1] -= 1

        # Spawn/delete pipes if needed
        if self.use_pipes:
            if len(self.pipes) == 0 or self.pipes[len(self.pipes) - 1][1] < 28:
                if self.deterministic:
                    self.pipes.append([15, 50])  # pipes have equal length
                else:
                    self.pipes.append([random.randrange(5, 25), 50])
            elif self.pipes[0][1] == -5:
                self.pipes.pop()

        # draw pipes
        for i in range(len(self.pipes)):
            height = self.pipes[i][0]
            for j in range(self.pipes[i][1] - 3, self.pipes[i][1] + 4):
                if j > 0 and j < 50:
                    for k in range(0, height):
                        observation[3][k][j] = 1
                    for k in range(height + 20, 49):
                        observation[3][k][j] = 1

        # Change bird position
        self.birdY += self.v

        # draw bird + ckeck collision and reward
        for i in range(23, 28):
            if self.birdY - 2 > 0 and self.birdY + 3 < 50:
                for j in range(self.birdY - 2, self.birdY + 3):
                    if (observation[3][j][i] == 1):  # collision
                        done = True
                        reward = -1.0
                    else:
                        observation[3][j][i] = 2

        # check if the bird passed the pipe
        for i in self.pipes:
            if i[1] == 23:
                reward = 1.0

        # change speed
        if action == 0:  # nothing
            self.v += 2
        else:  # tap
            self.v = -5

        self.currentState = copy.deepcopy(observation)
        return observation, reward, done  # returns a tuple


env = FlappyEnv()
state = env.reset()
for x in range(10):
    state = env.step(0)

"""
Questions
1. for first list in observation 0 = before before, 1 = before, 2 = current , 3 = next ? Also how can I store future 
A, What i am expecting
B, Compute 
2. is center of screen 24 or 25  // assumed 25 OK
3. [frame][row][colomn] observation[?][y][x]  
4. 2 errors
5. what does the "Object" give to this class. A: Nothing
6. Whats speed? Currently shown as 'v' A: class variable 
7. The bird position change according to the past speed or new speed? A: Move bird first then change speed 



pipes => [height, position]
"""




