"""
    Name:
    Surname:
    Student ID:
"""

import os.path

import tree_search_agents
from Environment import Environment
import time


GRID_DIR = "grid_worlds/"


if __name__ == "__main__":
    """ file_name = input("Enter file name: ")  """
    file_name = "Grid5.pkl"
    assert os.path.exists(os.path.join(GRID_DIR, file_name)), "Invalid File"

    env = Environment(os.path.join(GRID_DIR, file_name))

    agents = [tree_search_agents.AStarAgent(), tree_search_agents.UCSAgent()]

    actions = ["UP", "LEFT", "DOWN", "RIGHT"]

    for agent in agents:
        print("*" * 50)
        print(agent.name)

        env.reset()

        start_time = time.time_ns()

        path, score, expansion = agent.run(env)

        end_time = time.time_ns()

        print("Actions:", [actions[i] for i in path])
        print("Score:", score)
        print("Expansion:", expansion)

        print("Elapsed Time (ms):", (end_time - start_time) * 1e-6)

        print("*" * 50)
