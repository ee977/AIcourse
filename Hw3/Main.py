"""
    Name:
    Surname:
    Student ID:
"""

import os.path

import numpy as np
import matplotlib.pyplot as plt

import rl_agents
from Environment import Environment
import time


GRID_DIR = "grid_worlds/"


if __name__ == "__main__":
    #file_name = input("Enter file name: ")
    file_name = "Grid5.pkl"
    assert os.path.exists(os.path.join(GRID_DIR, file_name)), "Invalid File"

    env = Environment(os.path.join(GRID_DIR, file_name))

    # Type your parameters env,seed,discount_rate,epsilon,epsilon_decay,epsilon_min,alpha,max_episode
    agents = [rl_agents.QLearningAgent(env, 0, 0.9, 1, 0.9, 0.001, 1, 200), rl_agents.QLearningAgent(env, 0, 0.9, 1, 0.9, 0.001, 0.5, 500) , rl_agents.QLearningAgent(env, 0, 0.9, 1, 0.9, 0.001, 0.1, 500)] #rl_agents.SARSAAgent(env, 0, 0.9, 1, 0.9, 0.0001, 1, 200)
    actions = ["UP", "LEFT", "DOWN", "RIGHT"]
    for agent in agents:
        print("*" * 50)
        env.reset()
        start_time = time.time_ns()
        agent.train()
        end_time = time.time_ns()
        path, score = agent.validate()
        print("Actions:", [actions[i] for i in path])
        print("Score:", score)
        print("Elapsed Time (ms):", (end_time - start_time) * 1e-6)

