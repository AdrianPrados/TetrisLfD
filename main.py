"""
Tetris in Python for DQN used for Learninf from Demonstrations
Run this for manual testing of Tetris Enviorment (play normal Tetris)
"""

from enviorment.tetris import Tetris

env = Tetris({
    'reduced_shapes':0,
    'reduced_grid': 0
})


def main():
    while 1:
        env.reset()
        done = False
        while not done:
            state, action, done = env.render(1)


if __name__ == "__main__":
    main()
