import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from pygame.math import Vector2


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        act_values = self.model(state)
        return torch.argmax(act_values[0]).item()

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = torch.FloatTensor(state).unsqueeze(0)
            next_state = torch.FloatTensor(next_state).unsqueeze(0)
            target = reward
            if not done:
                target = (reward + self.gamma * torch.max(self.model(next_state)[0]).item())
            
            target_f = self.model(state)
            target_f[0][action] = target
            
            self.optimizer.zero_grad()
            loss = self.criterion(self.model(state), target_f)
            loss.backward()
            self.optimizer.step()
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_state(self, game):
        head = game.snake.body[0]
        
        point_l = Vector2(head.x - 1, head.y)
        point_r = Vector2(head.x + 1, head.y)
        point_u = Vector2(head.x, head.y - 1)
        point_d = Vector2(head.x, head.y + 1)
        
        dir_l = game.snake.direction.x == -1
        dir_r = game.snake.direction.x == 1
        dir_u = game.snake.direction.y == -1
        dir_d = game.snake.direction.y == 1

        state = [
            # Danger straight
            (dir_r and game.snake.check_collision_at(point_r)) or 
            (dir_l and game.snake.check_collision_at(point_l)) or 
            (dir_u and game.snake.check_collision_at(point_u)) or 
            (dir_d and game.snake.check_collision_at(point_d)),

            # Danger right
            (dir_u and game.snake.check_collision_at(point_r)) or 
            (dir_d and game.snake.check_collision_at(point_l)) or 
            (dir_l and game.snake.check_collision_at(point_u)) or 
            (dir_r and game.snake.check_collision_at(point_d)),

            # Danger left
            (dir_d and game.snake.check_collision_at(point_r)) or 
            (dir_u and game.snake.check_collision_at(point_l)) or 
            (dir_r and game.snake.check_collision_at(point_u)) or 
            (dir_l and game.snake.check_collision_at(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.position.x < head.x,  # food left
            game.food.position.x > head.x,  # food right
            game.food.position.y < head.y,  # food up
            game.food.position.y > head.y  # food down
        ]

        return np.array(state, dtype=int)
