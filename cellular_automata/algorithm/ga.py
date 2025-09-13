

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