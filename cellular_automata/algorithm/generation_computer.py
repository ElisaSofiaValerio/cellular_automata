import numpy as np
import scipy.signal
#from sklearn.externals.array_api_compat.torch import zeros #need to comment or I get an error


class GenCompute:
    def __init__(self):

        pass

    def next_step(self, grid: np.array, kernel: np.array, birth: list, survival: list):

        # Loop the kernel over the grid, to compute neighbours for each cell. Use wrap around.
        # Keep the neighbours values in a separate array
        neighbours_grid = scipy.signal.correlate2d(grid, kernel, mode='same', boundary='wrap')

        # I try to fix the bug here
        if not survival and not birth:
            next_gen_grid = np.zeros(grid.shape)
        else:
            next_gen_grid = grid.copy()
            # For cells with 0 in the grid, check for birth conditions using neighbour array
            # I removed the mask for the zeros
            index_r, index_c = np.where(grid == 0)
            for i in range(len(index_r)):
                if neighbours_grid[index_r[i]][index_c[i]] in birth:
                    next_gen_grid[index_r[i]][index_c[i]] = 1
            # For cells with 1 in the grid, check for survival conditions using neighbour array
            index_r, index_c = np.where(grid == 1)
            for i in range(len(index_r)):
                if neighbours_grid[index_r[i]][index_c[i]] not in survival:
                    next_gen_grid[index_r[i]][index_c[i]] = 0

        # return grid, please.
        return next_gen_grid

    def next_step_vone(self, grid: np.array, kernel: np.array, birth: list, survival: list):

        # Loop the kernel over the grid, to compute neighbours for each cell. Use wrap around.
        # Keep the neighbours values in a separate array
        neighbours_grid = scipy.signal.correlate2d(grid, kernel, mode='same', boundary='wrap')

        # For cells with 1 in the grid, check for survival conditions using neighbour array
        next_gen_grid = grid.copy()
        mask_grid = grid * neighbours_grid
        index_r, index_c = np.where(mask_grid != 0)

        for i in range(len(index_r)):
            if neighbours_grid[index_r[i]][index_c[i]] not in survival:
                next_gen_grid[index_r[i]][index_c[i]] = 0
        # For cells with 0 in the grid, check for birth conditions using neighbour array
        #Kindly fix a small bug here, its in your notes.
        mask_grid = (1 - grid) * neighbours_grid
        index_r, index_c = np.where(mask_grid != 0)
        for i in range(len(index_r)):
            if neighbours_grid[index_r[i]][index_c[i]] in birth:
                next_gen_grid[index_r[i]][index_c[i]] = 1

        # return grid, please.
        return next_gen_grid


if __name__ == '__main__':
    a = GenCompute()
