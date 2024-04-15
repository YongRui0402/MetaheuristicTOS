import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Board.board import Board
import random
import timeit

class GA:
    def __init__(self, boardstring,limitpathlen=30,limittime=3,seed_value=-1):
        board = Board()
        board.initialize_board(boardstring)
        self.board = board
        self.best_path = ""
        self.best_score = 0
        self.find_sol =  0
        self.limittime =  limittime
        self.limitpathlen =  limitpathlen
        if seed_value !=-1:
            random.seed(seed_value)

    def fitness_function(self,solution):
        path = ''.join(str(x) for x in solution[2:])
        self.board.reset_board()
        self.board.make_move(solution[0],solution[1],path)
        fitness = self.board.cpmpute_scroce()
        
        return fitness
    
    def initialize_individual(self):
        individual = []
        startrow = 2
        startcol = 3
        individual.append(startrow)
        individual.append(startcol)
        for _ in range(10):
            gene = random.randint(0, 3)  
            individual.append(gene)
        return individual
    
    def initialize_population(self,population_size):
        population = []
        for _ in range(population_size):
            individual = self.initialize_individual()
            population.append(individual)
            
        return population
    
    def calculate_fitness(self,population):
        fitness_values = []
        for individual in population:
            fitness = self.fitness_function(individual)
            fitness_values.append(fitness)
            
        return fitness_values
    
    def selection(self, population, fitness_values):
        
        def roulette_wheel_selection(population, probabilities):
            cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
            random_number = random.random()
            
            for i, cumulative_probability in enumerate(cumulative_probabilities):
                if random_number <= cumulative_probability:
                    return population[i]
            
        total_fitness = sum(fitness_values)
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        selected_population = []
        for _ in range(len(population)):
            selected_individual = roulette_wheel_selection(population, probabilities)
            selected_population.append(selected_individual)
        
        return selected_population

    def crossover(self,parent1, parent2):
        crossover_pointrate = random.random()
        crossover_point1 = max(2,round((len(parent1)-1)*crossover_pointrate+1))
        crossover_point2 = max(2,round((len(parent2)-1)*crossover_pointrate+1))
        offspring1 = parent1[:crossover_point1] + parent2[crossover_point2:]
        offspring2 = parent2[:crossover_point2] + parent1[crossover_point1:]
        
        return offspring1, offspring2
    
    def mutate(self,individual):
        mutated_individual = []
        mnum = 1    
        mutation_rate = mnum/len(individual)
        mutation_start_rate = 1/9
        if random.random() < mutation_start_rate:
            mutated_gene = (individual[0] + random.randint(-1,1) + 5)%5
            mutated_individual.append(mutated_gene)
            mutated_gene = (individual[1] + random.randint(-1,1) + 6)%6
            mutated_individual.append(mutated_gene)
        else:  
            mutated_individual.append(individual[0])
            mutated_individual.append(individual[1])
        for gene in individual[2:]:
            if random.random() < mutation_rate:
                mutated_gene = (gene + random.randint(1, 3))%4
            else:
                mutated_gene = gene
            mutated_individual.append(mutated_gene)
        mutation_add_rate = 0.2
        mutation_add_num = random.randint(1, 10)
        if random.random() < mutation_add_rate:
            if(len(mutated_individual)-2+mutation_add_num<self.limitpathlen):
                for i in range(mutation_add_num):
                    mutated_individual.append(random.randint(0, 3))
        if random.random() < mutation_add_rate:
            if(len(mutated_individual)-2>mutation_add_num):
                mutated_individual=mutated_individual[:-mutation_add_num]
                
        return mutated_individual
    
    def find_path(self,population_size=100, generations=1000):
        population = self.initialize_population(population_size)
        self.best_path = population[0]
        startrow = 0
        startcol = 0
        best_path = ''
        start = timeit.default_timer()
        for _ in range(generations):
            fitness_values = self.calculate_fitness(population)
            selected_population = self.selection(population, fitness_values)
            offspring_population = []
            for i in range(0, len(selected_population), 2):
                parent1 = selected_population[i]
                parent2 = selected_population[i+1]
                offspring1, offspring2 = self.crossover(parent1, parent2)
                offspring_population.append(offspring1)
                offspring_population.append(offspring2)
            mutated_population = [self.mutate(individual) for individual in offspring_population]
            population = mutated_population
            tmp_best_path = max(population, key=self.fitness_function)
            best_score = self.fitness_function(self.best_path)
            tmp_best_score = self.fitness_function(tmp_best_path)
            if  best_score < tmp_best_score:
                self.best_path = tmp_best_path
                self.best_score = tmp_best_score
                startrow = self.best_path[0]
                startcol = self.best_path[1]
                best_path = ''.join(str(x) for x in self.best_path[2:])
            if timeit.default_timer() - start > self.limittime:
                return startrow,startcol,best_path

        return startrow,startcol,best_path