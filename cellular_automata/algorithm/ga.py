from typing import List
import numpy as np

from cellular_automata.algorithm.generation_computer import GenCompute


# The algorithm we will be using is called Genetic Algorithm
# What da goal?
# Given a initial grid configuration
# I will also give you a final grid configuration
# Find the kernel
# Find the Birth and surival rule
# For any N number of frames/generations


# What da genetic algorithm?
# We have a population. N = 200 members
# Fitness, how fit is each member of the population.
# Select top fit members.
# Crossover - With top fit members, generate new population. Whose size is also N=200members.
# Mutation - Randomly mutate a single 'gene' in some members.
# Repeat

#For our use case.
# We define population, or each member as a possible solution.
# Solution = birth conditions, survival conditiosn, kernel
# Example: Birth = [0, 2, 7],        [1, 0, 1, 0, 0, 0, 0 ,1, 0], surival = [1, 3] = [0, 1, 0, 1, 0, 0,0 ,0,0], kernel = [1, 1, 1, 1, 0, 1, 1, 1, 1]
# A population member = [1, 0, 1, 0, 0, 0, 0 ,1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]

# How do you check fitness
# For each member, you run another loop internal loop.
# This loop takes the input grid, and applies the rules for b,s, kernel. For 50 steps
# For each of the 50 steps, you get 50 grids, compute dice score of each of these grids with target grid.
# Get the best dice score as your final grid and store the value of steps, which step was that grid.
# Dice score - suggestion

# Select top 20% of the highest dice score members.
# Crossover
# pop1 = [1, 0, 1, 0, 0, 0, 0 ,1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]
# pop2 = [1, 1, 1, 0, 0, 0, 0 ,1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]
# Child1 = [1, 0, 1, 0, 0, 0, 0 ,1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]
# Child2 = alternate bits, alternate from p1 and p2
# Keep the parents the top 20% also in the next generation.

#Mutation
# For each member of population, there is a 1% chance or even 0.1% chance of a single gene mutating.
# Loop over each member of population and for each member, loop over each gene.
# Check for probabliitlu 1%, if yes, flip the bit
# pop1 = [1, 0, 1, 0, 0, 0, 0 ,1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]

# Now with new generation, repeat the process.
# Stop this process when you find perfect dice score 1, or closest to 1.
# Run this for like 200 or 300 generation.


# BREAK DOWN INTO STEPS

# STEP UNO -  Encode birth, survive, kernel into chromosomes i.e a member of population
# STEP DUE - GEenerate memembers of population automatically, its random.
# STEP TRE - Implement fitness for a SINGLE member of population.

class Chromosome:
    """
    FEEL FREE TO EDIT THIS CODE TO HOW YOU LIKE!
    ASSUMING BIRTH IS FIRST
    SURVIVAL IS SECOND
    KERNEL IS THIRD
    """
    def __init__(self, random_genes):
        self.genes = random_genes
        self.best_score = -1.0
        self.best_step = 0

    def get_birth(self):
        birth_rule = np.nonzero(self.genes[:9])[0]
        birth_rule = birth_rule.tolist()
        return birth_rule

    def get_survival(self):
        survival_rule = np.nonzero(self.genes[9:18])[0]
        survival_rule = survival_rule.tolist()
        return survival_rule

    def get_kernel(self):
        return np.array(self.genes[18:]).reshape(3, 3)

    def fitness(self, input_grid, target_grid):
        """
        COMPUTE AND RETURN DICE SCORE (OR ANY METRIC OF YOUR CHOICE) OF THIS CHROMOSOME
        RUN THIS CHROMOSOME THROUGH MULTIPLE STEPS WITH THE CODE YOU IMPLEMENTED BEFORE (next_step code)
        USE THE ABOVE FUNCTIONS TO MAKE LIFE EASIER, ALSO LEARN HOW THEY WORK.
        Run the next_step function for a certain number of steps. Let's say 50.
        MAKE SURE TO UPDATE self.best_score and self.best_step
        self.best_score is the best score you get out of all the steps you run
        self.best_step is the step/frame which has the best score.
        :return:
        """
        x = sum(sum(input_grid))
        y = sum(sum(target_grid))
        overlap = input_grid*target_grid
        intersection = sum(sum(overlap))
        dice_score = (2*intersection)/(x+y)
        self.best_score = dice_score

        number_of_steps = 50
        ev = GenCompute()
        current_grid = input_grid.copy()
        for i in range(number_of_steps):
            next_gen = ev.next_step(current_grid, self.get_kernel(), self.get_birth(), self.get_survival())
            x = sum(sum(next_gen))
            overlap = next_gen * target_grid
            intersection = sum(sum(overlap))
            dice_score = (2 * intersection) / (x + y)
            if dice_score > self.best_score:
                self.best_score = dice_score
                self.best_step = i
            current_grid = next_gen

        return dice_score


