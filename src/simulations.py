from display_app import Simulation
from scipy.signal import convolve2d
from einops import repeat
import numpy as np


class RandomSimulation(Simulation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rng = np.random.default_rng()

    def step(self):
        while True:
            yield self.rng.integers(0, 255, size=(200, 200, 3), dtype=np.uint8)


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


class GameOfLifeSimulation(Simulation):
    def __init__(self, grid_size: int = 400, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = grid_size
        self.rng = np.random.default_rng()
        self.grid = self.rng.integers(0, 2, size=(self.grid_size, self.grid_size))

    def step(self):
        while True:
            neighbours = convolve2d(
                self.grid,
                [[1, 1, 1], [1, 7, 1], [1, 1, 1]],
                boundary="fill",
                mode="same",
            )
            self.grid = np.isin(neighbours, [9, 10, 3]).astype(np.uint8)
            yield repeat(self.grid, "h w -> h w 3") * 255


class RandomRainfall(Simulation):
    def __init__(self, grid_size: int = 200, num_points: int = 500, **kwargs):
        super().__init__(**kwargs)
        self.grid_size = grid_size
        self.rng = np.random.default_rng()
        self.num_points = num_points
        self.points = self.rng.integers(0, grid_size, size=(2, num_points))
        self.grid = np.zeros((self.grid_size, self.grid_size, 3))

    def step(self):
        while True:
            updates = self.rng.integers(-1, 2, size=self.points.shape)
            updates[0, :] = np.clip(np.abs(updates[0, :]), 0, 1)
            self.points += updates.astype(np.uint8)
            self.points %= self.grid_size
            self.points = self.points.astype(np.uint8)
            self.grid *= 0.95
            self.grid[*self.points, :] = 255
            # self.grid[..., 0] = np.roll(self.grid[..., 0], 1)
            # self.grid[..., 1] = np.roll(self.grid[..., 1], -1)
            yield self.grid.astype(np.uint8)
