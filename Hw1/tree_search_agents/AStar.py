"""
    Name:
    Surname:
    Student ID:
"""


from tree_search_agents.TreeSearchAgent import *
from tree_search_agents.PriorityQueue import PriorityQueue
import time


class AStarAgent(TreeSearchAgent):
    def run(self, env: Environment) -> (List[int], float, list):
        """
            You should implement this method for A* algorithm.

            DO NOT CHANGE the name, parameters and output of the method.
        :param env: Environment
        :return: List of actions and total score
        """
        prq = PriorityQueue()
        path = []  # for the visited list
        explored = []
        tmp_reward = 0;
        exp_dict = {env.to_state(env.current_position): [tmp_reward, -1]}  # for the expansion list
        prq.enqueue(env.current_position, 0)
        start_pos = env.current_position

        if env.is_done(env.current_position):
            return path
        else:
            asd = 1
            run = 0
            found = 0
            while (not prq.is_empty() and not found):  # not prq.is_empty()
                run += 1
                dequed_item = prq.dequeue()  # pop it
                if not isinstance(dequed_item, int):  # if int
                    dequed_item = env.to_state(dequed_item)  # change pos -> int

                env.set_current_state(dequed_item)  # get as int
                reward = exp_dict[dequed_item][0]

                explored.append(dequed_item)  # add it
                pos = env.current_position  # get for reward calc?

                for i in range(4):
                    if not found:
                        tmp_mov_pos, tmp_reward, _ = env.move(i)
                        env.set_current_state(env.to_state(pos))
                        if tmp_mov_pos not in (key for key in exp_dict):
                            if env.get_node_type(env.to_position(tmp_mov_pos)) != 'D':
                                if env.to_position(tmp_mov_pos)[0] in range(0, env.grid_size):
                                    if env.to_position(tmp_mov_pos)[1] in range(0, env.grid_size):
                                        if env.get_node_type(env.to_position(tmp_mov_pos)) == 'G':

                                            tmp_reward += reward

                                            print(tmp_mov_pos)
                                            tmp_reward += self.get_heuristic(env, tmp_mov_pos)


                                            prq.enqueue(tmp_mov_pos, tmp_reward)
                                            exp_dict.update({tmp_mov_pos: [tmp_reward, i]})

                                            dequed_item = prq.dequeue()  # pop it
                                            if not isinstance(dequed_item, int):  # if int
                                                dequed_item = env.to_state(dequed_item)  # change pos -> int
                                            explored.append(dequed_item)  # add it
                                            final_pos = env.to_position(dequed_item)
                                            found = 1
                                        else:   # for all almost all stiuations
                                            tmp_reward += reward
                                            print("before tmp_reward")
                                            print(tmp_reward)
                                            #tmp_reward += 1.000000*self.get_heuristic(env, tmp_mov_pos)
                                            print("after tmp_reward")
                                            print(tmp_reward)
                                            prq.enqueue(tmp_mov_pos, tmp_reward)
                                            exp_dict.update({tmp_mov_pos: [tmp_reward, i]})

            while final_pos != start_pos:
                if exp_dict[env.to_state(final_pos)][1] == 0:
                    final_pos[0] = final_pos[0] + 1
                    path.append(0)
                if exp_dict[env.to_state(final_pos)][1] == 1:
                    final_pos[1] = final_pos[1] + 1
                    path.append(1)
                if exp_dict[env.to_state(final_pos)][1] == 2:
                    final_pos[0] = final_pos[0] - 1
                    path.append(2)
                if exp_dict[env.to_state(final_pos)][1] == 3:
                    final_pos[1] = final_pos[1] - 1
                    path.append(3)
            path.reverse()
        score = TreeSearchAgent.play(self, env, path)
        print("length of dic")
        print(len(exp_dict))
        return path, score, exp_dict

    def get_heuristic(self, env: Environment, state: int, **kwargs) -> float:
        """
            You should implement your heuristic calculation for A*

            DO NOT CHANGE the name, parameters and output of the method.

            Note that you can use kwargs to get more parameters :)
        :param env: Environment object
        :param state: Current state
        :param kwargs: More parameters
        :return: Heuristic score
        """
        #print(state)
        curr_pos = env.to_position(state)
        #print(env.to_position(state))
        goals = env.get_goals()
        min_pos = 9999
        for i in goals:
            goal_pos = abs(env.to_position(i)[0] - curr_pos[0]) + abs(env.to_position(i)[1] - curr_pos[1])
            if goal_pos < min_pos:
                min_pos = goal_pos
            """
            print("GOAL_LOC")
            print(env.to_position(i))
            print("goal_pos")
            print(goal_pos)"""

        #print("min_pos")
        #print(min_pos)
        min_pos = - min_pos
        return min_pos

    @property
    def name(self) -> str:
        return "AStar"
