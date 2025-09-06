import numpy as np


class GenCompute:
    def __init__(self):

        pass

    def next_step(self, grid: np.array, kernel: np.array, birth: list, survival: list):

        # Loop the kernel over the grid, to compute neighbours for each cell. Use wrap around.

        # Keep the neighbours values in a separate array

        # For cells with 0 in the grid, check for birth conditions using neighbour array

        # For cells with 1 in the grid, check for survival conditions using neighbour array

        # Create new generation of grid

        # return grid, please.
        return grid


if __name__ == '__main__':
    a = GenCompute()
