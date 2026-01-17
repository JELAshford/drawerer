from skimage.draw import line_aa, disk
from drawerer.core import Simulation
from scipy.signal import convolve2d
from einops import repeat
import networkx as nx
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


class RandomGraphSimulation(Simulation):
    def __init__(
        self,
        grid_size: int = 1000,
        num_points: int = 100,
        num_connections: int = 80,
        seed: int = 1701,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.grid_size = grid_size
        self.rng = np.random.default_rng(seed=seed)
        self.grid = np.zeros((self.grid_size, self.grid_size, 3))
        # Create graph and get layout
        self.G = nx.Graph()
        for p1, p2, w in self.rng.integers(0, num_points, size=(num_connections, 3)):
            self.G.add_edge(p1, p2, weight=w)
        self.layout = nx.forceatlas2_layout(self.G)
        self.layout = nx.rescale_layout_dict(pos=self.layout, scale=0.5)
        self.layout = {
            n: (p + 0.5) * (self.grid_size - 1) for n, p in self.layout.items()
        }

    def step(self, eps: float = 1e-6):
        while True:
            self.grid *= 0.1
            # Generate layout
            self.layout = nx.forceatlas2_layout(self.G, pos=self.layout)
            self.layout = nx.rescale_layout_dict(pos=self.layout, scale=0.5)
            self.layout = {
                n: (p + 0.5) * (self.grid_size - 1) for n, p in self.layout.items()
            }
            # Draw graph edges
            for ind1, ind2 in self.G.edges:
                p1, p2 = self.layout[ind1], self.layout[ind2]
                yy, xx, val = line_aa(*p1.astype(int), *p2.astype(int))
                self.grid[yy, xx] = repeat((val * 0.5 * 255).astype(int), "l -> l 3")
            # Draw nodes
            for index, (y, x) in self.layout.items():
                yy, xx = disk((y, x), 4, shape=self.grid.shape)
                self.grid[yy, xx] = 255
            # Update weights slightly
            yield self.grid.astype(np.uint8)