class GeneticEvolutionOfSnails:

    def __init__(self, input_grid, target, population_size=100, number_of_generations=100):
        self.input_grid = input_grid
        self.target_grid = target
        self.population_size = population_size
        self.num_gen = number_of_generations
        self.population = None

        # EDIT THESE VARIABLES TO YOUR LIKING
        self.crossover_percentage = 20
        self.mutation_rate_percentage = 1

    def generate_population(self):
        """
        Generate a population. Population number is defined by self.population_size. Use it
        Each member of population is Chromosome object
        Each chromosome object should be initialized with genes.
        Randomly generate a list of size 27, with random 0's or 1's, that is your random gene.
        Store each chromosome object in a list
        set self.population = the created list
        :return:
        """
        chromosomes_list = []
        for i in range(self.population_size):
            genes = np.random.rand(27)
            genes = np.round(genes)
            genes = genes.tolist()
            c = Chromosome(genes)
            chromosomes_list.append(c)
        self.population = chromosomes_list


    def crossover(self, top_chromosomes: List):
        """
        Given a list of top (20%) of the chromosomes, we perform crossover over all of them
        Use different crossover techniques to create children for next generation
        Use the current parents also in next generation
        You can also random generate new population for the next generation, choice is yours
        The next generation size should be a list of chromosomes equal to self.population_size
        :return next_generation_list:
        """
        # Write code here

    def mutation(self, next_generation: List):
        """
        Perform mutation per chromosome, per item in the gene based on mutation_rate_percentage (1%)
        Mutation is currently defined as flipping the bit, 0->1 or 1->0.
        return the next_generation_list after mutation
        :param next_generation:
        :return:
        """
        # Write code here

    def single_epoch(self):
        """
        For each member of population
        Compute its fitness score
        Store the best fitness score for each chromosome/population member
        Select top chromosomes based on crossover_rate (for 100 chromosomes, select top 20)
        Call self.crossover(top_chromosomes) function to give it the top chromosomes to do crossover
        You should recieve a new list, call it next_generation or something
        Send this new list to self.mutation(next_generation) function, to perform mutation.
        You now have a new generation
        set self.population = this new generation list
        return the best scoring chromosome object.
        :return:
        """
        # Write code here

    def run(self):
        """
        Run loop for number of generations
        For each epoch, return the top performing chromosome
        the top_performer should be Chromosome object
        Below that I print the best score for each generation and if the best score is 1.0
        Then you print the chromosome's kernel, birth and survival.
        :return:
        """
        self.generate_population()
        for n in range(self.num_gen):
            top_performer = self.single_epoch()
            print(top_performer.best_score, top_performer.best_step)
            if top_performer.best_score == 1.0:
                print(top_performer.get_kernel())
                print(top_performer.get_birth())
                print(top_performer.get_survival())


if __name__=='__main__':

    grid = np.zeros(shape=(10, 10))
    grid[4][4] = 1
    grid[4][5] = 1
    grid[5][4] = 1
    grid[5][5] = 1

    target_grid = np.zeros(shape=(10, 10))
    target_grid[4][5] = 1
    target_grid[5][5] = 1
    target_grid[5][6] = 1
    target_grid[4][6] = 1

    g = GeneticEvolutionOfSnails(population_size=200, number_of_generations=100, input_grid=grid, target=target_grid)
    g.run()

