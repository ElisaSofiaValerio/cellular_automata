import numpy as np

from cellular_automata.algorithm.generation_computer import GenCompute


def test_first_gen():

    grid = np.zeros(shape=(10, 10))
    grid[4][4] = 1
    grid[4][5] = 1
    grid[5][4] = 1
    grid[5][5] = 1

    kernel = np.zeros(shape=(3, 3))
    kernel[0][0] = 1
    kernel[0][1] = 1
    kernel[-1][0] = 1
    kernel[-1][1] = 1

    birth = [2, 7]
    survival = [2, 7]

    test_object = GenCompute()
    new_grid = test_object.next_step(grid, kernel, birth, survival)

    target_grid = np.zeros(shape=(10, 10))
    target_grid[3][5] = 1
    target_grid[4][5] = 1
    target_grid[5][5] = 1
    target_grid[6][5] = 1

    np.testing.assert_equal(new_grid, target_grid)


def test_second_gen():

    grid = np.zeros(shape=(10, 10))
    grid[3][5] = 1
    grid[4][5] = 1
    grid[6][5] = 1
    grid[5][5] = 1

    kernel = np.zeros(shape=(3, 3))
    kernel[0][0] = 1
    kernel[0][1] = 1
    kernel[-1][0] = 1
    kernel[-1][1] = 1

    birth = [2, 7]
    survival = [2, 7]

    test_object = GenCompute()
    new_grid = test_object.next_step(grid, kernel, birth, survival)

    target_grid = np.zeros(shape=(10, 10))
    target_grid[4][5] = 1
    target_grid[5][5] = 1
    target_grid[5][6] = 1
    target_grid[4][6] = 1

    np.testing.assert_equal(new_grid, target_grid)


