#!/usr/bin/env python3

from __future__ import annotations

import copy
import gymnasium as gym
import pickle
from minigrid.minigrid_env import MiniGridEnv
from minigrid.utils.window import Window
from minigrid.wrappers import ImgObsWrapper, RGBImgPartialObsWrapper

dataset=[]
#trajdata=[]
#trajnum=1

class ManualControl:
    def __init__(
        self,
        env: MiniGridEnv,
        agent_view: bool = False,
        window: Window = None,
        seed=None,
        
    ) -> None:
        self.env = env
        self.agent_view = agent_view
        self.seed = seed
        self.trajnum = 1#so it doesnt reset
        self.trajdata = []

        if window is None:
            window = Window("minigrid - " + str(env.__class__))
        self.window = window
        self.window.reg_key_handler(self.key_handler)

    def start(self):
        """Start the window display with blocking event loop"""
        self.reset(self.seed)
        self.window.show(block=True)



    def step(self, action: MiniGridEnv.Actions):
        _, reward, terminated, truncated, _ = self.env.step(action)
        print(f"step={self.env.step_count}, reward={reward:.2f}")
        #print(self.env)####################################noah add

        #s1=self.env
        #print(dataset)
        #s1=copy.deepcopy(self.env)
        #s2=self.env.step_count
        #a1=key
        #trajectory={
        #    'id':'traj1'
        #    'data':[(self.env,key)]
            #'data':[(s1)]
        #}

        #statedata.append(s1)
        #dataset.append(s1)
        #print(dataset)

        if terminated:
            self.trajnum+=1
            dataset.append(self.trajdata)
            self.trajdata=[]
            print(dataset)
            print("terminated!")
            self.reset(self.seed)
        elif truncated:
            print("truncated!")
            self.reset(self.seed)
        else:
            self.redraw()

    def redraw(self):
        frame = self.env.get_frame(agent_pov=self.agent_view)
        self.window.show_img(frame)

    def reset(self, seed=None):
        self.env.reset(seed=seed)

        if hasattr(self.env, "mission"):
            print("Mission: %s" % self.env.mission)
            self.window.set_caption(self.env.mission)

        self.redraw()

    def key_handler(self, event):
        key: str = event.key
        print("pressed", key)

        a1=key



        if key == "escape":
            self.window.close()
            return
        if key == "backspace":
            self.reset()
            return

        key_to_action = {
            "left": MiniGridEnv.Actions.left,
            "right": MiniGridEnv.Actions.right,
            "up": MiniGridEnv.Actions.forward,
            " ": MiniGridEnv.Actions.toggle,
            "pageup": MiniGridEnv.Actions.pickup,
            "pagedown": MiniGridEnv.Actions.drop,
            "enter": MiniGridEnv.Actions.done,
        }

        action = key_to_action[key]
        self.step(action)

############################################# Noah  Add
        s1=copy.deepcopy(self.env)
        a1=key
        #dataset=[]
        trajectory={
            'id':[('trajectory',self.trajnum)],
            'data':[(s1,a1)]
        }


        if self.env.step_count == 1:
            self.trajdata.append(trajectory['id'])
            self.trajdata.append(trajectory['data'])
        elif self.env.step_count > 1:
            self.trajdata.append(trajectory['data'])

        
        #self.trajdata.append(trajectory['data'])

        #self.trajdata.append(trajectory['data'])

        #data=(s1,a1)
        #dataset.append(trajectory)
        #trajectory['data'].append((s1,a1))

        #actiondata.append(a1)
        #dataset.append(a1)

        #dataset.append(trajectory['data'])
        #trajectory['data'].append(dataset)

        #dataset.append(self.env)
        #dataset.append(key)
        #dataset.append(trajectory)


        #print(dataset)
        #print(trajectory)# just to make sure it works
        ##print(dataset)

        #dataset2=[dataset.append]
        
        #print(dataset2)

        #with open('traject.pkl', 'wb') as the_file:
        #    b = pickle.dump((trajectory),  the_file) 
                    
        #with open('traject.pkl', 'rb') as the_file:
        #    b = pickle.load(the_file)

        with open('traject.pkl', 'wb') as the_file:
            b = pickle.dump((dataset),  the_file) 
                    
        with open('traject.pkl', 'rb') as the_file:
            b = pickle.load(the_file)

        #dataset.append(statedata)
        #dataset.append(actiondata)
        #print(dataset)



########################################################        



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env", help="gym environment to load", default="MiniGrid-MultiRoom-N6-v0"
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="random seed to generate the environment with",
        default=None,
    )
    parser.add_argument(
        "--tile-size", type=int, help="size at which to render tiles", default=32
    )
    parser.add_argument(
        "--agent-view",
        default=False,
        help="draw the agent sees (partially observable view)",
        action="store_true",
    )

    args = parser.parse_args()

    env: MiniGridEnv = gym.make(args.env, tile_size=args.tile_size)

    if args.agent_view:
        print("Using agent view")
        env = RGBImgPartialObsWrapper(env, env.tile_size)
        env = ImgObsWrapper(env)

    manual_control = ManualControl(env, agent_view=args.agent_view, seed=args.seed)
    manual_control.start()
