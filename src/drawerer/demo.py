from drawerer.core import DisplayApp, Simulation
import numpy as np


class RandomWalkerSimulation(Simulation):
    def __init__(self, grid_size: int = 200, num_points: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = grid_size
        self.rng = np.random.default_rng()
        half = self.grid_size // 2
        self.points = self.rng.integers(0, half, size=(2, num_points)) + half // 2
        self.grid = np.zeros((self.grid_size, self.grid_size, 3))

    def step(self):
        while True:
            self.points += ((self.rng.random(self.points.shape) * 10) - 5).astype(int)
            self.points %= self.grid_size
            self.grid *= 0.9
            self.grid[*self.points, :] = 255
            yield self.grid.astype(np.uint8)


def main():
    DisplayApp(RandomWalkerSimulation()).run()


if __name__ == "__main__":
    main()
